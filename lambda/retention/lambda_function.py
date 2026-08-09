import hashlib
import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client("lambda")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
DELETION_FUNCTION_NAME = os.environ["DELETION_FUNCTION_NAME"]
MAX_DOCUMENTS_PER_RUN = max(
    1,
    min(int(os.environ.get("MAX_DOCUMENTS_PER_RUN", "10")), 100)
)


def safe_log(level, payload):
    getattr(logger, level)(json.dumps(payload, separators=(",", ":"), default=str))


def document_fingerprint(document_id):
    return hashlib.sha256(document_id.encode("utf-8")).hexdigest()


def supabase_get(table_name, query):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase configuration is missing")

    url = f"{SUPABASE_URL}/rest/v1/{table_name}?{query}"
    request = urllib.request.Request(url=url, method="GET")
    request.add_header("apikey", SUPABASE_SERVICE_ROLE_KEY)
    request.add_header("Authorization", f"Bearer {SUPABASE_SERVICE_ROLE_KEY}")

    try:
        with urllib.request.urlopen(request, timeout=10) as result:
            raw = result.read().decode("utf-8")
            return json.loads(raw) if raw else []
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase GET failed: {error.code} {body[:300]}"
        ) from error
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Supabase connection failed: {error.reason}"
        ) from error


def get_expired_documents(document_id=None):
    now_utc = datetime.now(timezone.utc).isoformat()
    encoded_now = urllib.parse.quote(now_utc, safe=":-.")

    filters = [
        f"retention_until=lte.{encoded_now}",
        "retention_enforcement_enabled=eq.true"
    ]

    if document_id:
        try:
            uuid.UUID(document_id)
        except ValueError as exc:
            raise ValueError("documentId must be a valid UUID") from exc
        filters.append(f"id=eq.{document_id}")

    query = (
        "&".join(filters)
        + "&select=id,retention_until"
        + "&order=retention_until.asc"
        + f"&limit={MAX_DOCUMENTS_PER_RUN}"
    )

    return supabase_get("documents", query)


def invoke_deletion(document_id):
    payload = {
        "documentId": document_id,
        "requestType": "retention",
        "reason": "Prototype retention deadline expired"
    }

    response = lambda_client.invoke(
        FunctionName=DELETION_FUNCTION_NAME,
        InvocationType="RequestResponse",
        Payload=json.dumps(payload).encode("utf-8")
    )

    raw = response["Payload"].read().decode("utf-8")
    result = json.loads(raw) if raw else {}

    if response.get("FunctionError"):
        raise RuntimeError("Deletion Lambda returned a function error")

    return result


def lambda_handler(event, context):
    trace_id = getattr(context, "aws_request_id", "unknown")

    document_id = None
    if isinstance(event, dict):
        document_id = event.get("documentId")

    try:
        expired = get_expired_documents(document_id=document_id)
    except ValueError as error:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(error),
                "traceId": trace_id
            })
        }

    summary = {
        "expiredFound": len(expired),
        "processed": 0,
        "completed": 0,
        "skipped": 0,
        "failed": 0
    }

    safe_log("info", {
        "traceId": trace_id,
        "stage": "retention_enforcement",
        "status": "scan_started",
        "expiredFound": len(expired),
        "maxDocumentsPerRun": MAX_DOCUMENTS_PER_RUN
    })

    for document in expired:
        document_id = document["id"]
        fingerprint = document_fingerprint(document_id)

        try:
            result = invoke_deletion(document_id)
            status_code = int(result.get("statusCode", 500))
            summary["processed"] += 1

            if status_code == 200:
                summary["completed"] += 1
                outcome = "completed"
            elif status_code in {404, 409}:
                summary["skipped"] += 1
                outcome = "skipped"
            else:
                summary["failed"] += 1
                outcome = "failed"

            safe_log("info", {
                "traceId": trace_id,
                "stage": "retention_enforcement",
                "status": outcome,
                "documentFingerprint": fingerprint,
                "deletionStatusCode": status_code
            })

        except Exception as error:
            summary["processed"] += 1
            summary["failed"] += 1

            safe_log("error", {
                "traceId": trace_id,
                "stage": "retention_enforcement",
                "status": "failed",
                "documentFingerprint": fingerprint,
                "errorType": type(error).__name__,
                "errorMessage": str(error)[:200]
            })

    safe_log("info", {
        "traceId": trace_id,
        "stage": "retention_enforcement",
        "status": "scan_completed",
        **summary
    })

    if summary["failed"] > 0:
        raise RuntimeError(
            f"Retention scan completed with {summary['failed']} failed deletion(s)"
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Retention scan completed",
            **summary,
            "traceId": trace_id
        })
    }
