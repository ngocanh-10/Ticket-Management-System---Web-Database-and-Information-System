var latestTicketNumber; // lưu số ghế khách đặt
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

// Hiện các giá trị lựa chọn cho 4 cột: benXuatPhat,benKetThuc,tinhXuatPhat,tinhKetThuc
async function getData() {
  // You have a server endpoint to fetch data
  const response = await fetch('http://127.0.0.1:8000/get_data');
  const data = await response.json();
  console.log(data)
  return data;
}

async function populateDropdownOptions(dropdownId, options) {
  const dropdown = document.getElementById(dropdownId);
  dropdown.innerHTML = ''; // Clear existing options

  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option;
    dropdown.appendChild(optionElement);
  });
}

async function updateDropdownOptions(dropdownId, filterKey, filterValue) {
  const data = await getData();
  const filteredOptions = [...new Set(data.filter(item => item[filterKey] === filterValue).map(item => item[dropdownId]))];
  await populateDropdownOptions(dropdownId, filteredOptions);
}

async function updateBenXuatPhatOptions() {
  const selectedTinhXuatPhat = document.getElementById('tinhXuatPhat').value;
  await updateDropdownOptions('benXuatPhat', 'tinhXuatPhat', selectedTinhXuatPhat);
}

async function updateBenKetThucOptions() {
  const selectedTinhKetThuc = document.getElementById('tinhKetThuc').value;
  await updateDropdownOptions('benKetThuc', 'tinhKetThuc', selectedTinhKetThuc);
}

// Initial population
document.addEventListener('DOMContentLoaded', async () => {
  const data = await getData();
  const tinhXuatPhatOptions = [...new Set(data.map(item => item.tinhXuatPhat))];
  const tinhKetThucOptions = [...new Set(data.map(item => item.tinhKetThuc))];

  await populateDropdownOptions('tinhXuatPhat', tinhXuatPhatOptions);
  await populateDropdownOptions('tinhKetThuc', tinhKetThucOptions);
  await updateBenXuatPhatOptions();
  await updateBenKetThucOptions();
});

// Lấy thẻ input date
var dateInput = document.getElementById('date');

// Thêm sự kiện input và change để kiểm tra giá trị ngày
dateInput.addEventListener('input', function () {
  validateDate();
});

dateInput.addEventListener('change', function () {
  validateDate();
});

// Hàm kiểm tra giá trị ngày và cập nhật giá trị min
function validateDate() {
  // Lấy ngày hiện tại
  var today = new Date();
  // Thêm một ngày để có ngày kế tiếp
  today.setDate(today.getDate() + 1);

  // Chuyển định dạng ngày thành YYYY-MM-DD
  var formattedToday = today.toISOString().split('T')[0];

  // Lấy giá trị ngày từ input
  var selectedDate = dateInput.value;

  // So sánh giá trị ngày và ngày hiện tại
  if (selectedDate < formattedToday) {
    alert('Bạn chỉ có thể đặt xe cho 7 ngày sau KHÔNG kể từ ngày hiện tại');
    // Nếu ngày chọn nhỏ hơn ngày hiện tại, cập nhật giá trị ngày thành ngày hiện tại
    dateInput.value = formattedToday;
  }
}

