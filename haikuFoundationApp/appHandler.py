from processRequestHandler import CONTROLLERS, FALLBACK
from utils.authorizer import parse_body, build_response, validate_jwt_token


def lambda_handler(event, context):
    print("EVENT:", event)
    http_method = (
        event.get("httpMethod", "")
        .upper()
    )
    if http_method == "OPTIONS":
      return build_response(200, {"message": "CORS preflight success"})
    body = parse_body(event)
    request_method = body.get("requestMethod")
    if not request_method:
      return build_response(400, {"error": "Missing requestMethod"})
    controller = CONTROLLERS.get(request_method, FALLBACK)
    handler = getattr(
        controller,
        http_method.lower(),
        None
    )
    if not handler:
      return build_response(405, {"error": f"{http_method} not supported for {request_method}"})
    user_claims = None
    if http_method in ("GET", "POST"):
      headers = event.get('headers', {}) or {}
      auth_header = headers.get('Authorization') or headers.get('authorization')
      try:
        user_claims = validate_jwt_token(auth_header)
      except Exception as e:
        return build_response(401, {"error": str(e)})
    controller_event = {
        "httpMethod": http_method,
        "route": request_method,
        "body": body,
        "headers": event.get("headers", {}),
      "user": user_claims or (
            event
            .get("requestContext", {})
            .get("authorizer")
        )
    }
    result = handler(controller_event)
    return build_response(200, result)
