from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
import mysql.connector
from pydantic import BaseModel
from typing import List
import datetime

from connect_db import *


templates = Jinja2Templates(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\user\\templates")
# Kết nối thư mục "css" ,"js" và "img" để phục vụ các tệp tin tĩnh

# Đường dẫn tuyệt đối đến thư mục img
img_directory = "D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\user\\img-u"

# Gắn thư mục img vào tuyến đường '/img'
app.mount("/img-u", StaticFiles(directory=img_directory), name="img-u")


app.mount("/css-u", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\user\\css-u"), name="css-u")
app.mount("/js-u", StaticFiles(directory="D:\\Năm 3\\CSDL web\\THỰC HÀNH WEB\\ban-ve-xe-khach\\frontend\\user\\js-u"), name="js-u")

class Customer(BaseModel):
    id: int
    userName: str
    email: str
    phone: int
    bankAccount: str
    password: str


class Ticket(BaseModel):
    tripId: int 
    slot: int 
    time1: str
    time2: str
    price: int 
    driver: int 
    busId: str 
    routerId: int 
    ticketId: int 
    amount: int 
    tripId2: int 
    userId: int 
    payId: int 


@app.post("/get_kh_id/{id_KH}")
def get_kh_id(request: Request, id_KH: int):
    cursor = conn.cursor()
    query_KH = "SELECT * FROM khachhang WHERE maKhachHang = %s"
    cursor.execute(query_KH, (id_KH,))
    customer = cursor.fetchone()
    customer_object = Customer(
        id=customer[0],
        userName=customer[1],
        email=customer[2],
        phone=customer[3],
        bankAccount=customer[4],
        password=customer[5],
    )
    conn.commit()
    cursor.close()
    return {"customer_object": customer_object}


@app.get("/vehientai/me")
def check_ticket(myId: int, resquest: Request):
    cursor = conn.cursor()
    query = "SELECT * FROM chuyendi JOIN datve ON chuyendi.maChuyenDi = datve.machuyendi WHERE datve.maKhachHang = %s;"
    cursor.execute(query,(myId,))
    data = cursor.fetchall()  
    # data_ticket = Ticket(
    #     tripId=data[0][0],
    #     slot=data[0][1],
    #     time1=data[0][2],
    #     time2=data[0][3],
    #     price=data[0][4],
    #     driver=data[0][5],
    #     busId=data[0][6],
    #     apprId=data[0][7],
    #     ticketId=data[0][8],
    #     amount=data[0][9],
    #     tripId2=data[0][10],
    #     userId=data[0][11],
    #     payId=data[0][12],
    # )
    cursor.close()
    return templates.TemplateResponse("check_ticket.html", {"request": resquest, "data": data})

# @appr.post("/vedadi/me/{id}")
# def check_ticket(id: int):
#     cursor = conn.cursor()
#     query = "SELECT * FROM chuyendi JOIN datve ON chuyendi.maChuyenDi = datve.machuyendi WHERE datve.maKhachHang = %s AND DATE(chuyendi.gioDi) < CURRENT_DATE;"
#     cursor.execute(
#         query,
#         (id,),
#     )
#     data = cursor.fetchall()
#     data_ticket = Ticket(
#         tripId=data[0][0],
#         slot=data[0][1],
#         time1=data[0][2],
#         time2=data[0][3],
#         price=data[0][4],
#         driver=data[0][5],
#         busId=data[0][6],
#         apprId=data[0][7],
#         ticketId=data[0][8],
#         amount=data[0][9],
#         tripId2=data[0][10],
#         userId=data[0][11],
#         payId=data[0][12],
#     )
#     cursor.close()
#     # return templates.TemplateResponse("check_ve.html", {"request": request, "data": data})
#     return {"data_ticket": data_ticket}

@app.post('/huy_ve')
def huy_ve(request: Request, maChuyenDi: int = Form(...), soGheDat: int = Form(...), maVe: int = Form(...), soLuong: int = Form(...), maThanhToan: int = Form(...)):
    query = "DELETE FROM datve WHERE maVe = %s"
    query2 = "DELETE FROM thanhtoan WHERE maThanhToan = %s"
    query3 = "UPDATE chuyendi SET soGheDat = %s WHERE maChuyenDi = %s"
    soGheMoi = soGheDat - soLuong
    cursor = conn.cursor()
    cursor.execute(query, (maVe,))
    cursor.execute(query2, (maThanhToan,))
    cursor.execute(query3, (soGheMoi, maChuyenDi))
    conn.commit()
    cursor.close()
    return {"message": "Bạn đã hủy vé thành công"}


@app.post("/edit_me/{id_KH}")
async def edit_khachhang(
    id_KH: int, 
    username: str = Form(...), 
    phone: int = Form(...), 
    email: str = Form(...), 
    password: str = Form(...),
):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE khachhang SET tenKhachHang= %s, soDienThoai_KH = %s, email = %s, matKhau = %s WHERE maKhachHang = %s",
            (username, phone, email, password, id_KH),
        )
        conn.commit()
        return {"message": "Đã cập nhật thông tin thành công"}
    except mysql.connector.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()

@app.post('/get_ticket_number/{id_KH}')
def get_ticket_number(request: Request, id_KH: int):
    query = 'SELECT COUNT(*) FROM datve WHERE maKhachHang = %s'
    cursor = conn.cursor()
    cursor.execute(query, (id_KH,))
    ticket_number = cursor.fetchone()[0]  # Lấy giá trị từ tuple trả về
    conn.commit()
    cursor.close()
    return {"message": ticket_number}



@app.get("/home_user.html", response_class=HTMLResponse)
async def read1(request: Request):
    return templates.TemplateResponse("home_user.html", {"request": request})


@app.get("/acc_info.html", response_class=HTMLResponse)
async def read2(request: Request):
    return templates.TemplateResponse("acc_info.html", {"request": request})


@app.get("/check_ticket.html", response_class=HTMLResponse)
async def read3(request: Request):
    return templates.TemplateResponse("check_ticket.html", {"request": request})


@app.get("/contact_info.html", response_class=HTMLResponse)
async def read4(request: Request):
    return templates.TemplateResponse("contact_info.html", {"request": request})


@app.get("/help.html", response_class=HTMLResponse)
async def read5(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})


