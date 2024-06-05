// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
for (const btn of document.querySelectorAll(".myBtn")) {
  // When the user clicks the button, open the modal
  btn.onclick = function () {
    modal.style.display = "block";
  }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// chuyển qua lại giữa đăng nhập và đăng ký
var login = document.getElementById("login");
var register = document.getElementById("register");
var login_link = document.getElementById("login-link");
var register_link = document.getElementById("register-link");

login_link.onclick = function () {
  login.style.display = "none";
  register.style.display = "block";

}
register_link.onclick = function () {
  register.style.display = "none";
  login.style.display = "block";

}

// chuyển trang khi ấn đăng nhập và đăng ký
// function login_redirect() {
//     for (const el of document.getElementById('login-form').querySelectorAll("[required]")) {
//       if (!el.reportValidity()) {       // kiểm tra xem người dùng đã nhập hết các trường chưa
//         return;
//       }
//     }



//    xác minh xem là loại tài khoản nào  (admin, quản lý, khách)
//    if (điều kiện xác nhận tài khoản admin) {
//        window.location = 'admin1.html'
//    } else if (...

// document.getElementById('login-form').submit();

// window.location = 'user/templates/home_user.html';     // nếu là khách
// window.location = 'admin/templates/admin.html';     // nếu là admin
//    window.location = chưa có;     // nếu là quản lý
// }

function register_redirect() {
  for (const el of document.getElementById('register-form').querySelectorAll("[required]")) {
    if (!el.reportValidity()) {
      return;
    }
  }


  //    document.getElementById('register-form').submit();
  // window.location = 'user/templates/home_user.html';
}

async function login_redirect() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch('http://127.0.0.1:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      'username': username,
      'password': password
    })
  });

  if (response.ok) {
    const responseData = await response.json();
    const userType = responseData.user_type; // Assume the backend sends the user type
    // const customerObjectString = JSON.stringify(responseData.customer_object, null, 2); //Lấy ra cả file
    // alert(customerObjectString); // Lấy ra ID
    // alert(customerId);
    switch (userType) {
      case 'customer':
        // Nếu là khách hàng, chuyển hướng đến trang demo.html
        const customerId = responseData.customer_object.id  // Lấy ra ID
        // document.getElementById('customerIdInput').value = customerId
        console.log(customerId)
        localStorage.setItem('customerID', customerId)
        const url = 'http://127.0.0.1:8000/home_user.html';
        // const url = 'http://127.0.0.1:8000/home_user.html?id=' + customerId;
        window.location.href = url;
        break;
      case 'admin':
        // Nếu là quản trị viên, chuyển hướng đến trang admin.html
        const adminId = responseData.admin_object.id  // Lấy ra ID
        window.location.href = 'http://127.0.0.1:8000/users';
        break;
      case 'manager':
        // Nếu là quản lý, chuyển hướng đến trang quanly.html
        const managerId = responseData.manager_object.id  // Lấy ra ID
        window.location.href = 'http://127.0.0.1:8000/ticket.html';
        break;
      default:
        alert('Đăng nhập thất bại. Loại người dùng không được xác định.');
    }
  } else {
    // Đăng nhập thất bại, có thể hiển thị thông báo lỗi hoặc giữ người dùng ở trang đăng nhập
    alert('Đăng nhập thất bại. Vui lòng kiểm tra tên đăng nhập và mật khẩu.');
  }
}

// async function sendId(customerId) {
//   const response = await fetch('http://127.0.0.1:8000/user_id', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({ customerId }),
//   });

//   if (response.ok) {
//     const responseData = await response.json();
//     console.log(responseData);
//   } else {
//     console.log('Lỗi khi gửi yêu cầu.');
//   }
// }

