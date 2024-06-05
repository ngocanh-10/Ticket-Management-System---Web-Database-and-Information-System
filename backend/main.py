from fastapi import FastAPI
from connect_db import *
from user_api import *
from admin_api import *
from manager_api import *
import os
from login import *



app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend")), name="static")

@app.get("/")
async def readGuest(request: Request):
    return FileResponse(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend"), "home_guest.html"))

