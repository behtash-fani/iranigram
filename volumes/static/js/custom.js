// document.addEventListener("DOMContentLoaded", function () {
//   let buttons = document.querySelectorAll(".copy-text");
//   for (let i = 0; i < buttons.length; i++) {
//     buttons[i].addEventListener("click", function (event) {
//       event.preventDefault();
//       let value = this.getAttribute("value");
//       navigator.clipboard.writeText(value);
//       buttons.forEach(function (item) {
//         item.className = "btn btn-light rounded-4 copy-text";
//       });
//       this.className = "btn btn-warning rounded-4 copy-text";
//     });
//   }
// });