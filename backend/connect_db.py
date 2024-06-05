from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [ "localhost:5500", ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host = "localhost"
user = "root"
database = "co_so_du_lieu_xe_khach"
try:
    conn = mysql.connector.connect(
        host=host, user=user, database=database
    )
    cursor = conn.cursor()
    
except Exception as e:
    print(f"Lỗi: {e}")