import os
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional, List

from app.routers.photo_router import photo_router


class FileSystemStorage:
    def __init__(self, path: str, allow_extensions: Optional[List[str]] = None, max_size: int = 1024 ** 3):
        self.max_size = max_size
        self.allow_extensions = allow_extensions
        self.path = path
        os.makedirs(self.path, exist_ok=True)  # Создаем директорию, если она не существует

    async def upload(self, file: UploadFile):
        filename = file.filename
        content = await file.read()

        file_size = len(content)
        if file_size > self.max_size:
            raise HTTPException(status_code=400, detail=f"Размер файла {file_size} превышает максимальный размер {self.max_size}")

        if self.allow_extensions:
            if not any(filename.endswith(ext) for ext in self.allow_extensions):
                raise HTTPException(status_code=400,
                                    detail=f"Расширение файла недопустимо. Допустимые: {self.allow_extensions}")

        file_path = os.path.join(self.path, filename)
        with open(file_path, "wb") as f:
            f.write(content)

        return filename


# Инициализация хранилищ для файлов и фотографий
storageF = FileSystemStorage(path="static/file", allow_extensions=['.pdf', '.docx', '.txt'])
storageI = FileSystemStorage(path="static/photo", allow_extensions=['.jpg', '.png', '.gif'])

# file = Column(FileType(storage=storageF))

# Эндпоинт для загрузки файла
@photo_router.post("/upload_file")
async def upload_file(file: UploadFile):
    filename = await storageF.upload(file)
    return {"filename": filename}


# Эндпоинт для загрузки фотографии
@photo_router.post("/upload_photo")
async def upload_photo(file: UploadFile):
    filename = await storageI.upload(file)
    return {"filename": filename}


# Эндпоинт для получения загруженного файла
@photo_router.get("/files/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("static/file", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(file_path)


# Эндпоинт для получения загруженной фотографии
@photo_router.get("/photos/{filename}")
async def get_photo(filename: str):
    file_path = os.path.join("static/photo", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Фото не найдено")

    return FileResponse(file_path)

