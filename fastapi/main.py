import requests

from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

# origins = ["http://localhost"]
#
app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

REALM = 'MyRealm'
KEYCLOAK_BASEURL = f'https://proxy/auth/realms' \
                   f'/{REALM}/protocol/openid-connect'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=KEYCLOAK_BASEURL + '/token')


async def auth(token: str = Depends(oauth2_scheme)):
    headers = {'Authorization': 'bearer ' + token}
    r_user = requests.get(
        KEYCLOAK_BASEURL + '/userinfo',
        headers=headers,
        verify=False
    )
    if r_user.status_code == HTTP_200_OK:
        return r_user.json()
    elif r_user.status_code == HTTP_401_UNAUTHORIZED:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=r_user.json()
        )
    else:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Internal authentication error (our bad)'
        )


@app.get('/api/user/me')
async def hello_world(user: str = Depends(auth)):
    return user
