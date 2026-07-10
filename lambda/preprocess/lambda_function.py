import json
import os
import logging
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

BUCKET_NAME = os.environ.get("BUCKET_NAME", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png"
]


def supabase_request(method, table_name, payload=None, query_string=""):
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase configuration is missing")

    url = f"{SUPABASE_URL}/rest/v1/{table_name}{query_string}"

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url=url,
        data=data,
        method=method
    )

    request.add_header("apikey", SUPABASE_SERVICE_ROLE_KEY)
    request.add_header("Authorization", f"Bearer {SUPABASE_SERVICE_ROLE_KEY}")
    request.add_header("Content-Type", "application/json")

    if method in ["PATCH", "POST"]:
        request.add_header("Prefer", "return=minimal")

    try:
        with urllib.request.urlopen(request, timeout=8) as result:
            if result.status < 200 or result.status >= 300:
                raise RuntimeError(
                    f"Supabase request failed with status {result.status}"
                )

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase request failed for {table_name}: "
            f"{error.code} {error_body[:500]}"
        )

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Supabase connection failed for {table_name}: {str(error.reason)}"
        )


def update_document_status(document_id, status, trace_id):
    payload = {
        "status": status,
        "trace_id": trace_id,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }

    supabase_request(
        method="PATCH",
        table_name="documents",
        payload=payload,
        query_string=f"?id=eq.{document_id}"
    )


def insert_audit_log(
    document_id,
    user_id,
    company_id,
    action,
    resource,
    result,
    trace_id,
    details
):
    payload = {
        "document_id": document_id,
        "user_id": user_id,
        "company_id": company_id,
        "action": action,
        "resource": resource,
        "result": result,
        "trace_id": trace_id,
        "details": details
    }

    supabase_request(
        method="POST",
        table_name="audit_logs",
        payload=payload
    )


def parse_object_key(object_key):
    # Expected format:
    # raw/{company_id}/{user_id}/{document_id}/{file_name}
    parts = object_key.split("/")

    if len(parts) < 5:
        raise ValueError(
            "Object key does not match expected "
            "raw/company/user/document/file format"
        )

    prefix = parts[0]
    company_id = parts[1]
    user_id = parts[2]
    document_id = parts[3]
    file_name = "/".join(parts[4:])

    if prefix != "raw":
        raise ValueError("Object is not under raw prefix")

    return {
        "prefix": prefix,
        "company_id": company_id,
        "user_id": user_id,
        "document_id": document_id,
        "file_name": file_name
    }


def handle_s3_record(s3_record, trace_id):
    bucket_name = s3_record["s3"]["bucket"]["name"]
    raw_key = s3_record["s3"]["object"]["key"]
    object_key = urllib.parse.unquote_plus(raw_key)

    if bucket_name != BUCKET_NAME:
        raise ValueError("Unexpected S3 bucket")

    parsed = parse_object_key(object_key)

    document_id = parsed["document_id"]
    user_id = parsed["user_id"]
    company_id = parsed["company_id"]

    update_document_status(document_id, "uploaded", trace_id)

    insert_audit_log(
        document_id=document_id,
        user_id=user_id,
        company_id=company_id,
        action="FILE_UPLOADED",
        resource=object_key,
        result="SUCCESS",
        trace_id=trace_id,
        details={
            "bucket": bucket_name,
            "objectKey": object_key
        }
    )

    update_document_status(document_id, "preprocessing_started", trace_id)

    head_response = s3.head_object(
        Bucket=bucket_name,
        Key=object_key
    )

    object_size = head_response.get("ContentLength")
    content_type = head_response.get("ContentType", "unknown")

    if content_type not in ALLOWED_CONTENT_TYPES:
        update_document_status(document_id, "preprocessing_failed", trace_id)

        insert_audit_log(
            document_id=document_id,
            user_id=user_id,
            company_id=company_id,
            action="PREPROCESSING_FAILED",
            resource=object_key,
            result="FAILED",
            trace_id=trace_id,
            details={
                "reason": "Unsupported content type after upload",
                "contentType": content_type,
                "objectSize": object_size
            }
        )

        raise ValueError("Unsupported content type after upload")

    update_document_status(document_id, "preprocessing_completed", trace_id)

    insert_audit_log(
        document_id=document_id,
        user_id=user_id,
        company_id=company_id,
        action="PREPROCESSING_COMPLETED",
        resource=object_key,
        result="SUCCESS",
        trace_id=trace_id,
        details={
            "contentType": content_type,
            "objectSize": object_size,
            "validation": "object_exists_and_type_allowed"
        }
    )

    logger.info(json.dumps({
        "traceId": trace_id,
        "documentId": document_id,
        "stage": "preprocessing",
        "status": "preprocessing_completed",
        "bucket": bucket_name,
        "objectKey": object_key,
        "contentType": content_type,
        "objectSize": object_size
    }))


def lambda_handler(event, context):
    trace_id = getattr(context, "aws_request_id", "preprocess-trace")

    try:
        for sqs_record in event.get("Records", []):
            body = json.loads(sqs_record["body"])

            # S3 sends a test event when notification is configured.
            if body.get("Event") == "s3:TestEvent":
                logger.info(json.dumps({
                    "traceId": trace_id,
                    "stage": "preprocessing",
                    "status": "s3_test_event_received"
                }))
                continue

            for s3_record in body.get("Records", []):
                handle_s3_record(s3_record, trace_id)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Pre-processing event handled",
                "traceId": trace_id
            })
        }

    except Exception as error:
        logger.error(json.dumps({
            "traceId": trace_id,
            "stage": "preprocessing",
            "status": "failed",
            "errorType": type(error).__name__,
            "errorMessage": str(error)[:300]
        }))

        raise
