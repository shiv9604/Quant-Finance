API_KEY = "TsjwX0WMQ4CtoNKECm3nNjk8aytodw"
API_SECRET = "RmFWLC9XHAoBx89xseayjkAPGx2ECokbPYNH3Q5gq6QGAY5yVSql0ZhJ3mv6"
BASE_URL = "https://api.delta.exchange"

def generate_signature(secret, method, path, timestamp, query_string="", body=""):
    message = method + timestamp + path + query_string + body
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

def private_request(method, path, query_params=None, body=None):

    timestamp = str(int(time.time()))
    query_string = ""

    if query_params:
        query_string = "?" + "&".join(
            f"{k}={v}" for k, v in query_params.items()
        )

    body_str = json.dumps(body) if body else ""

    signature = generate_signature(
        API_SECRET,
        method,
        path,
        timestamp,
        query_string,
        body_str
    )

    headers = {
        "api-key": API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    url = BASE_URL + path + query_string

    response = requests.request(
        method,
        url,
        headers=headers,
        data=body_str
    )

    return response.json()

# Example test: Get account details (private endpoint)
result = private_request("GET", "/v2/wallet/balances")
print(result)