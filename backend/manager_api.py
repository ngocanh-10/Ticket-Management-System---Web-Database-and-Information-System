from fastapi import FastAPI, HTTPException, Request, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
import mysql.connector
from connect_db import *

# router = APIRouter()



templatesManager = Jinja2Templates(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\manager\\templates")
# Kết nối thư mục "css" ,"js" và "img" để phục vụ các tệp tin tĩnh


# Gắn thư mục img vào tuyến đường '/img'
app.mount("/img-m", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\img"), name="img-m")
app.mount("/css-m", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\manager\\css-m"), name="css-m")
app.mount("/js-m", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\manager\\js-m"), name="js-m")


# @app.get("/bus.html", response_class=HTMLResponse)
# async def read1(request: Request):
#     return templatesManager.TemplateResponse("bus.html", {"request": request})


# @app.get("/employee.html", response_class=HTMLResponse)
# async def read2(request: Request):
#     return templatesManager.TemplateResponse("employee.html", {"request": request})


# @app.get("/passenger.html", response_class=HTMLResponse)
# async def read3(request: Request):
#     return templatesManager.TemplateResponse("passenger.html", {"request": request})


# @app.get("/payment.html", response_class=HTMLResponse)
# async def read4(request: Request):
#     return templatesManager.TemplateResponse("payment.html", {"request": request})


# @app.get("/routes.html", response_class=HTMLResponse)
# async def read5(request: Request):
#     return templatesManager.TemplateResponse("routes.html", {"request": request})


# # @app.get("/ticket.html", response_class=HTMLResponse)
# # async def read6(request: Request):
# #     return templatesManager.TemplateResponse("ticket.html", {"request": request})


# @app.get("/trip.html", response_class=HTMLResponse)
# async def read6(request: Request):
#     return templatesManager.TemplateResponse("trip.html", {"request": request})


# quản lý khách hàng

@app.get("/passenger.html")
def get_khachhang(request: Request):
    cursor = conn.cursor() # Đại diện cho việc kết nối đến cơ sở dữ liệu 
    cursor.execute("SELECT maKhachHang, tenKhachHang, email, soDienThoai_KH, soTaiKhoanNH FROM khachhang ")
    data = cursor.fetchall() # Trả về tất các các kết quả truy vấn 
    cursor.close()
    return templatesManager.TemplateResponse("passenger.html", {"request": request, "data": data})


# Thêm 1 hàng vào bảng khachhang
@app.get("/add_kh", response_class=HTMLResponse)
async def add_kh_form(request: Request):
    return {"request": request}


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



# Edit bảng khachhang
@app.get("/edit_kh", response_class=HTMLResponse)
async def edit_khachhang_form(request: Request):
    return templatesManager.TemplateResponse("edit_khachhang.html", {"request": request})


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
@app.get("/delete_kh", response_class=HTMLResponse)
async def delete_khachhang(request: Request):
    return templatesManager.TemplateResponse("delete_khachhang.html", {"request": request})


@app.post("/delete_kh")
async def delete_khachhang_post(request: Request, maKhachHang: int = Form(...)):
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

# quản lý nhân viên

@app.get("/employee.html")
def get_khachhang(request: Request):
    cursor = conn.cursor()  
    cursor.execute("SELECT maNhanVien, tenNhanVien, chucVu, gioiTinh, soDienThoai_NV, email, ngaySinh, diaChi, luong FROM nhanvien ")
    data = cursor.fetchall()  
    cursor.close()
    return templatesManager.TemplateResponse("employee.html", {"request": request, "data": data})
       

# Thêm 1 hàng vào bảng nhanvien
@app.get("/add_nv", response_class=HTMLResponse)
async def add_nv_form(request: Request):
    return {"request": request}


@app.post("/add_nv")
async def add_nv(
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
            "INSERT INTO nhanvien (tenNhanVien, chucVu, ngaySinh, gioiTinh, diaChi, soDienThoai_NV, luong, email, matKhau) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (tenNhanVien, chucVu, ngaySinh, gioiTinh, diaChi, soDienThoai_NV, luong, email, matKhau),
        )
        conn.commit()
        return {"message": "Đã thêm nhân viên thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng nhanvien
@app.get("/edit_nv", response_class=HTMLResponse)
async def edit_nhanvien_form(request: Request):
    return templatesManager.TemplateResponse("edit_nhanvien.html", {"request": request})


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
            "UPDATE khachhang SET tenNhanVien = %s, chucVu = %s, ngaySinh = %s, gioiTinh = %s, diaChi = %s, soDienThoai_NV = %s, luong = %s, email = %s, matKhau = %s WHERE maNhanVien = %s",
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
@app.get("/delete_nv", response_class=HTMLResponse)
async def delete_nhanvien(request: Request):
    return templatesManager.TemplateResponse("delete_nhanvien.html", {"request": request})


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

# quản lý vé

@app.get("/ticket.html")
def get_datve(request: Request):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM datve")
    data = cursor.fetchall() 
    cursor.close()
    return templatesManager.TemplateResponse("ticket.html", {"request": request, "data": data})

# Thêm 1 hàng vào bảng datve
@app.get("/add_datve", response_class=HTMLResponse)
async def add_datve_form(request: Request):
    return {"request": request}


@app.post("/add_datve")
async def add_datve(
    soLuong: int = Form(...),
    maChuyenDi: str = Form(...),
    maKhachHang: int = Form(...),
    maThanhToan: str = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO datve (soLuong, maChuyenDi, maKhachHang, maThanhToan) VALUES (%s, %s, %s, %s)",
            (soLuong, maChuyenDi, maKhachHang, maThanhToan)
        )
        conn.commit()
        return {"message": "Đã thêm vé đặt thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng datve 
@app.get("/edit_datve", response_class=HTMLResponse)
async def edit_datve_form(request: Request):
    return templatesManager.TemplateResponse("edit_datve.html", {"request": request})

@app.post("/edit_datve")
async def edit_datve(
    maVe: str = Form(...),
    soLuong: int = Form(...),
    maChuyenDi: str = Form(...),
    maKhachHang: int = Form(...),
    maThanhToan: str = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE datve SET soLuong = %s, maChuyenDi = %s, maKhachHang = %s, maThanhToan = %s WHERE maVe = %s", (soLuong, maChuyenDi, maKhachHang, maThanhToan, maVe))
        conn.commit()
        return {"message": "Đã cập nhật thông tin đặt vé thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Xóa 1 hàng dựa trên mã vé của bảng datve
@app.get("/delete_datve", response_class=HTMLResponse)
async def delete_datve(request: Request):
    return templatesManager.TemplateResponse("delete_datve.html", {"request": request})


@app.post("/delete_datve")
async def delete_datve_post(request: Request, maVe: str = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM datve WHERE maVe = %s", (maVe,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()      

# quản lý chuyến đi

        
@app.get("/trip.html")
def get_chuyendi(request: Request):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM chuyendi ")
    data = cursor.fetchall() 
    cursor.close()
    return templatesManager.TemplateResponse("trip.html", {"request": request, "data": data})

# Thêm 1 hàng vào bảng chuyendi
@app.get("/add_chuyendi", response_class=HTMLResponse)
async def add_chuyendi_form(request: Request):
    return {"request": request}


@app.post("/add_chuyendi")
async def add_chuyendi(
    soGheDat: int = Form(...),
    gioDi: str = Form(...),
    gioDen: str = Form(...),
    giaChuyenDi: int = Form(...),
    taiXe: str = Form(...),
    maXeKhach: str = Form(...),
    maLoTrinh: int = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO chuyendi (soGheDat, gioDi, gioDen, giaChuyenDi, taiXe, maXeKhach, maLoTrinh) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (soGheDat, gioDi, gioDen, giaChuyenDi, taiXe, maXeKhach, maLoTrinh)
        )
        conn.commit()
        return {"message": "Đã thêm chuyến đi thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng chuyendi 
@app.get("/edit_chuyendi", response_class=HTMLResponse)
async def edit_chuyendi_form(request: Request):
    return templatesManager.TemplateResponse("edit_chuyendi.html", {"request": request})

@app.post("/edit_chuyendi")
async def edit_chuyendi(
    maChuyenDi: str = Form(...),
    soGheDat: int = Form(...),
    gioDi: str = Form(...),
    gioDen: str = Form(...),
    giaChuyenDi: int = Form(...),
    taiXe: str = Form(...),
    maXeKhach: str = Form(...),
    maLoTrinh: int = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE chuyendi SET soGheDat = %s, gioDi = %s, gioDen = %s, giaChuyenDi = %s, taiXe = %, maXeKhach = %s, maLoTrinh = %s WHERE maChuyenDi = %s", (soGheDat, gioDi, gioDen, giaChuyenDi, taiXe, maXeKhach, maLoTrinh, maChuyenDi))
        conn.commit()
        return {"message": "Đã cập nhật thông tin chuyến đi thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Xóa 1 hàng dựa trên mã khách hàng của bảng chuyendi
@app.get("/delete_chuyendi", response_class=HTMLResponse)
async def delete_chuyendi(request: Request):
    return templatesManager.TemplateResponse("delete_chuyendi.html", {"request": request})


@app.post("/delete_chuyendi")
async def delete_chuyendi_post(request: Request, maChuyenDi: str = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chuyendi WHERE maChuyenDi = %s", (maChuyenDi,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# quản lý xe

@app.get("/bus.html")
def get_xekhach(request: Request):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM xekhach ")
    data = cursor.fetchall() 
    cursor.close()
    return templatesManager.TemplateResponse("bus.html", {"request": request, "data": data})

# Thêm 1 hàng vào bảng xekhach
@app.get("/add_xekhach", response_class=HTMLResponse)
async def add_xekhach_form(request: Request):
    return {"request": request}


@app.post("/add_xekhach")
async def add_xekhach(
    maXeKhach: str = Form(...),
    loaiGhe: str = Form(...),
    soGhe: int = Form(...),
    phuPhi: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO xekhach (maXeKhach, loaiGhe, soGhe, phuPhi) VALUES (%s, %s, %s, %s)",
            (maXeKhach, loaiGhe, soGhe, phuPhi)
        )
        conn.commit()
        return {"message": "Đã thêm xe thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng xekhach 
@app.get("/edit_xekhach", response_class=HTMLResponse)
async def edit_xekhach_form(request: Request):
    return templatesManager.TemplateResponse("edit_xekhach.html", {"request": request})

@app.post("/edit_xekhach")
async def edit_xekhach(
    maXeKhach: str = Form(...),
    loaiGhe: str = Form(...),
    soGhe: int = Form(...),
    phuPhi: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE xekhach SET loaiGhe = %s, soGhe = %s, phuPhi = %s WHERE maXeKhach = %s", (loaiGhe, soGhe, phuPhi, maXeKhach))
        conn.commit()
        return {"message": "Đã cập nhật thông tin xe thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Xóa 1 hàng dựa trên mã xe của bảng xekhach
@app.get("/delete_xekhach", response_class=HTMLResponse)
async def delete_xekhach(request: Request):
    return templatesManager.TemplateResponse("delete_xekhach.html", {"request": request})


@app.post("/delete_xekhach")
async def delete_xekhach_post(request: Request, maXeKhach: str = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM xekhach WHERE maXeKhach = %s", (maXeKhach,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# quản lý lộ trình
        

@app.get("/routes.html")
def get_lotrinh(request: Request):
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM lotrinh ")
    data = cursor.fetchall() 
    cursor.close()
    return templatesManager.TemplateResponse("routes.html", {"request": request, "data": data})

# Thêm 1 hàng vào bảng lotrinh
@app.get("/add_lotrinh", response_class=HTMLResponse)
async def add_lotrinh_form(request: Request):
    return {"request": request}


@app.post("/add_lotrinh")
async def add_lotrinh(
    diemDau: str = Form(...),
    diemCuoi: str = Form(...),
    tinhXuatPhat: str = Form(...),
    tinhKetThuc: str = Form(...),
    giaLoTrinh: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO lotrinh (diemDau, diemCuoi, tinhXuatPhat, tinhKetThuc, giaLoTrinh) VALUES (%s, %s, %s, %s, %s)",
            (diemDau, diemCuoi, tinhXuatPhat, tinhKetThuc, giaLoTrinh)
        )
        conn.commit()
        return {"message": "Đã thêm thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng lotrinh 
@app.get("/edit_lotrinh", response_class=HTMLResponse)
async def edit_lotrinh_form(request: Request):
    return templatesManager.TemplateResponse("edit_lotrinh.html", {"request": request})

@app.post("/edit_lotrinh")
async def edit_lotrinh(
    maLoTrinh: int = Form(...),
    diemDau: str = Form(...),
    diemCuoi: str = Form(...),
    tinhXuatPhat: str = Form(...),
    tinhKetThuc: str = Form(...),
    giaLoTrinh: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE lotrinh SET diemDau = %s, diemCuoi = %s, tinhXuatPhat = %, tinhKetThuc = %s, giaLoTrinh = %s WHERE maLoTrinh = %s", (diemDau, diemCuoi, tinhXuatPhat, tinhKetThuc, giaLoTrinh, maLoTrinh))
        conn.commit()
        return {"message": "Đã cập nhật thông tin lộ trình thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Xóa 1 hàng dựa trên mã lộ trình của bảng lotrinh
@app.get("/delete_lotrinh", response_class=HTMLResponse)
async def delete_lotrinh(request: Request):
    return templatesManager.TemplateResponse("delete_lotrinh.html", {"request": request})


@app.post("/delete_lotrinh")
async def delete_lotrinh_post(request: Request, maLoTrinh: str = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM lotrinh WHERE maLoTrinh = %s", (maLoTrinh,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# quản lý thanh toán
        
@app.get("/payment.html")
def get_congviec(request: Request):
    cursor = conn.cursor() # Đại diện cho việc kết nối đến cơ sở dữ liệu 
    cursor.execute("SELECT * FROM thanhtoan")
    data = cursor.fetchall() # Trả về tất các các kết quả truy vấn 
    cursor.close()
    return templatesManager.TemplateResponse("payment.html", {"request": request, "data": data})


# Thêm 1 hàng vào bảng thanhtoan
@app.get("/add_thanhtoan", response_class=HTMLResponse)
async def add_thanhtoan_form(request: Request):
    return {"request": request}


@app.post("/add_thanhtoan")
async def add_thanhtoan(
    trangThai: int = Form(...),
    tongTien: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO thanhtoan (trangThai, tongTien) VALUES (%s, %s)",
            (trangThai, tongTien)
        )
        conn.commit()
        return {"message": "Đã thêm thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Edit bảng thanhtoan 
@app.get("/edit_thanhtoan", response_class=HTMLResponse)
async def edit_thanhtoan_form(request: Request):
    return templatesManager.TemplateResponse("edit_thanhtoan.html", {"request": request})

@app.post("/edit_thanhtoan")
async def edit_thanhtoan(
    maThanhToan: int = Form(...),
    trangThai: int = Form(...),
    tongTien: float = Form(...)
):
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE thanhtoan SET trangThai = %s, tongTien = %s WHERE maThanhToan = %s", (trangThai, tongTien, maThanhToan))
        conn.commit()
        return {"message": "Đã cập nhật thanh toán thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

# Xóa 1 hàng dựa trên mã lộ trình của bảng thanhtoan
@app.get("/delete_thanhtoan", response_class=HTMLResponse)
async def delete_thanhtoan(request: Request):
    return templatesManager.TemplateResponse("delete_thanhtoan.html", {"request": request})


@app.post("/delete_thanhtoan")
async def delete_thanhtoan_post(request: Request, maLoTrinh: str = Form(...)):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM thanhtoan WHERE maLoTrinh = %s", (maLoTrinh,))
        conn.commit()
        return {"message": "Deleted successfully"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