@app.get("/home_guest.html", response_class=HTMLResponse)
async def read6(request: Request):
    return templates.TemplateResponse("home_guest.html", {"request": request})



# Define your data model
class LoTrinh(BaseModel):
    benXuatPhat: str
    benKetThuc: str
    tinhXuatPhat: str
    tinhKetThuc: str


# Create a connection to the database

cursor = conn.cursor()

# Check if the 'lotrinh' table exists
cursor.execute("SHOW TABLES LIKE 'lotrinh'")
table_exists = cursor.fetchone()


# Define your API endpoint
@app.get('/get_data', response_model=List[LoTrinh])
def get_lo_trinh():
    # Create a connection to the database
    cursor = conn.cursor(dictionary=True)

    # Retrieve only the relevant columns from the 'lotrinh' table
    cursor.execute("SELECT DISTINCT benXuatPhat, benKetThuc, tinhXuatPhat, tinhKetThuc FROM lotrinh")
    data = cursor.fetchall()
    
    return data


# Tạo chuyến xe cho 7 ngày tiếp theo không kể ngày hôm nay
try:
    # Tạo bảng tạm
    cursor.execute("CREATE TEMPORARY TABLE temp_lotrinhs (maLoTrinh INT)")

    # Chèn dữ liệu vào bảng tạm
    cursor.execute("INSERT INTO temp_lotrinhs (maLoTrinh) SELECT maLoTrinh FROM lotrinh")
    # Lấy ngày hiện tại
    current_date = datetime.now().date()
    # Lặp qua từng ngày trong tuần tiếp theo (7 ngày kế tiếp)
    for _ in range(7):
        current_date += datetime.timedelta(days=1)
        # Kiểm tra xem ngày đã được xử lý hay chưa
        cursor.execute("SELECT COUNT(*) FROM chuyendi WHERE DATE(gioDi) = %s", (current_date,))
        count = cursor.fetchone()[0]
        # Nếu chưa xử lý, thì tiếp tục xử lý và thêm bản ghi
        if count == 0:
            # Lặp qua từng bản ghi trong bảng tạm
            cursor.execute("SELECT maLoTrinh FROM temp_lotrinhs")
            for row in cursor.fetchall():
                maLoTrinh = row[0]
                # Danh sách giờ đi cố định
                gio_di_list = ['05:00:00', '20:00:00']
                for gio_di in gio_di_list:
                    # Lấy giá trị maXeKhach từ bảng xekhach
                    cursor.execute("SELECT maXeKhach FROM xekhach WHERE loaiGhe='Giường nằm' ORDER BY RAND() LIMIT 1 ")
                    maXeKhach = cursor.fetchone()[0]
                    # Lấy thông tin thời gian di chuyển từ bảng lotrinh
                    cursor.execute("SELECT thoi_gian_di_chuyen FROM lotrinh WHERE maLoTrinh = %s", (maLoTrinh,))
                    thoi_gian_di_chuyen = cursor.fetchone()[0]
                    # Lấy giá lộ trình từ bảng lotrinh và phụ phí từ bảng xe khách
                    cursor.execute("SELECT giaLoTrinh FROM lotrinh WHERE maLoTrinh=%s", (maLoTrinh,))
                    giaLoTrinh = cursor.fetchone()[0]
                    cursor.execute("SELECT phuPhi FROM xekhach WHERE maXeKhach = %s ", (maXeKhach,))
                    phuPhi = cursor.fetchone()[0]
                    giaChuyenDi = phuPhi + giaLoTrinh

                    # Thêm bản ghi mới vào bảng chuyendi
                    cursor.execute(f"""
                        INSERT INTO chuyendi (maChuyenDi, soGheDat, gioDi, gioDen, giaChuyenDi, taiXe, maXeKhach, maLoTrinh)
                        VALUES (
                            CONCAT('CD', LPAD(FLOOR(RAND()*1000000), 6, '0')),
                            0,
                            STR_TO_DATE(CONCAT('{current_date}', ' ', '{gio_di}'), '%Y-%m-%d %H:%i:%s'),
                            ADDTIME(STR_TO_DATE(CONCAT('{current_date}', ' ', '{gio_di}'), '%Y-%m-%d %H:%i:%s'), '{thoi_gian_di_chuyen}'),
                            '{giaChuyenDi}',
                            0,
                            '{maXeKhach}',
                            '{maLoTrinh}'
                        )
                    """, )

                # Danh sách giờ đi cố định
                gio_di_list = ['15:00:00', '10:00:00']
                for gio_di in gio_di_list:
                    # Lấy giá trị maXeKhach từ bảng xekhach
                    cursor.execute("SELECT maXeKhach FROM xekhach WHERE loaiGhe='Ghế ngồi' ORDER BY RAND() LIMIT 1 ")
                    maXeKhach = cursor.fetchone()[0]
                    # Lấy thông tin thời gian di chuyển từ bảng lotrinh
                    cursor.execute("SELECT thoi_gian_di_chuyen FROM lotrinh WHERE maLoTrinh = %s", (maLoTrinh,))
                    thoi_gian_di_chuyen = cursor.fetchone()[0]
                    # Lấy giá lộ trình từ bảng lotrinh và phụ phí từ bảng xe khách
                    cursor.execute("SELECT giaLoTrinh FROM lotrinh WHERE maLoTrinh=%s", (maLoTrinh,))
                    giaLoTrinh = cursor.fetchone()[0]
                    cursor.execute("SELECT phuPhi FROM xekhach WHERE maXeKhach = %s ", (maXeKhach,))
                    phuPhi = cursor.fetchone()[0]
                    giaChuyenDi = phuPhi + giaLoTrinh
                    # Thêm bản ghi mới vào bảng chuyendi
                    cursor.execute(f"""
                        INSERT INTO chuyendi (maChuyenDi, soGheDat, gioDi, gioDen, giaChuyenDi, taiXe, maXeKhach, maLoTrinh)
                        VALUES (
                            CONCAT('CD', LPAD(FLOOR(RAND()*1000000), 6, '0')),
                            0,
                            STR_TO_DATE(CONCAT('{current_date}', ' ', '{gio_di}'), '%Y-%m-%d %H:%i:%s'),
                            ADDTIME(STR_TO_DATE(CONCAT('{current_date}', ' ', '{gio_di}'), '%Y-%m-%d %H:%i:%s'), '{thoi_gian_di_chuyen}'),
                            '{giaChuyenDi}',
                            0,
                            '{maXeKhach}',
                            '{maLoTrinh}'
                        )
                    """, )
    # Commit các thay đổi
    conn.commit()
    print("Đã tạo chuyến đi mới thành công.")
