import os
import json

import urllib.request
import urllib.error

def _fetch_json(url, timeout=10):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw)

def _post_json(url, data, timeout=10):
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = raw
        return resp.getcode(), parsed

def lambda_handler(event, context):
    api_path = os.environ.get("API_PATH")
    ms_path = os.environ.get("MS_PATH")

    if not api_path or not ms_path:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "API_PATH y MS_PATH deben estar definidas en las variables de entorno"})
        }

    try:
        source_data = _fetch_json(api_path)
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = ""
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "GET desde API_PATH falló", "http_code": e.code, "details": err_body})
        }
    except urllib.error.URLError as e:
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "GET desde API_PATH falló", "details": str(e)})
        }
    except ValueError as e:
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "JSON inválido recibido desde API_PATH", "details": str(e)})
        }

    try:
        ms_status, ms_response = _post_json(ms_path, source_data)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "success", "ms_status": ms_status, "ms_response": ms_response})
        }
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            err_body = ""
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "La publicación a MS_PATH falló", "http_code": e.code, "details": err_body})
        }
    except urllib.error.URLError as e:
        return {
            "statusCode": 502,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "La publicación a MS_PATH falló", "details": str(e)})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"status": "error", "message": "Error inesperado", "details": str(e)})
        }