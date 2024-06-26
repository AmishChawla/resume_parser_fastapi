from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile, Request, Path, Body, Query, Form, \
    APIRouter

import methods
from crud import email_templates_crud
from sqlalchemy.orm import Session, joinedload, selectinload
import models
from schemas import get_db
from methods import oauth2_scheme, get_user_from_token

email_template_router = APIRouter(prefix="/api/email-templates")


@email_template_router.post("/create-template")
def create_email_template(template: models.EmailTemplateCreate, token: str = Depends(oauth2_scheme),
                          db: Session = Depends(get_db)):
    user = get_user_from_token(token)
    if not methods.is_service_allowed(user_id=user.id):
        raise HTTPException(status_code=403, detail="User does not have access to this service")
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    email_template = email_templates_crud.create_email_template(template=template, db=db, user_id=user.id)
    return email_template


@email_template_router.get("/all")
def read_email_templates(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        templates = email_templates_crud.get_user_templates(user_id=user.id, db=db)
    return templates


@email_template_router.get("/{template_id}")
def read_email_templates(template_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        templates = email_templates_crud.get_user_templates_by_id(template_id=template_id, db=db)
    return templates


@email_template_router.put("/update-template/{template_id}")
def update_email_template(template_id: int, template: models.EmailTemplateCreate, db: Session = Depends(get_db),
                          token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not methods.is_service_allowed(user_id=user.id):
        raise HTTPException(status_code=403, detail="User does not have access to this service")
    else:
        new_template = email_templates_crud.update_email_template(template_id=template_id, template=template, db=db)
    return new_template


@email_template_router.delete("/delete-template/{template_id}")
def delete_email_template(template_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not methods.is_service_allowed(user_id=user.id):
        raise HTTPException(status_code=403, detail="User does not have access to this service")
    else:
        print('i am here')
        email_templates_crud.delete_email_template(template_id=template_id, db=db)
        print("i am here")

    return {"message": "Template deleted"}


@email_template_router.post("/send-mail")
def send_email(mail: models.Mail, token: str = Depends(oauth2_scheme),
               db: Session = Depends(get_db)):
    user = get_user_from_token(token)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not methods.is_service_allowed(user_id=user.id):
        raise HTTPException(status_code=403, detail="User does not have access to this service")

    methods.send_email(recipient_emails=[mail.to], message=mail.body, subject=mail.subject, role=user.role,
                       user_id=user.id)
    return "Mail Sent Successfully"
