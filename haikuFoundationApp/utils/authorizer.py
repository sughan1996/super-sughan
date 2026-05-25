import json
import ssl
from urllib.request import urlopen

import certifi
from jose import jwt, ExpiredSignatureError, JWTError
from jose.exceptions import JWTClaimsError

AWS_REGION = "us-east-1"
COGNITO_USER_POOL_ID = "us-east-1_1pgqSzf45"
COGNITO_CLIENT_ID = "3q34c48o6fvaqbdmssvuovu86k"
JWKS_CACHE = {"jwks": None}


def get_jwks(jwks_url: str) -> dict:
  if JWKS_CACHE["jwks"] is None:
    # Use certifi CA bundle to avoid local trust store issues
    context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(jwks_url, context=context) as resp:
      JWKS_CACHE["jwks"] = json.load(resp)
  return JWKS_CACHE["jwks"]


def validate_jwt_token(auth_header: str) -> dict:
  """
  Validate JWT token from Authorization header.
  Returns decoded token claims if valid.
  Raises Exception if invalid.
  """
  if not auth_header or not auth_header.startswith('Bearer '):
    raise Exception('Missing or invalid Authorization header')

  token = auth_header.split(' ')[1]

  region = AWS_REGION
  user_pool_id = COGNITO_USER_POOL_ID
  client_id = COGNITO_CLIENT_ID
  if not user_pool_id or not client_id:
    raise Exception('Missing Cognito configuration')

  issuer = f'https://cognito-idp.{region}.amazonaws.com/{user_pool_id}'
  jwks_url = f'{issuer}/.well-known/jwks.json'

  jwks = get_jwks(jwks_url)

  try:
    # Select the correct key from JWKS using token header kid
    headers = jwt.get_unverified_header(token)
    kid = headers.get('kid')
    if not kid:
      raise Exception('Missing kid in token header')
    key = next((k for k in jwks.get('keys', []) if k.get('kid') == kid), None)
    if not key:
      raise Exception('Unable to find matching JWK for token')
    claims = jwt.decode(
      token,
      key,
      algorithms=['RS256'],
      options={
        'verify_aud': False,  # handle aud/client_id manually below
        'verify_at_hash': False
      },
      issuer=issuer
    )

    # Validate client id. For id/access tokens, the field can be 'aud' or 'client_id'
    token_client_id = claims.get('aud') or claims.get('client_id')
    if token_client_id != client_id:
      raise JWTClaimsError('Invalid client_id')
    return claims
  except ExpiredSignatureError:
    raise Exception('Token expired')
  except (JWTClaimsError, JWTError) as e:
    raise Exception(f'Invalid token: {str(e)}')
