from fastapi import FastAPI, Form, HTTPException
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
from connect_db import *


templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Mô hình dữ liệu người dùng
class Customer(BaseModel):
    id: int
    userName: str
    email: str
    phone: int
    bankAccount: str
    password: str

class Admin(BaseModel):
    id: int
    userName: str
    email: str
    phone: int
    password: str

class Manager(BaseModel):
    id: int
    userName: str
    email: str
    phone: int
    password: str

@app.post('/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    cursor = conn.cursor()
    query_KH = 'SELECT * FROM khachhang WHERE email = %s OR soDienThoai_KH = %s'
    query_AD = 'SELECT * FROM nhanvien WHERE (email = %s OR soDienThoai_NV = %s) AND chucVu = "Admin"'
    query_QL = 'SELECT * FROM nhanvien WHERE (email = %s OR soDienThoai_NV = %s) AND chucVu = "Quản lý"'
    cursor.execute(query_KH, (username,username))
    customer = cursor.fetchone()
    cursor.execute(query_AD, (username,username))
    admin = cursor.fetchone()
    cursor.execute(query_QL, (username,username))
    manager = cursor.fetchone()
    if customer:
        if customer[5] == password:
            customer_object = Customer(
                id=customer[0],
                userName=customer[1],
                email=customer[2],
                phone=customer[3],
                bankAccount=customer[4],
                password=customer[5]
            )
            return {"user_type": "customer", "customer_object": customer_object}
    if admin:
        if admin[9] == password:
            admin_object = Admin(
                id=admin[0],
                userName=admin[1],
                email=admin[8],
                phone=admin[6],
                password=admin[9]
            )
            return {"user_type": "admin", "admin_object": admin_object}
    if manager:
        if manager[9] == password:
            manager_object = Admin(
                id=manager[0],
                userName=manager[1],
                email=manager[8],
                phone=manager[6],
                password=manager[9]
            )
            return {"user_type": "manager", "manager_object": manager_object}
    raise HTTPException(status_code=401, detail='Tên tài khoản hoặc mật khẩu không chính xác')