except Exception as e:
    # Rollback nếu có lỗi
    conn.rollback()
    print(f"Lỗi: {e}")

# Xoá các chuyến đi trong ngày hôm nay mà có số ghế đặt =0
try:
    # Lấy ngày hiện tại
    current_date = datetime.now().date()

    # Tạo điều kiện ngày để xóa các chuyến đi trong ngày hôm nay
    condition_date = f"DATE(gioDi) = '{current_date}'"

    # Tạo điều kiện số ghế đặt = 0
    condition_seats = "soGheDat = 0"

    # Kết hợp cả hai điều kiện
    condition = f"{condition_date} AND {condition_seats}"

    # Câu truy vấn DELETE
    delete_query = f"DELETE FROM chuyendi WHERE {condition}"

    # Thực hiện câu truy vấn DELETE
    cursor.execute(delete_query)

    # Commit các thay đổi
    conn.commit()

    print(f"Đã xóa các chuyến đi trong ngày {current_date} mà số ghế đặt = 0 thành công.")
except Exception as e:
    # Rollback nếu có lỗi
    conn.rollback()
    print(f"Lỗi: {e}")

# Tạo thêm chuyến đi mới nếu đã hết vé


# Lọc xe
class FilterRequest(BaseModel):
    benXuatPhat: str
    benKetThuc: str
    date: str
    busType: str


