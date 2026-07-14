import json
import os
import uuid
import logging
import urllib.request
import urllib.error
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")

if SUPABASE_URL.endswith("/rest/v1"):
    SUPABASE_URL = SUPABASE_URL.replace("/rest/v1", "")

SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", "0.85"))


def now_iso():
    return datetime.now(timezone.utc).isoformat()


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

    if method in ["POST", "PATCH"]:
        request.add_header("Prefer", "return=minimal")

    try:
        with urllib.request.urlopen(request, timeout=8) as result:
            if result.status < 200 or result.status >= 300:
                raise RuntimeError(f"Supabase request failed with status {result.status}")

    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase request failed for {table_name}: {error.code} {error_body[:500]}"
        )

    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Supabase connection failed for {table_name}: {str(error.reason)}"
        )


def update_document_status(document_id, status, trace_id):
    payload = {
        "status": status,
        "trace_id": trace_id,
        "updated_at": now_iso()
    }

    supabase_request(
        method="PATCH",
        table_name="documents",
        payload=payload,
        query_string=f"?id=eq.{document_id}"
    )


def insert_audit_log(document_id, user_id, company_id, action, resource, result, trace_id, details):
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


def insert_processing_run(run_id, document_id, object_key, trace_id):
    payload = {
        "id": run_id,
        "document_id": document_id,
        "provider": "mock",
        "model_name": "mock-receipt-extractor",
        "model_version": "v1",
        "processing_method": "mock",
        "input_s3_object_key": object_key,
        "status": "started",
        "started_at": now_iso(),
        "trace_id": trace_id
    }

    supabase_request(
        method="POST",
        table_name="processing_runs",
        payload=payload
    )


def complete_processing_run(run_id, duration_ms, trace_id):
    payload = {
        "status": "completed",
        "completed_at": now_iso(),
        "duration_ms": duration_ms,
        "trace_id": trace_id
    }

    supabase_request(
        method="PATCH",
        table_name="processing_runs",
        payload=payload,
        query_string=f"?id=eq.{run_id}"
    )


def fail_processing_run(run_id, error_message, trace_id):
    payload = {
        "status": "failed",
        "completed_at": now_iso(),
        "trace_id": trace_id,
        "error_message": error_message[:500]
    }

    supabase_request(
        method="PATCH",
        table_name="processing_runs",
        payload=payload,
        query_string=f"?id=eq.{run_id}"
    )


def create_mock_extraction(message):
    file_name = message.get("objectKey", "").split("/")[-1]

    extracted_json = {
        "supplier_name": "Mock Supplier Ltd",
        "document_date": "2026-07-13",
        "document_time": None,
        "currency": "EUR",
        "total_amount": 42.50,
        "document_category": "receipt",
        "line_items": [
            {
                "description": "Mock item",
                "quantity": 1,
                "unit_price": 42.50,
                "amount": 42.50
            }
        ],
        "source_file": file_name,
        "extraction_mode": "mock"
    }

    field_confidence = {
        "supplier_name": 0.92,
        "document_date": 0.90,
        "currency": 0.95,
        "total_amount": 0.91,
        "line_items": 0.80
    }

    confidence_values = list(field_confidence.values())
    confidence_overall = sum(confidence_values) / len(confidence_values)

    return extracted_json, field_confidence, round(confidence_overall, 3)


def insert_extraction_result(
    document_id,
    processing_run_id,
    extracted_json,
    field_confidence,
    confidence_overall,
    needs_human_review
):
    payload = {
        "document_id": document_id,
        "processing_run_id": processing_run_id,
        "extracted_json": extracted_json,
        "supplier_name": extracted_json.get("supplier_name"),
        "document_date": extracted_json.get("document_date"),
        "currency": extracted_json.get("currency"),
        "total_amount": extracted_json.get("total_amount"),
        "confidence_overall": confidence_overall,
        "field_confidence": field_confidence,
        "needs_human_review": needs_human_review
    }

    supabase_request(
        method="POST",
        table_name="extraction_results",
        payload=payload
    )


def handle_extraction_message(message, lambda_trace_id):
    start_time = datetime.now(timezone.utc)

    document_id = message["documentId"]
    user_id = message.get("userId", "unknown")
    company_id = message.get("companyId", "unknown")
    object_key = message["objectKey"]
    trace_id = message.get("traceId", lambda_trace_id)

    processing_run_id = str(uuid.uuid4())

    try:
        update_document_status(document_id, "ocr_started", trace_id)

        insert_audit_log(
            document_id=document_id,
            user_id=user_id,
            company_id=company_id,
            action="EXTRACTION_STARTED",
            resource=object_key,
            result="SUCCESS",
            trace_id=trace_id,
            details={
                "provider": "mock",
                "modelName": "mock-receipt-extractor",
                "processingRunId": processing_run_id
            }
        )

        insert_processing_run(
            run_id=processing_run_id,
            document_id=document_id,
            object_key=object_key,
            trace_id=trace_id
        )

        extracted_json, field_confidence, confidence_overall = create_mock_extraction(message)

        needs_human_review = confidence_overall < CONFIDENCE_THRESHOLD

        insert_extraction_result(
            document_id=document_id,
            processing_run_id=processing_run_id,
            extracted_json=extracted_json,
            field_confidence=field_confidence,
            confidence_overall=confidence_overall,
            needs_human_review=needs_human_review
        )

        end_time = datetime.now(timezone.utc)
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        complete_processing_run(
            run_id=processing_run_id,
            duration_ms=duration_ms,
            trace_id=trace_id
        )

        final_status = "needs_human_review" if needs_human_review else "ocr_completed"

        update_document_status(document_id, final_status, trace_id)

        insert_audit_log(
            document_id=document_id,
            user_id=user_id,
            company_id=company_id,
            action="EXTRACTION_COMPLETED",
            resource=object_key,
            result="SUCCESS",
            trace_id=trace_id,
            details={
                "provider": "mock",
                "modelName": "mock-receipt-extractor",
                "processingRunId": processing_run_id,
                "confidenceOverall": confidence_overall,
                "confidenceThreshold": CONFIDENCE_THRESHOLD,
                "needsHumanReview": needs_human_review,
                "finalStatus": final_status
            }
        )

        logger.info(json.dumps({
            "traceId": trace_id,
            "documentId": document_id,
            "processingRunId": processing_run_id,
            "stage": "extraction",
            "status": final_status,
            "confidenceOverall": confidence_overall,
            "needsHumanReview": needs_human_review,
            "durationMs": duration_ms
        }))

    except Exception as error:
        try:
            fail_processing_run(
                run_id=processing_run_id,
                error_message=str(error),
                trace_id=trace_id
            )
        except Exception:
            pass

        update_document_status(document_id, "failed", trace_id)

        insert_audit_log(
            document_id=document_id,
            user_id=user_id,
            company_id=company_id,
            action="EXTRACTION_FAILED",
            resource=object_key,
            result="FAILED",
            trace_id=trace_id,
            details={
                "errorType": type(error).__name__,
                "errorMessage": str(error)[:300]
            }
        )

        raise


def lambda_handler(event, context):
    lambda_trace_id = getattr(context, "aws_request_id", "extraction-trace")

    try:
        for sqs_record in event.get("Records", []):
            message = json.loads(sqs_record["body"])
            handle_extraction_message(message, lambda_trace_id)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Extraction event handled",
                "traceId": lambda_trace_id
            })
        }

    except Exception as error:
        logger.error(json.dumps({
            "traceId": lambda_trace_id,
            "stage": "extraction",
            "status": "failed",
            "errorType": type(error).__name__,
            "errorMessage": str(error)[:300]
        }))

        raise
