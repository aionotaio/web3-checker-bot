from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from services.auth import get_current_admin
from shared.vars import TEMPLATES_DIR


router = APIRouter()
templates = Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", include_in_schema=False, dependencies=[Depends(get_current_admin)])
async def redirect_to(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/login", include_in_schema=False)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/dashboard", include_in_schema=False, dependencies=[Depends(get_current_admin)])
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
