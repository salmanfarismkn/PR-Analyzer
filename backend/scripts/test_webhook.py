import hashlib
import hmac
import json
import uuid

import requests


SECRET = "13579246810"

payload = {
    "action": "opened",
    "repository": {
        "id": 123456789,  # replace with your real repo GitHub ID
        "name": "event-checker",
        "full_name": "azuzm/event-checker",
        "owner": {
            "login": "azuzm"
        }
    },
    "pull_request": {
        "id": 999001,
        "number": 10,
        "title": "Webhook test PR",
        "state": "open",
        "author": "azuzm",                 # manually add
        "base_branch": "main",              # manually add
        "head_branch": "main",  # manually add
        "is_draft": False,                  # manually add
        "merged": False,
        "merged_at": None,
        "closed_at": None
    }
}


body = json.dumps(payload).encode("utf-8")

signature = (
    "sha256="
    + hmac.new(
        SECRET.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
)


delivery_id = f"test-delivery-{uuid.uuid4()}"

response = requests.post(
    "http://127.0.0.1:8000/webhooks/github",
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
        "X-GitHub-Delivery": delivery_id,
        "X-Hub-Signature-256": signature,
    },
)


print(response.status_code)

try:
    data = response.json()
    print("Parsed JSON:", data)
except ValueError:
    print("Response is not JSON. Status:", response.status_code)
    print("Raw text:", response.text)