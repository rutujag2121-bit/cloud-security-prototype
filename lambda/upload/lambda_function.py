import json
import os
import re
import uuid
import logging
from datetime import datetime, timezone

import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")

BUCKET_NAME = os.environ["BUCKET_NAME"]
UPLOAD_PREFIX = os.environ.get("UPLOAD_PREFIX", "raw")
MAX_FILE_SIZE_BYTES = int(os.environ.get("MAX_FILE_SIZE_BYTES", "10485760"))
PRESIGNED_URL_EXPIRES_SECONDS = int(os.environ.get("PRESIGNED_URL_EXPIRES_SECONDS", "900"))

ALLOWED_TYPES = {
    "application/pdf": [".pdf"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"]
}


def get_allowed_origins():
    raw = os.environ.get("ALLOWED_ORIGINS", "")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


def cors_headers(event):
    allowed_origins = get_allowed_origins()
    headers = event.get("headers") or {}
    request_origin = headers.get("origin") or headers.get("Origin")

    if request_origin in allowed_origins:
        origin = request_origin
    elif allowed_origins:
        origin = allowed_origins[0]
    else:
        origin = "http://localhost:3000"

    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Headers": "Content-Type,Authorization",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }


def response(event, status_code, body):
    return {
        "statusCode": status_code,
        "headers": cors_headers(event),
        "body": json.dumps(body)
    }


def sanitize_filename(file_name):
    file_name = str(file_name).strip()
    file_name = file_name.split("/")[-1].split("\\")[-1]
    file_name = re.sub(r"[^A-Za-z0-9._-]", "_", file_name)
    return file_name[:120]


def validate_request(body):
    required_fields = ["fileName", "contentType", "fileSizeBytes"]

    for field in required_fields:
        if field not in body:
            return False, f"Missing required field: {field}"

    file_name = str(body["fileName"]).strip()
    content_type = str(body["contentType"]).strip()

    if not file_name:
        return False, "fileName cannot be empty"

    if content_type not in ALLOWED_TYPES:
        return False, "Unsupported contentType. Allowed types are PDF, JPG, JPEG, PNG"

    try:
        file_size = int(body["fileSizeBytes"])
    except (TypeError, ValueError):
        return False, "fileSizeBytes must be an integer"

    if file_size <= 0:
        return False, "fileSizeBytes must be greater than zero"

    if file_size > MAX_FILE_SIZE_BYTES:
        return False, "File exceeds maximum allowed size of 10 MB"

    lower_name = file_name.lower()
    valid_extension = any(
        lower_name.endswith(ext)
        for ext in ALLOWED_TYPES[content_type]
    )

    if not valid_extension:
        return False, "File extension does not match contentType"

    return True, None


def lambda_handler(event, context):
    trace_id = getattr(context, "aws_request_id", str(uuid.uuid4()))

    if event.get("httpMethod") == "OPTIONS":
        return response(event, 200, {"message": "CORS preflight ok"})

    try:
        raw_body = event.get("body")

        if raw_body is None:
            body = event
        elif isinstance(raw_body, str):
            body = json.loads(raw_body)
        else:
            body = raw_body

    except json.JSONDecodeError:
        return response(event, 400, {"error": "Invalid JSON body"})

    is_valid, error_message = validate_request(body)

    if not is_valid:
        logger.warning(json.dumps({
            "traceId": trace_id,
            "stage": "upload_initiate",
            "status": "rejected",
            "reason": error_message
        }))

        return response(event, 400, {"error": error_message})

    safe_file_name = sanitize_filename(body["fileName"])
    content_type = body["contentType"]
    file_size = int(body["fileSizeBytes"])

    # Temporary placeholders until Supabase Auth is connected.
    # Later these values should come from a verified JWT.
    user_id = str(body.get("userId", "anonymous"))
    company_id = str(body.get("companyId", "default-company"))

    document_id = str(uuid.uuid4())
    object_key = f"{UPLOAD_PREFIX}/{company_id}/{user_id}/{document_id}/{safe_file_name}"

    try:
        upload_url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type
            },
            ExpiresIn=PRESIGNED_URL_EXPIRES_SECONDS,
            HttpMethod="PUT"
        )

        created_at = datetime.now(timezone.utc).isoformat()

        logger.info(json.dumps({
            "traceId": trace_id,
            "documentId": document_id,
            "stage": "upload_initiate",
            "status": "upload_url_created",
            "contentType": content_type,
            "fileSizeBytes": file_size,
            "objectKey": object_key,
            "createdAt": created_at
        }))

        return response(event, 201, {
            "message": "Secure upload URL created",
            "documentId": document_id,
            "jobId": document_id,
            "status": "upload_url_created",
            "bucket": BUCKET_NAME,
            "objectKey": object_key,
            "uploadUrl": upload_url,
            "uploadMethod": "PUT",
            "requiredHeaders": {
                "Content-Type": content_type
            },
            "expiresInSeconds": PRESIGNED_URL_EXPIRES_SECONDS,
            "traceId": trace_id,
            "createdAt": created_at
        })

    except Exception as error:
        logger.error(json.dumps({
            "traceId": trace_id,
            "stage": "upload_initiate",
            "status": "failed",
            "errorType": type(error).__name__
        }))

        return response(event, 500, {
            "error": "Internal server error while creating upload URL",
            "traceId": trace_id
        })

