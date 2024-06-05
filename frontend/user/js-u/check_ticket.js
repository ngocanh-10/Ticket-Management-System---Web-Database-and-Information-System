// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("user-img");
// When the user clicks the button, open the modal
btn.onmouseover = function () {
  modal.style.display = "block";
}
window.onmouseover = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var alert = document.getElementById("alert");
var close_btn = document.getElementById("close-btn");

for (const btn of document.querySelectorAll(".del-btn")) {
  // When the user clicks the button, open the modal
  btn.onclick = function () {
    alert.style.display = "block";
  }
}

// When the user clicks anywhere outside of the modal hoặc nút không, close it
window.onclick = function (event) {
  if (event.target == alert || event.target == close_btn) {
    alert.style.display = "none";
  }
}

// var table1 = document.getElementById("table-data1");
// var table2 = document.getElementById("table-data2");
// var table3 = document.getElementById("table-data3");
// var filter1 = document.getElementById("filter1");
// var filter2 = document.getElementById("filter2");
// var filter3 = document.getElementById("filter3");





async function check_ticket() {

  event.preventDefault();


  const userId = localStorage.getItem('customerID')


  // Gửi yêu cầu đến máy chủ FastAPI thông qua Fetch API
  fetch('http://127.0.0.1:8000/vehientai/me', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      
      myId: userId
      
    }),
  })
    .then(response => {
      if (!response.ok) {

        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(async data => {
      alert("Chọn vé thành công")
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Đã xảy ra lỗi khi cập nhật số ghế. Vui lòng thử lại.');
    });
  return false

}
//   tableUser1.style.display = 'block'

//   const responseData = await response.json();
//   console.log(responseData.data_ticket)
//   const customerObjectString = JSON.stringify(responseData.data_ticket, null, 2)
//   console.log(customerObjectString);
//   const tripId = responseData.data_ticket.tripId
//   document.getElementById("tripId").textContent = tripId
//   const slot = responseData.data_ticket.slot
//   document.getElementById("slot").textContent = slot
//   const time1 = responseData.data_ticket.time1
//   document.getElementById("time1").textContent = time1
//   const time2 = responseData.data_ticket.time2
//   document.getElementById("time2").textContent = time2
//   const price = responseData.data_ticket.price
//   document.getElementById("price").textContent = price
//   const ticketId = responseData.data_ticket.ticketId
//   document.getElementById("ticketId").textContent = ticketId
//   const amount = responseData.data_ticket.amount
//   document.getElementById("amount").textContent = amount
//   const userId = responseData.data_ticket.userId
//   document.getElementById("userId").textContent = userId
//   const payId = responseData.data_ticket.payId
//   document.getElementById("payId").textContent = payId
//   const driver = responseData.data_ticket.driver
//   document.getElementById("driver").textContent = driver
//   const routerId = responseData.data_ticket.routerId
//   document.getElementById("routerId").textContent = routerId
//   const tripId2 = responseData.data_ticket.tripId2
//   document.getElementById("tripId2").textContent = tripId2
// }



async function huy(maChuyenDi, soGheDat, maVe, soLuong, gioDi, maThanhToan) {
  var currentDateTime = new Date();
  var gioDiDate = new Date(gioDi); // Chuyển đổi gioDi thành đối tượng Date
  currentDateTime.setDate(currentDateTime.getDate() + 1)
  if (gioDiDate <= currentDateTime) {
    console.log("Không thể hủy chuyến vé trước 1 ngày");
  } else {
    const response = await fetch('http://127.0.0.1:8000/huyve', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        'maChuyenDi': maChuyenDi,
        'soGheDat': soGheDat,
        'maVe': maVe,
        'soLuong': soLuong,
        'maThanhToan': maThanhToan
      })
    });
    const responseData = await response.json();
    const message = responseData.message;
    console.log(message);
  }
}


