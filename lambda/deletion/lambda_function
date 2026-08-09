import hashlib
import json
import logging
import os
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
BUCKET_NAME = os.environ["BUCKET_NAME"]
ALLOWED_DELETE_PREFIX = os.environ.get("ALLOWED_DELETE_PREFIX", "raw/").lstrip("/")


def safe_log(level, payload):
    getattr(logger, level)(json.dumps(payload, separators=(",", ":"), default=str))


def api_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }


def supabase_request(method, table_name, query="", payload=None, prefer=None):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase configuration is missing")

    url = f"{SUPABASE_URL}/rest/v1/{table_name}"
    if query:
        url = f"{url}?{query}"

    data = json.dumps(payload).encode("utf-8") if payload is not None else None

    req = urllib.request.Request(url=url, data=data, method=method)
    req.add_header("apikey", SUPABASE_SERVICE_ROLE_KEY)
    req.add_header("Authorization", f"Bearer {SUPABASE_SERVICE_ROLE_KEY}")
    req.add_header("Content-Type", "application/json")
    if prefer:
        req.add_header("Prefer", prefer)

    try:
        with urllib.request.urlopen(req, timeout=10) as result:
            raw = result.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase {method} failed for {table_name}: {error.code} {body[:400]}"
        ) from error
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Supabase connection failed for {table_name}: {error.reason}"
        ) from error


def parse_event(event):
    raw_body = event.get("body") if isinstance(event, dict) else None
    if raw_body is None:
        body = event
    elif isinstance(raw_body, str):
        body = json.loads(raw_body)
    elif isinstance(raw_body, dict):
        body = raw_body
    else:
        raise ValueError("Unsupported request body")

    if not isinstance(body, dict):
        raise ValueError("Request must be a JSON object")

    document_id = str(body.get("documentId", "")).strip()
    request_type = str(body.get("requestType", "manual")).strip()
    reason = str(body.get("reason", "secure deletion request")).strip()[:200]

    if not document_id:
        raise ValueError("documentId is required")
    try:
        uuid.UUID(document_id)
    except ValueError as exc:
        raise ValueError("documentId must be a valid UUID") from exc
    if request_type not in {"manual", "retention"}:
        raise ValueError("requestType must be manual or retention")
    if not reason:
        raise ValueError("reason cannot be empty")

    return document_id, request_type, reason



def retention_is_expired(retention_until):
    if not retention_until:
        return False

    try:
        parsed = datetime.fromisoformat(str(retention_until).replace("Z", "+00:00"))
    except ValueError as exc:
        raise RuntimeError("Stored retention deadline is invalid") from exc

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc) <= datetime.now(timezone.utc)

def fingerprint(document_id):
    return hashlib.sha256(document_id.encode("utf-8")).hexdigest()


def get_document(document_id):
    rows = supabase_request(
        "GET",
        "documents",
        query=(
            f"id=eq.{document_id}"
            "&select=id,s3_bucket,s3_object_key,status,retention_until,retention_policy"
            "&limit=1"
        )
    )
    return rows[0] if rows else None


def get_completed_deletion(doc_fingerprint):
    rows = supabase_request(
        "GET",
        "deletion_requests",
        query=(
            f"document_fingerprint=eq.{doc_fingerprint}"
            "&status=eq.completed"
            "&select=id,status,completed_at,s3_objects_deleted,database_deleted,audit_redacted"
            "&order=completed_at.desc&limit=1"
        )
    )
    return rows[0] if rows else None


def create_deletion_request(request_id, document_id, doc_fingerprint, request_type, reason, trace_id):
    supabase_request(
        "POST",
        "deletion_requests",
        payload={
            "id": request_id,
            "document_id": document_id,
            "document_fingerprint": doc_fingerprint,
            "request_type": request_type,
            "status": "in_progress",
            "reason": reason,
            "trace_id": trace_id
        },
        prefer="return=minimal"
    )


def update_deletion_request(request_id, payload):
    supabase_request(
        "PATCH",
        "deletion_requests",
        query=f"id=eq.{request_id}",
        payload=payload,
        prefer="return=minimal"
    )


def validate_storage_target(document):
    bucket = document.get("s3_bucket")
    key = str(document.get("s3_object_key", ""))

    if bucket != BUCKET_NAME:
        raise RuntimeError("Document bucket is outside the allowed deletion scope")
    if not key.startswith(ALLOWED_DELETE_PREFIX):
        raise RuntimeError("Document object key is outside the allowed deletion prefix")
    if key.endswith("/") or ".." in key.split("/"):
        raise RuntimeError("Document object key failed safety validation")

    return bucket, key


