import os
import json
import random
import string
import datetime
import azure.functions as func

def create_random_device():
    id_chars = string.ascii_lowercase + string.digits
    device_id = "".join(random.choices(id_chars, k=10))
    last_seen = str(datetime.datetime.now().timestamp())
    data = {"temp": round(random.uniform(-10, 50), 2)}
    return {"id": device_id, "last_seen": last_seen, "data": data}

def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    
    if not req_body:
        return func.HttpResponse("Invalid request.", status_code=400)
    
    operation = req_body.get("operation")
    
    if operation == "create_device":
        device = create_random_device()
        return func.HttpResponse(json.dumps(device), mimetype="application/json")
    
    elif operation == "report_data":
        device_id = req_body.get("device_id")
        data = req_body.get("data")
        
        conn_string = os.environ["IOTHUB_CONNECTION_STRING"]
        iothub_service_sdk = IoTHubServiceClientFromConnectionString(conn_string)
        
        message = Message(json.dumps(data))
        iothub_service_sdk.send_message_async(device_id, message)
        
        return func.HttpResponse("Message sent.", status_code=200)
    
    else:
        return func.HttpResponse("Invalid operation.", status_code=400)