function filterTripsAndScroll() {
  // Gọi hàm để lọc chuyến đi
  filterTrips();

  // Cuộn lên đầu trang
  window.scrollTo(0, 0);
  alert("Chọn phương thức thanh toán trước khi đặt vé!")
}
// Lọc xe
function filterTrips() {

  var start = document.getElementById("benXuatPhat").value;
  var end = document.getElementById("benKetThuc").value;
  var date = document.getElementById("date").value;
  var bus_type = document.getElementById("bus-type").value;
  // Gửi yêu cầu lọc đến máy chủ FastAPI thông qua Fetch API
  fetch('http://127.0.0.1:8000/filter-trips', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      benXuatPhat: start,
      benKetThuc: end,
      date: date,
      busType: bus_type
    }),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      // Xử lý dữ liệu trả về từ máy chủ FastAPI
      // Lưu trữ thông tin từng dòng dữ liệu trong một mảng
      var tripData = data.map(arr => {
        return {
          gioDi: arr[0],
          gioDen: arr[1],
          benXuatPhat: arr[2],
          benKetThuc: arr[3],
          maXeKhach: arr[4],
          loaiGhe: arr[5],
          giaVe: arr[6],
          maChuyenDi: arr[7]
        };
      });
      displayResults(tripData);

    })
    .catch((error) => {
      console.error('Error:', error);
      alert('Không tồn tại chuyến đi này. Vui lòng chọn lại.');
    });

  // Ngăn chặn form submit mặc định
  return false;

  //
  function displayResults(tripData) {
    var container = document.querySelector(".list");

    // Xóa nội dung cũ của container
    container.innerHTML = "";

    // Lặp qua mỗi bản ghi và tạo phần tử HTML tương ứng
    tripData.forEach(result => {
      var listItem = document.createElement("div");
      listItem.classList.add("list-item", "sleeper");


      var left = document.createElement("div");
      left.classList.add("left");

      var h2 = document.createElement("h2");
      h2.textContent = `Xe (${result.loaiGhe} )`;

      var leftInfo = document.createElement("div");
      leftInfo.classList.add("left-info");

      // var busImage = document.createElement("img");
      // busImage.classList.add("bus-image");
      // // busImage.src = "../img-u/bus1.jpg";

      // var location = document.createElement("div");
      // location.classList.add("location-icon");

      var locationDetail1 = createLocationDetail(result.benXuatPhat, result.gioDi);
      var locationDetail2 = createLocationDetail(result.benKetThuc, result.gioDen);

      var ticketNumberDiv = document.createElement("div");
      ticketNumberDiv.style.display = "block";
      ticketNumberDiv.style.textAlign = "center";

      var ticketNumberLabel = document.createElement("p");
      ticketNumberLabel.textContent = "Số vé đặt";

      var ticketNumberInput = document.createElement("input");
      ticketNumberInput.classList.add("ticket-number");
      ticketNumberInput.type = "text";

      // Thêm thông tin "mã xe khách", "mã chuyến đi" và "loại ghế" vào phần tử HTML
      var maXeKhachP = document.createElement("p");
      maXeKhachP.textContent = `Mã Xe Khách: ${result.maXeKhach}`;

      var maChuyenDiP = document.createElement("p");
      maChuyenDiP.textContent = `Mã Chuyến Đi: ${result.maChuyenDi}`;

      var loaiGheP = document.createElement("p");
      loaiGheP.textContent = `Loại Ghế: ${result.loaiGhe}`;
      // Chèn các phần tử con vào container
      location.appendChild(locationDetail1);
      location.appendChild(document.createElement("br"));
      location.appendChild(locationDetail2);

      ticketNumberDiv.appendChild(ticketNumberLabel);
      ticketNumberDiv.appendChild(ticketNumberInput);


      // leftInfo.appendChild(busImage);
      // leftInfo.appendChild(location);
      leftInfo.appendChild(ticketNumberDiv);

      left.appendChild(h2);
      left.appendChild(leftInfo);

      var right = document.createElement("div");
      right.classList.add("right");

      var giaVeP = document.createElement("p");
      giaVeP.textContent = `Giá vé: ${result.giaVe}`;

      var voucherBorder = document.createElement("div");
      voucherBorder.classList.add("voucher-border");

      var voucherLink = document.createElement("a");
      voucherLink.href = "my_voucher.html";

      var voucherDiv = document.createElement("div");
      voucherDiv.classList.add("voucher");
      voucherDiv.textContent = "Voucher";

      var selectBusButton = document.createElement("button");
      selectBusButton.classList.add("select-bus");
      selectBusButton.textContent = "Chọn";

      v

      // Chèn các phần tử con vào container
      voucherLink.appendChild(voucherDiv);
      voucherBorder.appendChild(voucherLink);

      right.appendChild(giaVeP);
      right.appendChild(document.createElement("br"));
      right.appendChild(voucherBorder);
      right.appendChild(document.createElement("br"));
      right.appendChild(selectBusButton);

      listItem.appendChild(left);
      listItem.appendChild(right);

      container.appendChild(listItem);



      selectBusButton.addEventListener('click', function () {
        latestTripId = result.maChuyenDi; // Cập nhật mã chuyến đi mới nhất
        latestTicketNumber = parseInt(ticketNumberInput.value) || 0;
        window.scrollTo(0, 300);
        book_success(latestTripId, latestTicketNumber);
      });

    });
    return false
  }

  function createLocationDetail(location, time) {
    var locationDetail = document.createElement("div");
    locationDetail.classList.add("location-detail");

    // var locationIcon = document.createElement("img");
    // locationIcon.classList.add("location-icon");
    // locationIcon.src = "../img-u/location-icon1.png";

    var locationNameP = document.createElement("p");
    locationNameP.textContent = `\u00A0${location}:\u00A0\u00A0\u00A0\u00A0`;

    var timeP = document.createElement("p");
    timeP.textContent = time;

    // locationDetail.appendChild(locationIcon);
    locationDetail.appendChild(locationNameP);
    locationDetail.appendChild(timeP);

    return locationDetail;
  }

}



// nhấn nút đặt vé -> hệ thống cập nhập số ghế đặt cho chuyến đi đó trên csdl và tạo mã thanh toán mới cũng như mã vé mới
function book_success(latestTripId, latestTicketNumber) {
  console.log(latestTripId, latestTicketNumber);
  // Lấy thông tin cần thiết từ trang web
  var selectedBenXuatPhat = document.getElementById("benXuatPhat").value;
  var selectedBenKetThuc = document.getElementById("benKetThuc").value;
  var selectedDate = document.getElementById("date").value;
  var selectedBusType = document.getElementById("bus-type").value;


  // Tạo một đối tượng chứa thông tin đặt vé
  var bookingData = {
    benXuatPhat: selectedBenXuatPhat,
    benKetThuc: selectedBenKetThuc,
    date: selectedDate,
    busType: selectedBusType,
    ticketNumber: latestTicketNumber,
    tripId: latestTripId,

  };

  save_ticket(bookingData)
}

function save_ticket(bookingData) {
  event.preventDefault();


  const userId = localStorage.getItem('customerID')
  var latestTripId = bookingData.tripId;
  var latestTicketNumber = bookingData.ticketNumber;
  var selectedPayment = document.getElementById("payment").value;
  console.log(selectedPayment, latestTripId)
  // Gửi yêu cầu đến máy chủ FastAPI thông qua Fetch API
  fetch('http://127.0.0.1:8000/book_success/' + userId, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      payment_method: selectedPayment,
      ID_user: userId,
      tripId: latestTripId,
      ticketNumber: latestTicketNumber

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
function pay_ticket() {
  event.preventDefault();

  var payment = document.getElementById("payment");
  var stk = document.getElementById("stk");
  if (payment.options[1].selected) {
    stk.setAttribute("required", "required");
  }
  if (payment.options[0].selected) {
    stk.removeAttribute("required");
  }
  for (const el of document.getElementById('book-form').querySelectorAll("[required]")) {
    if (!el.reportValidity()) {       // kiểm tra xem người dùng đã nhập hết các trường chưa
      return;
    }
  }


  alert("Đặt vé thành công")
}