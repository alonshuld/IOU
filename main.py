from fastapi import FastAPI
from ioulist import IOUList

iou_db = IOUList()

app = FastAPI()

@app.get("/users")
def get_users():
    pass


@app.post("/add")
def create_user():
    pass


@app.post("/iou")
def create_iou():
    pass