import datetime
import math
from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Request, Form
from sqlalchemy.exc import IntegrityError
import constants
from databases import Database
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
import methods
import models
import schemas
from routes import auth_routes, cms_routes, services_routes, companies_routes, settings_routes, user_management_routes, resumer_parser_routes
from schemas import User, ResumeData, get_db, SessionLocal, Service, UserServices, Company
from models import UserResponse, UserCreate, TokenData, UserFiles, AdminInfo
from constants import DATABASE_URL, ACCESS_TOKEN_EXPIRE_MINUTES
from methods import get_password_hash, verify_password, get_current_user, oauth2_scheme, \
    get_user_from_token
from sqlalchemy import update
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import stripe
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Initialize FastAPI and database
app = FastAPI(
    docs_url="/docs",
    openapi_url='/openapi.json',
    debug=True
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/profile_pictures", StaticFiles(directory="profile_pictures"), name="profile_pictures")
templates = Jinja2Templates(directory="templates")

#Routes
app.include_router(auth_routes.auth_router)
app.include_router(services_routes.services_router)
app.include_router(companies_routes.company_router)
app.include_router(settings_routes.email_settings_router)
app.include_router(settings_routes.plan_settings_router)
app.include_router(settings_routes.subscription_router)
app.include_router(user_management_routes.user_management_router)
app.include_router(resumer_parser_routes.resume_parser_router)
app.include_router(cms_routes.cms_router)


stripe.api_key = constants.STRIPE_API_KEY

@app.on_event("startup")
async def startup():
    redis_url = "redis://localhost"
    FastAPICache.init(RedisBackend(redis_url), prefix="fastapi-cache")


# database = Database(DATABASE_URL)
#
#
# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        name="index.html", request=request)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
