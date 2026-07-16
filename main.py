from fastapi import FastAPI, File, UploadFile, Form, Depends
from sqlalchemy.orm import Session
import database

import shutil
import os
import pdfPageCounter

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
    i:int = 0
    while True:
        path = f"pdf_files/{file.filename}_{i}"
        if os.path.exists(path):
            i+=1
        else:
            break
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    new_pdf=database.PDF(
        path=path,
        title=file.filename,
        pages=pdfPageCounter.get_pdf_page_count(path),
        user=user_id
    )

    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)

    return{"message": f"succes"}

@app.delete("/delete/{pdf_id}")
async def delete(pdf_id: int,
           db: Session = Depends(database.get_db)
    ):
    pdf = db.query(database.PDF).filter(database.PDF.id == pdf_id).first()
    if pdf:
        pdf_path = pdf.path
        db.delete(pdf)
        db.commit()
        try:
            os.remove(pdf_path)
        except:
            return {"message": "Error 404"}

        return {"status": "Success","message": "Deleted Successfully"}
    else:
        return {"status": "error", "message": "Pdf not found"}



@app.put("/change-conf")
def change_conf():
    pass

@app.put("/log-in")
def log_in(login:str, password:str):
    pass