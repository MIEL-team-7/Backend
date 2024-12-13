import os
from typing import BinaryIO

from fastapi import UploadFile
from sqladmin import Admin, ModelView
from sqlalchemy import Column, Integer
from sqlalchemy.orm import Session
from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import FileType, ImageType

from app.core.db import engine, Base, AsyncSessionFactory
from app.main import app
from app.models.models import BaseUser

'''

storageF = FileSystemStorage(path="/static/file")
storageI = FileSystemStorage(path="/static/image")

# Проверяем, существует ли директория
if not os.path.exists(storageF):
    os.makedirs(storageF)  # Создаем директорию, если она не существует

if not os.path.exists(storageI):
    os.makedirs(storageI)



class User(BaseUser):
    __tablename__ = "users"

    file = Column(FileType(storage=storageF))
    photo = Column(ImageType(storage=storageI))

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.file, User.photo]


Base.metadata.create_all(engine)  # Create tables


@app.post("/upload/")
def create_upload_file(file: UploadFile):
    user = User(file=file)
    with AsyncSessionFactory.engine as session:
        session.add(user)
        session.commit()
        return {"filename": user.file.name}

'''