@app.post("/filter-trips")
async def filter_trips(request: FilterRequest):
    try:

        # Thực hiện truy vấn SQL để lọc dữ liệu
        sql = f"""
            SELECT chuyendi.gioDi, chuyendi.gioDen, lotrinh.benXuatPhat, lotrinh.benKetThuc, chuyendi.maXeKhach,xekhach.loaiGhe, chuyendi.giaChuyenDi,chuyendi.maChuyenDi
        FROM chuyendi
        INNER JOIN lotrinh ON chuyendi.maLoTrinh = lotrinh.maLoTrinh
        INNER JOIN xekhach ON chuyendi.maXeKhach = xekhach.maXeKhach
        WHERE lotrinh.benXuatPhat LIKE '{request.benXuatPhat}'
            AND lotrinh.benKetThuc LIKE '{request.benKetThuc}'
            AND SUBSTRING(chuyendi.gioDi, 1, 10) = '{request.date}'
            AND chuyendi.maLoTrinh = lotrinh.maLoTrinh
            AND chuyendi.maXeKhach = xekhach.maXeKhach
            AND chuyendi.soGheDat < xekhach.soGhe
            AND xekhach.loaiGhe = '{request.busType}'
        """
        cursor.execute(sql)
        result = cursor.fetchall()

        if result:
            records = []
            for row in result:
                records.append(row)

            return records
        else:
            raise HTTPException(status_code=404, detail="Không có dữ liệu phù hợp")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint cập nhật số ghế và tạo vé mới
class UpdateSeatRequest(BaseModel):
    tripId: int
    ticketNumber: int
    payment_method: str
    # ID_user: str


@app.post("/book_success/{userId}")
async def book_success(request_data: UpdateSeatRequest, userId: int):
    tripId = request_data.tripId
    ticketNumber = request_data.ticketNumber
    payment_method = request_data.payment_method
    # ID_user = request_data.phone_user

    # Cập nhập số ghế
    cursor.execute("SELECT * FROM chuyendi WHERE maChuyenDi = %s", (tripId,))
    chuyendi = cursor.fetchone()

    if chuyendi is None:
        raise HTTPException(status_code=404, detail=f"Chuyến đi không tồn tại maChuyenDi = {tripId}")
    cursor.execute("SELECT soGheDat FROM chuyendi WHERE maChuyenDi = %s", (tripId,))
    soGheDaCo = cursor.fetchone()[0]
    new_seat_count = soGheDaCo + ticketNumber
    print(new_seat_count)
    cursor.execute("UPDATE chuyendi SET soGheDat = %s WHERE maChuyenDi = %s", (new_seat_count, tripId))
    conn.commit()
    # return {"message": "Cập nhập số vé đặt thành công"}

    # Tạo mã vé mới và mã thanh toán mới
    cursor.execute("SELECT * FROM chuyendi WHERE maChuyenDi = %s", (tripId,))
    chuyendi = cursor.fetchone()

    if chuyendi is None:
        raise HTTPException(status_code=404, detail="Chuyến đi không tồn tại")

    # Lấy mã vé và mã thanh toán hiện tại
    cursor.execute("SELECT MAX(maVe) FROM datve")
    current_max_ticket_id = cursor.fetchone()[0] or 0  # Trường hợp đặc biệt khi không có vé nào trong cơ sở dữ liệu

    cursor.execute("SELECT MAX(maThanhToan) FROM datve")
    current_max_payment_id = cursor.fetchone()[
                                 0] or 0  # Trường hợp đặc biệt khi không có thanh toán nào trong cơ sở dữ liệu

    # Tăng giá trị của mã vé và mã thanh toán
    new_ticket_id = current_max_ticket_id + 1
    new_payment_id = current_max_payment_id + 1

    # Thêm vào bảng thanh toán
    cursor.execute("SELECT giaChuyenDi FROM chuyendi WHERE maChuyenDi=%s", (tripId,))
    gia = cursor.fetchone()[0]
    total = gia * ticketNumber
    if payment_method == "Online":
        trangThai = 1
    else:
        trangThai = 0
    cursor.execute("INSERT INTO thanhtoan (maThanhToan,trangThai,tongTien) VALUES (%s,%s,%s)",
                   (new_payment_id, trangThai, total))
    # ID_user = '21001111'  # chỗ này phải sửa khi ghép code
    # Thêm vé vào bảng đặt vé
    cursor.execute("INSERT INTO datve (maVe,soLuong, maChuyenDi,maKhachHang,maThanhToan) VALUES (%s,%s,%s,%s,%s)",
                   (new_ticket_id, ticketNumber, tripId, userId, new_payment_id))
    conn.commit()

    return {"message": "Tạo vé mới thành công"}