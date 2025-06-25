from fastapi import APIRouter, status, Response

from services.auth import create_access_token, authn_admin
from shared.schemas import Token, ResponseMsg, AdminAuth


router = APIRouter(prefix="/api/auth")


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": Token},
        status.HTTP_401_UNAUTHORIZED: {"model": ResponseMsg},
        status.HTTP_404_NOT_FOUND: {"model": ResponseMsg},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ResponseMsg},
    },
)
async def login(response: Response, form_data: AdminAuth) -> Token:
    await authn_admin(form_data.username, form_data.password)

    token = create_access_token({"sub": form_data.username})
    response.set_cookie(key="access_token", value=token, httponly=True)
    return Token(access_token=token)


@router.post("/logout")
async def logout_user(response: Response) -> ResponseMsg:
    response.delete_cookie(key="access_token")
    return ResponseMsg(detail="Successfully logged out!")
