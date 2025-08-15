#!/usr/bin/env python3
from flask import Flask, request, Response
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_SERVER = "192.168.100.2:8080"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Proxy requests to backend server"""
    
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logger.info(f"Request from {client_ip}: {request.method} {request.url}")
    
    target_url = f"http://{BACKEND_SERVER}/{path}"
    
    if request.query_string:
        target_url += f"?{request.query_string.decode()}"
    
    try:
        resp = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            timeout=10
        )
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                  if name.lower() not in excluded_headers]
        
        response = Response(resp.content, resp.status_code, headers)
        
        logger.info(f"Response to {client_ip}: {resp.status_code}")
        return response
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error proxying request: {e}")
        return f"Proxy Error: {str(e)}", 502

if __name__ == '__main__':
    print("Starting Reverse Proxy Server...")
    print(f"Forwarding requests to: {BACKEND_SERVER}")
    app.run(host='0.0.0.0', port=80, debug=False)