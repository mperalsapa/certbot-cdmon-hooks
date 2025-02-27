#!/usr/bin/python3
import http.client
import os
import sys
import json
import time

def CallApi(endpoint, body, headers = {}, method = "GET"):
    conn = http.client.HTTPSConnection(CDMON_API_DOMAIN)
    base_headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'apikey': CDMON_API_KEY,
    }
    headers = {**base_headers, **headers}
    conn.request(
        method,
        endpoint,
        headers=headers
    )
    return json.loads(conn.getresponse().read())

def CreateRecord(value):
    api_req_body = {
        "data": {
            "domain": CERTBOT_DOMAIN,
            "type": "txt",
            "ttl": 10,
            "host": "_acme-challenge",
            "value": value

        }
    }
    api_response = CallApi("/dnsrecords/create", api_req_body, method="POST")

    if api_response["status"] == "ok":
        time.sleep(5)
        return api_response["data"]
    else:
        print(f"ERROR: {api_response["data"]}")
        exit(1)
        return None


def GetRecord():
    if not record:
        return None
    api_req_body = {"data": {"domain": record}}
    api_response = CallApi("/getDnsRecords", api_req_body, method="POST")
    
    if api_response["status"] == "ok":
        return api_response["data"]["result"]
    else:
        print(f"ERROR: {api_response["data"]}")
        return None

def EditRecord(new_value):
    api_req_body = {
        "data": {
            "domain": CERTBOT_DOMAIN,
            "current": {
                "host": "_acme-challenge",
                "type": "txt"
            }, 
            "new": {
                "ttl": 10,
                "value": new_value
            }
        }
    }
    api_response = CallApi("/dnsrecords/edit", api_req_body, method="POST")
    
    if api_response["status"] == "ok":
        return api_response["data"]
    else:
        print(f"ERROR: {api_response["data"]}")
        return None

def UpdateWorkflow():
    if len(currentRecords) > 0:
        print("Record exists, editing record value...")
        editResponse = EditRecord(CERTBOT_VALIDATION)
        print(editResponse)
            
    else:
        print("Record does not exists, creating...")
        createResponse = CreateRecord(CERTBOT_VALIDATION)
        print(createResponse)

def CleanupWorkflow():
    print("Erasing record")
    

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Script usage: cdmon-updater.py <ACTION>")
        exit(1)
    
    REQUESTED_ACTION=sys.argv[1] if sys.argv[1].lower() in ["update", "cleanup"] else None

    CERTBOT_DOMAIN=os.getenv("CERTBOT_DOMAIN", "")
    CERTBOT_VALIDATION=os.getenv("CERTBOT_VALIDATION", "")
    CERTBOT_REMAINING_CHALLENGES=os.getenv("CERTBOT_REMAINING_CHALLENGES", "")
    CERTBOT_ALL_DOMAINS=os.getenv("CERTBOT_ALL_DOMAINS", "")

    CDMON_API_KEY = "API_KEY"
    CDMON_API_DOMAIN = "private-anon-9b9717fcc3-apidedominios.apiary-mock.com"
    
    if not REQUESTED_ACTION:
        print("Usage parameter is not correct. Use 'update' or 'cleanup'")
        exit(1)    

    if not CERTBOT_DOMAIN or not CERTBOT_VALIDATION or not CERTBOT_REMAINING_CHALLENGES or not CERTBOT_ALL_DOMAINS:
        print("""Missing any of the following env variables:\n\t- CERTBOT_DOMAIN\n\t- CERTBOT_VALIDATION\n\t- CERTBOT_REMAINING_CHALLENGES\n\t- CERTBOT_ALL_DOMAINS""")
        exit(1)

    currentRecords = GetRecord("_acme-challenge" + CERTBOT_DOMAIN)
    if not currentRecords:
        quit()

    if REQUESTED_ACTION == "update":
        UpdateWorkflow()
    else:
        CleanupWorkflow()
    