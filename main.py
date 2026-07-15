from fastapi import FastAPI, File, UploadFile, Form,Depends
from sqlalchemy.orm import Session
import database

import shutil

app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/library/{user_name}")
def read_items(user_name: str):
    pass

@app.get("/library/pdf/{pdf_id}")
def read_item(pdf_id: int):
    pass

@app.post("/register")
def register(login:str, password:str):
    pass

@app.post("/upload-pdf/")
async def upload_pdf(
        user_id: str=Form(...),
        file: UploadFile=File(...),
        db: Session = Depends(database.get_db)
    ):
    path=f"pdf_files/{file.filename}"

    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    new_pdf=database.PDF(
        path=f"pdf_files/{file.filename}",
        title=file.filename,
        pages='0',#TEMPORARY
        user=user_id
    )

    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)

    return{"message ": f"{user_id}, {file.filename}, {file.content_type}, {file.size}"}

@app.delete("/delete/{pdf_id}")
def delete(pdf_id: int):
    pass

@app.put("/change-conf")
def change_conf():
    pass

@app.put("/log-in")
def log_in(login:str, password:str):
    pass