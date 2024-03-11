let mybutton = document.getElementById("scrollUp");

window.onscroll = function () {
  scrollUp();
};

function scrollUp() {
  if (
    (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) &&
    !window.location.pathname.startsWith("/dashboard/")
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

function goToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}