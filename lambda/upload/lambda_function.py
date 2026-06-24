import json 

import uuid 

import re 

from datetime import datetime 

  

  

ALLOWED_CONTENT_TYPES = { 

    "application/pdf", 

    "image/jpeg", 

    "image/png" 

} 

  

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB 

  

  

def response(status_code, body): 

    return { 

        "statusCode": status_code, 

        "headers": { 

            "Content-Type": "application/json", 

            "Access-Control-Allow-Origin": "*", 

            "Access-Control-Allow-Headers": "Content-Type,Authorization", 

            "Access-Control-Allow-Methods": "POST,OPTIONS" 

        }, 

        "body": json.dumps(body) 

    } 

  

  

def lambda_handler(event, context): 

    try: 

        raw_body = event.get("body") 

  

        if raw_body is None: 

            body = event 

        elif isinstance(raw_body, str): 

            body = json.loads(raw_body) 

        else: 

            body = raw_body 

  

        file_name = body.get("fileName") 

        content_type = body.get("contentType") 

        file_size = body.get("fileSizeBytes") 

  

        if not file_name: 

            return response(400, { 

                "message": "Missing required field: fileName" 

            }) 

  

        if not content_type: 

            return response(400, { 

                "message": "Missing required field: contentType" 

            }) 

  

        if file_size is None: 

            return response(400, { 

                "message": "Missing required field: fileSizeBytes" 

            }) 

  

        if content_type not in ALLOWED_CONTENT_TYPES: 

            return response(415, { 

                "message": "Unsupported file type", 

                "allowedTypes": list(ALLOWED_CONTENT_TYPES) 

            }) 

  

        if int(file_size) > MAX_FILE_SIZE_BYTES: 

            return response(413, { 

                "message": "File size exceeds allowed limit", 

                "maxFileSizeBytes": MAX_FILE_SIZE_BYTES 

            }) 

  

        if not re.match(r"^[a-zA-Z0-9._-]+$", file_name): 

            return response(400, { 

                "message": "Invalid file name. Use only letters, numbers, dots, underscores, and hyphens." 

            }) 

  

        job_id = str(uuid.uuid4()) 

  

        result = { 

            "message": "Document upload request accepted", 

            "jobId": job_id, 

            "fileName": file_name, 

            "contentType": content_type, 

            "fileSizeBytes": file_size, 

            "status": "received", 

            "receivedAt": datetime.utcnow().isoformat() + "Z" 

        } 

  

        return response(201, result) 

  

    except json.JSONDecodeError: 

        return response(400, { 

            "message": "Invalid JSON body" 

        }) 

  

    except Exception as error: 

        return response(500, { 

            "message": "Internal server error", 

            "error": str(error) 

        }) 
