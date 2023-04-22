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
      let value = this.getAttribute("value");
      let text = this.innerText;
      navigator.clipboard.writeText(value);
      buttons.forEach(function (item) {
        item.className = "btn btn-light rounded-4 copy-text";
      });
      this.className = "btn btn-warning rounded-4 copy-text";
    });
  }
});

if (window.location.pathname === '/dashboard/verify-login/' || window.location.pathname === '/dashboard/verify-register/') {
  var counter = getCounterValueFromStorage() || 60; // get the initial value from localStorage or cookie, or use 60 if not available
  var intervalId;
  let phone_number = document.querySelector('#phone_number')
  var phone = phone_number ? phone_number.getAttribute('data-phone') : null;

  window.onload = function startCounter() {
    intervalId = setInterval(decrementCounter, 1000);
  }

  function decrementCounter() {
    counter--;
    if (document.getElementById("counter")) {
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
      removeCounterValueFromStorage(); // remove the counter value from localStorage or cookie when it reaches 0
    } else {
      storeCounterValueInStorage(counter); // store the current counter value in localStorage or cookie
    }
  }

  function getCounterValueFromStorage() {
    // retrieve the counter value from localStorage or cookie
    return localStorage.getItem('counter') || getCookie('counter');
  }

  function storeCounterValueInStorage(counter) {
    // store the current counter value in localStorage or cookie
    localStorage.setItem('counter', counter);
    setCookie('counter', counter, 1); // set the cookie to expire in 1 day
  }

  function removeCounterValueFromStorage() {
    // remove the counter value from localStorage or cookie
    localStorage.removeItem('counter');
    deleteCookie('counter');
  }

  function setCookie(name, value, days) {
    // set a cookie with the given name, value, and expiration time
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
  }

  function getCookie(name) {
    // retrieve a cookie with the given name
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
  }

  function deleteCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  }
}