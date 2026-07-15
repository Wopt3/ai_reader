from fastapi import FastAPI
import database



app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/library/{user_name}")
def read_items(user_name: str):
    pass

@app.get("/library/pdf/{pdf_id")
def read_item(pdf_id: int):
    pass

@app.post("/register")
def register(login:str, password:str):
    pass

@app.post("/send-pdf/{pdf_id}")
async def send_pdf(pdf_id: int):
    pass

@app.delete("/delete/{pdf_id}")
def delete(pdf_id: int):
    pass

@app.put("/change-conf")
def change_conf():
    pass

@app.put("/log-in")
def log_in(login:str, password:str):
    pass