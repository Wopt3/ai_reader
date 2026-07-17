from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import database

import shutil
import os
import pdfPageCounter
import PyPDF2

app = FastAPI()

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database.Base.metadata.create_all(bind=database.engine)

@app.get("/", response_class=HTMLResponse)
def read_root():
    static_file_path = os.path.join("static", "index.html")
    if os.path.exists(static_file_path):
        with open(static_file_path, "r", encoding="utf-8") as f:
            return f.read()
    return """
    <html>
        <head><title>AI Book Reader</title></head>
        <body style="font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #0f172a; color: #f8fafc;">
            <h1>AI Book Reader API</h1>
            <p>Frontend file <code>static/index.html</code> not found.</p>
        </body>
    </html>
    """

@app.get("/library/{user_name}")
def read_items(user_name: str, db: Session = Depends(database.get_db)):
    pdfs = db.query(database.PDF).filter(database.PDF.user == user_name).all()
    if not pdfs:
        return {"message": "No PDFs found for this user"}
    return pdfs

@app.get("/library/pdf/{pdf_id}")
def read_item(pdf_id: int, db: Session = Depends(database.get_db)):
    pdf = db.query(database.PDF).filter(database.PDF.id == pdf_id).first()
    if pdf is None:
        return {"message": "PDF not found"}
    return pdf

@app.get("/library/pdf/{pdf_id}/file")
def read_pdf_file(pdf_id: int, db: Session = Depends(database.get_db)):
    pdf = db.query(database.PDF).filter(database.PDF.id == pdf_id).first()
    if pdf is None:
        return {"error": "PDF not found"}
    if not os.path.exists(pdf.path):
        return {"error": f"File not found at path: {pdf.path}"}
    return FileResponse(pdf.path, media_type="application/pdf", filename=pdf.title)

@app.get("/library/pdf/{pdf_id}/text")
def read_pdf_text(pdf_id: int, db: Session = Depends(database.get_db)):
    pdf = db.query(database.PDF).filter(database.PDF.id == pdf_id).first()
    if pdf is None:
        return {"error": "PDF not found"}
    if not os.path.exists(pdf.path):
        return {"error": f"File not found at path: {pdf.path}"}
    
    try:
        pages_text = []
        with open(pdf.path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num in range(len(pdf_reader.pages)):
                text = pdf_reader.pages[page_num].extract_text() or ""
                pages_text.append({
                    "page": page_num + 1,
                    "text": text
                })
        return {
            "id": pdf.id,
            "title": pdf.title,
            "pages": pages_text
        }
    except Exception as e:
        return {"error": f"Failed to extract text: {str(e)}"}


    

@app.post("/register")
def register(user_data: database.UserRegister,
            db: Session = Depends(database.get_db)):
    existing_users_l = db.query(database.User).filter(database.User.login == user_data.login).first()
    existing_users_e = db.query(database.User).filter(database.User.email == user_data.email).first()
    if existing_users_l or existing_users_e:
        return{"message":"there is already user with this login or email, write again!"}
    new_user = database.User(
        login=user_data.login,
        password=user_data.password,
        email=user_data.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{"message": "User created correctly"}

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