def s3_object_exists(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as error:
        status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        code = error.response.get("Error", {}).get("Code")
        if status == 404 or code in {"404", "NoSuchKey", "NotFound"}:
            return False
        raise


def delete_s3_object_and_verify(bucket, key):
    if not s3_object_exists(bucket, key):
        return 0

    s3.delete_object(Bucket=bucket, Key=key)

    if s3_object_exists(bucket, key):
        raise RuntimeError("S3 object still exists after delete request")

    return 1


def redact_audit_logs(document_id):
    supabase_request(
        "PATCH",
        "audit_logs",
        query=f"document_id=eq.{document_id}",
        payload={
            "user_id": None,
            "company_id": None,
            "resource": None,
            "details": {
                "redacted": True,
                "reason": "secure_deletion",
                "retainedEvidence": "action,result,trace_id,timestamp"
            }
        },
        prefer="return=minimal"
    )


def delete_document(document_id):
    supabase_request(
        "DELETE",
        "documents",
        query=f"id=eq.{document_id}",
        prefer="return=minimal"
    )


def insert_completion_audit(doc_fingerprint, request_type, trace_id, s3_deleted):
    supabase_request(
        "POST",
        "audit_logs",
        payload={
            "document_id": None,
            "user_id": None,
            "company_id": None,
            "action": "SECURE_DELETION_COMPLETED",
            "resource": f"sha256:{doc_fingerprint}",
            "result": "SUCCESS",
            "trace_id": trace_id,
            "details": {
                "requestType": request_type,
                "s3ObjectsDeleted": s3_deleted,
                "databaseDeleted": True,
                "auditRedacted": True
            }
        },
        prefer="return=minimal"
    )


def lambda_handler(event, context):
    trace_id = getattr(context, "aws_request_id", str(uuid.uuid4()))
    request_id = str(uuid.uuid4())

    try:
        document_id, request_type, reason = parse_event(event)
    except (ValueError, json.JSONDecodeError) as error:
        safe_log("warning", {
            "traceId": trace_id,
            "stage": "secure_deletion",
            "status": "rejected",
            "reason": str(error)
        })
        return api_response(400, {"error": str(error), "traceId": trace_id})

    doc_fingerprint = fingerprint(document_id)

    try:
        completed = get_completed_deletion(doc_fingerprint)
        if completed:
            return api_response(200, {
                "message": "Deletion was already completed",
                "status": "completed",
                "deletionRequestId": completed["id"],
                "documentFingerprint": doc_fingerprint,
                "traceId": trace_id
            })

        document = get_document(document_id)
        if not document:
            return api_response(404, {"error": "Document not found", "traceId": trace_id})

        if request_type == "retention" and not retention_is_expired(
            document.get("retention_until")
        ):
            safe_log("warning", {
                "traceId": trace_id,
                "stage": "secure_deletion",
                "status": "retention_not_due"
            })
            return api_response(409, {
                "error": "Retention deadline has not expired",
                "status": "not_due",
                "traceId": trace_id
            })

        bucket, object_key = validate_storage_target(document)

        create_deletion_request(
            request_id, document_id, doc_fingerprint, request_type, reason, trace_id
        )

        safe_log("info", {
            "traceId": trace_id,
            "stage": "secure_deletion",
            "status": "started",
            "deletionRequestId": request_id,
            "requestType": request_type
        })

        s3_deleted = delete_s3_object_and_verify(bucket, object_key)
        update_deletion_request(request_id, {"s3_objects_deleted": s3_deleted})

        redact_audit_logs(document_id)
        update_deletion_request(request_id, {"audit_redacted": True})

        delete_document(document_id)

        completed_at = datetime.now(timezone.utc).isoformat()
        update_deletion_request(
            request_id,
            {
                "status": "completed",
                "database_deleted": True,
                "audit_redacted": True,
                "s3_objects_deleted": s3_deleted,
                "completed_at": completed_at
            }
        )

        completion_audit = "written"
        try:
            insert_completion_audit(
                doc_fingerprint, request_type, trace_id, s3_deleted
            )
        except Exception as audit_error:
            completion_audit = "failed"
            update_deletion_request(
                request_id,
                {
                    "error_code": "COMPLETION_AUDIT_WRITE_FAILED",
                    "error_message": str(audit_error)[:250]
                }
            )
            safe_log("error", {
                "traceId": trace_id,
                "stage": "secure_deletion",
                "status": "completion_audit_failed",
                "deletionRequestId": request_id,
                "errorType": type(audit_error).__name__
            })

        safe_log("info", {
            "traceId": trace_id,
            "stage": "secure_deletion",
            "status": "completed",
            "deletionRequestId": request_id,
            "requestType": request_type,
            "s3ObjectsDeleted": s3_deleted,
            "databaseDeleted": True,
            "auditRedacted": True,
            "completionAudit": completion_audit
        })

        return api_response(200, {
            "message": "Secure deletion completed",
            "status": "completed",
            "deletionRequestId": request_id,
            "documentFingerprint": doc_fingerprint,
            "s3ObjectsDeleted": s3_deleted,
            "databaseDeleted": True,
            "auditRedacted": True,
            "completionAudit": completion_audit,
            "traceId": trace_id
        })

    except Exception as error:
        try:
            update_deletion_request(
                request_id,
                {
                    "status": "failed",
                    "error_code": type(error).__name__,
                    "error_message": str(error)[:250]
                }
            )
        except Exception:
            pass

        safe_log("error", {
            "traceId": trace_id,
            "stage": "secure_deletion",
            "status": "failed",
            "deletionRequestId": request_id,
            "errorType": type(error).__name__,
            "errorMessage": str(error)[:250]
        })

        return api_response(500, {
            "error": "Secure deletion failed",
            "deletionRequestId": request_id,
            "traceId": trace_id
        })
