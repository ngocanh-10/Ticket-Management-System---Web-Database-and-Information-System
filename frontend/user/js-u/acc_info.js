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
var update_btn = document.getElementById("update");
var close_btn = document.getElementById("close-btn");

// When the user clicks the button, open the modal
update_btn.onclick = function () {
  alert.style.display = "block";
}

// When the user clicks on close button, close it
window.onclick = function (event) {
  if (event.target == close_btn) {
    alert.style.display = "none";
  }
}


async function myaccount() {
  const tableUser = document.getElementById('user_table')

  const id = localStorage.getItem('customerID')
  console.log(id)
  const response = await fetch('http://127.0.0.1:8000/get_kh_id/' + id, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });
  tableUser.style.display = 'block'
  const responseData = await response.json();
  const customerObjectString = JSON.stringify(responseData.customer_object, null, 2)
  console.log(customerObjectString);
  const userName = responseData.customer_object.userName
  document.getElementById("username").textContent = userName
  const phone = responseData.customer_object.phone
  document.getElementById("phone").textContent = phone
  const email = responseData.customer_object.email
  document.getElementById("email").textContent = email
  const password = responseData.customer_object.password
  document.getElementById("password").textContent = password

}

function hideaccount() {
  const tableUser = document.getElementById('user_table')
  tableUser.style.display = 'none'
}

async function quantityTicket() {
  const id = localStorage.getItem('customerID');
  const response = await fetch('http://127.0.0.1:8000/get_ticket_number/' + id, {
    method: 'POST', // Thay đổi phương thức thành GET
    headers: {
      'Content-Type': 'application/json',
    },
  });
  const responseData = await response.json();
  const ticket_number = responseData.message;
  document.getElementById("ticket-number").value = ticket_number
}

function closeForm() {
  var alertDiv = document.getElementById("alert");
  alertDiv.style.display = "none";
}

async function edit_KH() {
  const username = document.getElementById("username_edit").value
  const phone = document.getElementById("phone_edit").value
  const email = document.getElementById("email_edit").value
  const password = document.getElementById("password_edit").value
  const id = localStorage.getItem('customerID')
  const response = await fetch('http://127.0.0.1:8000/edit_me/' + id, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
          'username': username,
          'phone': phone,
          'email': email,
          'password': password
      })
  });
  const responseData = await response.json();
  const message = responseData.message;
  console.log(message)
}