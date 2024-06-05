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


// lọc tài khoản
// chưa làm xong
var name = document.querySelectorAll(".name");
var mail = document.querySelectorAll(".mail");
var tel = document.querySelectorAll(".telephone");
var type = document.querySelectorAll(".type");

var filter_btn = document.getElementsByClassName('search_button').value;
var filter_name = document.getElementsByName('acc-name').value;
var filter_mailphone = document.getElementsByName('acc-mailphone').value;
var filter_type = document.getElementsByName('acc-type').value;

//filter_btn.onclick = function() {
//  for (const n of name) {
//    if (name.innerHTML == filter_name)
//  }
//
//}


var all = document.getElementById('table-data');
var edit = document.getElementById('acc-edit');
var info = document.getElementById('acc-info');

for (const btn of document.querySelectorAll(".edit-btn")) {
  // When the user clicks the button, open the modal
  btn.onclick = function () {
    all.style.display = "none";
    edit.style.display = 'block';
    info.style.display = 'none';

  }
}

var edit_link = document.getElementById('edit-link');
var info_link = document.getElementById('info-link');

info_link.onclick = function () {
  all.style.display = "none";
  edit.style.display = 'none';
  info.style.display = 'block';
}
edit_link.onclick = function () {
  all.style.display = "none";
  edit.style.display = 'block';
  info.style.display = 'none';
}

var del_link = document.getElementById('del-link');
var alert = document.getElementById('alert');
var close_btn = document.getElementById("close-btn");

// When the user clicks the button, open the modal
del_link.onclick = function () {
  alert.style.display = "block";
}


// When the user clicks anywhere outside of the modal hoặc nút không, close it
window.onclick = function (event) {
  if (event.target == alert || event.target == close_btn) {
    alert.style.display = "none";
  }
}

var del_btn = document.getElementById("yes");
del_btn.onclick = function () {
  // gửi yêu cầu xóa tài khoản này lên server
  location.reload();
}


function handleSubmit() {
  const selectElement = document.querySelector('select[name="user-type"]');
  const selectedOption = selectElement.value;
  const table = document.getElementById('add_khachhang');
  const table_NV = document.getElementById('add_nhanvien')
  // Xử lý dữ liệu dựa trên giá trị đã chọn
  if (selectedOption === 'passenger') {
    // Logic khi chọn Khách hàng
    table.style.display = 'block';
  } else if (selectedOption === 'manager') {
    // Logic khi chọn Quản lý
    table_NV.style.display = 'block'
    console.log('Bạn đã chọn Quản lý');
  } else if (selectedOption === 'administrator') {
    // Logic khi chọn Admin
    table_NV.style.display = 'block'
    console.log('Bạn đã chọn Admin');
  }
}

async function add_khachhang() {
  const tenKH = document.getElementById("tenKH").value;
  const email = document.getElementById("email").value
  const sdt = document.getElementById("soDT").value
  const nganhang = document.getElementById("nganhang").value
  const mk = document.getElementById("mk").value
  const table = document.getElementById('add_khachhang')
  const response = await fetch('http://127.0.0.1:8000/add_kh', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
          'tenKH': tenKH,
          'email': email,
          'sdt': sdt,
          'nganhang': nganhang,
          'mk': mk
      })
  });
  const responseData = await response.json();
  const message = responseData.message;
  alert(message)
  table.style.display = 'none'
}




// function editCustomer(userId) {
//   console.log("Sửa khách hàng với userId: " + userId);

//   // window.open("/edit_kh/" + userId, "_blank", "width=300,height=280,left=1200");
//   var update_btn = document.getElementById("update");

//   var alert = document.getElementById("alert");
//   var update_btn = document.getElementById("update");
//   var close_btn = document.getElementById("close-btn");

//   // When the user clicks the button, open the modal
//   update_btn.onclick = function () {
//       alert.style.display = "block";
//   }

//   // When the user clicks on close button, close it
//   window.onclick = function (event) {
//       if (event.target == close_btn) {
//           alert.style.display = "none";
//       }
//   }
// }



var editButtons = document.querySelectorAll(".edit-button");
var deleteButtons = document.querySelectorAll(".delete-button");

editButtons.forEach(function(button) {
  var userId = button.dataset.userId;
  button.addEventListener("click", function() {
    editCustomer(userId);
  });
});

deleteButtons.forEach(function(button) {
  var userId = button.dataset.userId;
  button.addEventListener("click", function() {
    deleteCustomer(userId);
  });
});


// $(document).ready(function() {
//   // Bắt đầu chỉnh sửa khi người dùng bấm vào ô input
//   $('table.editable td').on('click', function() {
//       // Lưu giá trị cũ
//       var oldValue = $(this).text();
      
//       // Tạo ô input để chỉnh sửa
//       var input = $('<input type="text" value="' + oldValue + '">');
      
//       // Thay thế ô td bằng ô input
//       $(this).html(input);
      
//       // Tự động focus vào ô input
//       input.focus();
      
//       // Xử lý sự kiện khi người dùng kết thúc chỉnh sửa
//       input.on('blur', function() {
//           // Lấy giá trị mới từ ô input
//           var newValue = $(this).val();
          
//           // Kiểm tra nếu có sự thay đổi
//           if (newValue !== oldValue) {
//               // Lấy ID của hàng để cập nhật dữ liệu
//               var id = $(this).closest('tr').data('id');
              
//               // Gửi yêu cầu cập nhật thông qua Ajax
//               $.ajax({
//                   url: '/update',
//                   type: 'POST',
//                   contentType: 'application/json',
//                   data: JSON.stringify({id: id, value: newValue}),
//                   success: function(response) {
//                       if (response.success) {
//                           // Cập nhật thành công
//                           $(this).closest('td').text(newValue);
//                           console.log("Dữ liệu đã được cập nhật thành công");
//                       } else {
//                           console.log("Lỗi khi cập nhật dữ liệu");
//                       }
//                   },
//                   error: function() {
//                       console.log("Lỗi khi gửi yêu cầu cập nhật dữ liệu");
//                   }
//               });
//           } else {
//               // Không có sự thay đổi, khôi phục giá trị cũ
//               $(this).closest('td').text(oldValue);
//           }
//       });
//   });
// });
