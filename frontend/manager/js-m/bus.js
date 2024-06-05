// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("user-img");
// When the user clicks the button, open the modal
btn.onmouseover = function() {
  modal.style.display = "block";
}
window.onmouseover = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var save_btn = document.getElementById("save");

for (const i of document.getElementsByClassName("changed-info")) {
        i.oninput = function() {
            save_btn.style.backgroundColor = "#0097B2";
            save_btn.style.border = "none";
            save_btn.style.cursor = 'pointer';
            save_btn.removeAttribute("disabled");
        }
    }

var edit_detail = document.getElementById("edit-detail");
for (const i of document.getElementsByClassName("edit-btn")) {
    i.onclick = function() {
        edit_detail.style.display = 'block';
        window.scrollTo(0, 500);
    }
}

var add_btn = document.getElementById("add-btn");
add_btn.onclick = function() {
    window.scrollTo(0, 500);
}

save_btn.onclick = function() {
    for (const i of document.getElementsByClassName("changed-info")) {
        i.submit();
    }
}

var del_btn = document.getElementById('del-btn');
var alert = document.getElementById('alert');
var close_btn = document.getElementById("close-btn");

// When the user clicks the button, open the modal
del_btn.onclick = function() {
  alert.style.display = "block";
}


// When the user clicks anywhere outside of the modal hoặc nút không, close it
window.onclick = function(event) {
  if (event.target == alert || event.target == close_btn) {
    alert.style.display = "none";
  }
}

var yes_btn = document.getElementById("yes");
yes_btn.onclick = function() {
    // gửi yêu cầu xóa này lên server
    location.reload();
}


