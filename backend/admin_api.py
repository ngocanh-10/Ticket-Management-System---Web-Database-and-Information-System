from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from pydantic import BaseModel
from connect_db import *
import os

# router = APIRouter()


templatesAdmin = Jinja2Templates(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\admin\\templates")


# Đường dẫn tuyệt đối đến thư mục img
img_directory = "D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\admin\\img-a"

# Gắn thư mục img vào tuyến đường '/img'
app.mount("/img-a", StaticFiles(directory=img_directory), name="img-a")


app.mount("/css-a", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\admin\\css-a"), name="css-a")
app.mount("/js-a", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\admin\\js-a"), name="js-a")


@app.get("/admin.html", response_class=HTMLResponse)
async def readAdmin(request: Request):
    return templatesAdmin.TemplateResponse("admin.html", {"request": request})


@app.get("/admin_system.html", response_class=HTMLResponse)
async def readAdmin(request: Request):
    return templatesAdmin.TemplateResponse("admin_system.html", {"request": request})


# # lọc người dùng
# @app.post("/filter_users")
# async def filter_form(request: Request):
#     form_data = await request.form()
#     name = form_data["acc-name"]
#     email_phone = form_data["acc-mailphone"]
#     type_acc = form_data["acc-type"]
    
#     return {"name": name, "email_phone": email_phone, "type_acc": type_acc}

# @app.get("/filter_users")
# async def get_filter_user(request: Request, name: str, email_phone: str, type_acc: str):
#     cursor = conn.cursor()  # Đại diện cho việc kết nối đến cơ sở dữ liệu
#     if type_acc == "Khách hàng":
#         cursor.execute(
#             "SELECT maKhachHang, tenKhachHang, email, soDienThoai_KH, 'Khách hàng' AS chucVu FROM khachhang WHERE tenKhachHang = %s AND (soDienThoai_KH OR email = %s)",
#             (name, email_phone),
#         )
#     elif type_acc == "Admin":
#         cursor.execute(
#             "SELECT maNhanVien, tenNhanVien, email, soDienThoai_NV, chucVu FROM nhanvien WHERE tenNhanVien = %s AND (soDienThoai_NV OR email = %s) AND chucVu = 'Admin'",
#             (name, email_phone),
#         )
#     else:
#         cursor.execute(
#             "SELECT maNhanVien, tenNhanVien, email, soDienThoai_NV, chucVu FROM nhanvien WHERE tenNhanVien = %s AND (soDienThoai_NV OR email = %s) AND chucVu = 'Quản lý'",
#             (name, email_phone),
#         )
#     data = cursor.fetchall()  # Trả về tất các các kết quả truy vấn
#     cursor.close()
#     return templates.TemplateResponse(
#         "nguoidung.html", {"request": request, "data": data}
#     )




# Thêm 1 hàng vào bảng khachhang
@app.get("/add_kh", response_class=HTMLResponse)
async def add_kh_form(request: Request):
    return templatesAdmin.TemplateResponse("admin.html", {"request": request})


@app.post("/add_kh")
async def add_kh(
    tenKhachHang: str = Form(...),
    email: str = Form(...),
    soDienThoai_KH: int = Form(...),
    soTaiKhoanNH: str = Form(...),
    matKhau: str = Form(...),
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO khachhang (tenKhachHang, email, soDienThoai_KH, soTaiKhoanNH, matKhau) VALUES (%s, %s, %s, %s, %s)",
            (tenKhachHang, email, soDienThoai_KH, soTaiKhoanNH, matKhau),
        )
        conn.commit()
        return {"message": "Đã thêm khách hàng thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


@app.get("/users")
async def get_all_users(request: Request):
    cursor = conn.cursor() 
    cursor.execute(
        "SELECT maKhachHang, tenKhachHang, email, soDienThoai_KH, 'Khách hàng' AS chucVu FROM khachhang UNION ALL SELECT maNhanVien, tenNhanVien, email, soDienThoai_NV, chucVu FROM nhanvien"
    )
    data = cursor.fetchall() 
    cursor.close()
    return templatesAdmin.TemplateResponse(
        "admin.html", {"request": request, "data": data}
    )




# Edit bảng khachhang
@app.get("/edit_kh/{id}", response_class=HTMLResponse)
async def edit_khachhang_form(request: Request):
    return templatesAdmin.TemplateResponse("edit_khachhang.html", {"request": request})



@app.post("/edit_kh")
async def edit_khachhang(
    maKhachHang: int = Form(...),
    tenKhachHang: str = Form(...),
    email: str = Form(...),
    soDienThoai_KH: int = Form(...),
    soTaiKhoanNH: str = Form(...),
    matKhau: str = Form(...),
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE khachhang SET tenKhachHang = %s, email = %s, soDienThoai_KH = %s, soTaiKhoanNH = %s, matKhau = %s WHERE maKhachHang = %s",
            (tenKhachHang, email, soDienThoai_KH, soTaiKhoanNH, matKhau, maKhachHang),
        )
        conn.commit()
        return {"message": "Đã cập nhật thông tin khách hàng thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


# Xóa 1 hàng dựa trên mã khách hàng của bảng khachhang
@app.get("/delete_kh/{id}", response_class=HTMLResponse)
async def delete_khachhang(request: Request):
    return templatesAdmin.TemplateResponse("delete_khachhang.html", {"request": request})


@app.post("/delete_kh")
async def delete_khachhang_post(maKhachHang: int = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM khachhang WHERE maKhachHang = %s", (maKhachHang,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


# Edit bảng nhanvien
@app.get("/edit_nv/{id}", response_class=HTMLResponse)
async def edit_nhanvien_form(request: Request):
    return templatesAdmin.TemplateResponse("edit_nhanvien.html", {"request": request})


@app.post("/edit_nv")
async def edit_nhanvien(
    maNhanVien: int = Form(...),
    tenNhanVien: str = Form(...),
    chucVu: str = Form(...),
    ngaySinh: str = Form(...),
    gioiTinh: str = Form(...),
    diaChi: str = Form(...),
    soDienThoai_NV: int = Form(...),
    luong: int = Form(...),
    email: str = Form(...),
    matKhau: str = Form(...),
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE nhanvien SET tenNhanVien = %s, chucVu = %s, ngaySinh = %s, gioiTinh = %s, diaChi = %s, soDienThoai_NV = %s, luong = %s, email = %s, matKhau = %s WHERE maNhanVien = %s",
            (
                tenNhanVien,
                chucVu,
                ngaySinh,
                gioiTinh,
                diaChi,
                soDienThoai_NV,
                luong,
                email,
                matKhau,
                maNhanVien,
            ),
        )
        conn.commit()
        return {"message": "Đã cập nhật thông tin nhân viên thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()


# Xóa 1 hàng dựa trên mã nhân viên của bảng nhanvien
@app.get("/delete_nv/{id}", response_class=HTMLResponse)
async def delete_nhanvien(request: Request):
    return templatesAdmin.TemplateResponse("delete_nhanvien.html", {"request": request})


@app.post("/delete_nv")
async def delete_nhanvien_post(request: Request, maNhanVien: int = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM nhanvien WHERE maNhanVien = %s", (maNhanVien,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
