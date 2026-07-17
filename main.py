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
def read_items(user_name: str, db: Session = Depends(database.get_db)):
    pdfs = db.query(database.PDF).filter(database.PDF.user == user_name).all()
    if not pdfs:
        return {"message": "No PDFs found for this user"}
    
    return pdfs

@app.get("/library/pdf/{pdf_id}")
def read_item(pdf_id: int, db: Session = Depends(database.get_db)):
        pdf = db.query(database.PDF).filter(database.PDF.id == pdf_id).first()
        if not pdf:
            return {"message": "No PDFs found for this user"}
        return pdf

    

@app.post("/register")
def register(login:str, password:str,email:str, db: Session = Depends(database.get_db)):
    existing_users_l = db.query(database.User).filter(database.User.login == login).first()
    existing_users_e = db.query(database.User).filter(database.User.email == email).first()
    if existing_users_l or existing_users_e:
        return{"message":"there is already user with this login or email, write again!"}
    new_user = database.User(
        login=login,
        password=password,
        email=email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message": "User vreated correctly"}

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
    os.makedirs(os.path.dirname(path), exist_ok=True)
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