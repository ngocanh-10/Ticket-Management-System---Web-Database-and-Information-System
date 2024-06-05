for (const btn of document.querySelectorAll(".myBtn")) {
    // When the user clicks the button, open the modal
      btn.onclick = function() {
        alert("Bạn chưa đăng nhập. Vui lòng quay trở lại trang chủ và đăng nhập.");
      }
}

