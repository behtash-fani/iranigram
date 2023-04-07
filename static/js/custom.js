// show number that enter in field of charge wallet to persian letter
let letter_price = document.getElementById("letter_price");
let id_amount = document.getElementById("id_amount");
if (letter_price) {
  letter_price.innerHTML = Num2persian(0);
}
if (id_amount) {
  id_amount.addEventListener("input", (event) => {
    letter_price.innerHTML = Num2persian(event.target.value);
  });
}
// end of snippet

// this code enable toast message
$(document).ready(function () {
  $(".toast")
    .toast({
      delay: 10000,
    })
    .toast("show");
});
// end of snippet

document.addEventListener("DOMContentLoaded", function () {
  let buttons = document.querySelectorAll(".copy-text");
  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", function (event) {
      event.preventDefault();
      let value = this.value;
      let text = this.innerText;
      navigator.clipboard.writeText(value);
      buttons.forEach(function (item) {
        item.className = "btn btn-light rounded-4 copy-text";
      });
      this.className = "btn btn-warning rounded-4 copy-text";
    });
  }
});


var counter = 10;
var intervalId;
let phone_number = document.querySelector('#phone_number')
let phone = phone_number.getAttribute('data-phone')

window.onload = function startCounter() {
  intervalId = setInterval(decrementCounter, 1000);
}

function decrementCounter() {
  counter--;
    if (document.getElementById("counter")){
        document.getElementById("counter").innerHTML = counter;
    }
  if (counter === 0) {
    $.ajax({
        url: '/dashboard/check-expire-time/',
        dataType: 'json',
        method: 'POST',
        data: {
            'phone_number': phone
        },
        headers: {
            "X-CSRFToken": csrf_token,
        },
        success: function (response) {
            console.log(response.msg)
        },
        error: function (error) {
            console.log(error);
        }
    })
    clearInterval(intervalId);
    document.getElementById('counter_box').className = "d-none"
    document.getElementById('send_otpcode_again').classList.remove('d-none')
    document.getElementById('send_otpcode_again').classList.remove('d-block')
  }
}
