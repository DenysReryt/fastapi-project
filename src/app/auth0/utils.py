import http.client
import jwt
from datetime import datetime, timedelta
from src.app.config import settings
from fastapi import Response, Depends, HTTPException
from fastapi.security import HTTPBearer
from src.app.user_crud import crud

token_auth_scheme = HTTPBearer()


def auth_request(config, user):
    conn = http.client.HTTPSConnection(config['DOMAIN'])
    pyload = "{" \
             f"\"client_id\":\"{config['CLIENT_ID']}\"," \
             f"\"client_secret\":\"{config['CLIENT_SECRET']}\"," \
             f"\"audience\":\"{config['API_AUDIENCE']}\"," \
             f"\"email\":\"{user.email}\"," \
             f"\"password\":\"{user.password}\"," \
             f"\"connection\":\"{config['CONNECTION']}\"," \
             f"\"grant_type\":\"client_credentials\"" \
             "}"
    headers = {"content-type": "application/json"}
    conn.request("POST", "/dbconnections/signup", pyload, headers)
    conn.getresponse()


async def get_email_from_token(response: Response, token: str = Depends(token_auth_scheme)):
    if jwt.get_unverified_header(token.credentials).get('alg') == 'RS256':
        pyload_from_auth = VerifyToken(token.credentials).verify()
        return pyload_from_auth.get("email")
    else:
        pyload_from_me = VerifyToken(token.credentials).verify_my()
        return pyload_from_me.get("email")


async def create_access_token(email: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "email": email}
    config = set_up()
    encoded_jwt = jwt.encode(to_encode, config["SECRET"], algorithm=config["MY_ALGORITHMS"])
    return encoded_jwt


async def get_current_user(response: Response, token: str = Depends(token_auth_scheme)):
    if jwt.get_unverified_header(token.credentials).get('alg') == 'RS256':
        pyload_from_auth = VerifyToken(token.credentials).verify()
        user = await crud.get_user_by_email(email=pyload_from_auth.get("email"))
        if not user:
            user = await crud.create_user_by_email(email=pyload_from_auth.get("email"))
        return user
    else:
        pyload_from_me = VerifyToken(token.credentials).verify_my()
        user = await crud.get_user_by_email(email=pyload_from_me.get("email"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


def set_up():
    config = {
        "CLIENT_ID": settings.CLIENT_ID,
        "CLIENT_SECRET": settings.CLIENT_SECRET,
        "DOMAIN": settings.DOMAIN,
        "API_AUDIENCE": settings.API_AUDIENCE,
        "ISSUER": settings.ISSUER,
        "ALGORITHMS": settings.ALGORITHMS,
        "MY_ALGORITHMS": settings.MY_ALGORITHMS,
        "SECRET": settings.SECRET,
        "CONNECTION": settings.CONNECTION
    }
    return config


class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token, permissions=None, scopes=None):
        self.token = token
        self.permissions = permissions
        self.scopes = scopes
        self.config = set_up()

        # This gets the JWKS from a given URL and does processing so you can use any of
        # the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            raise HTTPException(status_code=400, detail=str(error))
        except jwt.exceptions.DecodeError as error:
            raise HTTPException(status_code=400, detail=str(error))

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        if self.scopes:
            result = self._check_claims(payload, 'scope', str, self.scopes.split(' '))
            if result.get("error"):
                return result

        if self.permissions:
            result = self._check_claims(payload, 'permissions', list, self.permissions)
            if result.get("error"):
                return result

        return payload

    def verify_my(self):
        try:
            payload = jwt.decode(
                self.token,
                self.config["SECRET"],
                algorithms=[self.config["MY_ALGORITHMS"]],
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return payload

    def _check_claims(self, payload, claim_name, claim_type, expected_value):

        instance_check = isinstance(payload[claim_name], claim_type)
        result = {"status": "success", "status_code": 200}

        payload_claim = payload[claim_name]

        if claim_name not in payload or not instance_check:
            result["status"] = "error"
            result["status_code"] = 400

            result["code"] = f"missing_{claim_name}"
            result["msg"] = f"No claim '{claim_name}' found in token."
            return result

        if claim_name == 'scope':
            payload_claim = payload[claim_name].split(' ')

        for value in expected_value:
            if value not in payload_claim:
                result["status"] = "error"
                result["status_code"] = 403

                result["code"] = f"insufficient_{claim_name}"
                result["msg"] = (f"Insufficient {claim_name} ({value}). You don't have "
                                 "access to this resource")
                return result
        return result
