// create functionality for go to top button
let mybutton = document.getElementById("scrollUp");
window.onscroll = function() {scrollUp()};

function scrollUp() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
    } else {
    mybutton.style.display = "none";
    }
}
function goToTop() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0; 
}
// create functionality for go to top button
