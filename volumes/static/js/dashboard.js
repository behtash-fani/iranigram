// Define a mapping object for URLs and DOM elements
const dashboardElements = {
  "/dashboard/new-order/": document.getElementsByClassName("new_order"),
  "/dashboard/": document.getElementsByClassName("state_dashboard"),
  "/dashboard/profile/": document.getElementsByClassName("profile_dashboard"),
  "/dashboard/wallet/": document.getElementsByClassName("wallet_dashboard"),
  "/dashboard/orders/": document.getElementsByClassName("orders_list_dashboard"),
  "/dashboard/transactions/": document.getElementsByClassName("transactions_dashboard"),
  "/dashboard/api-docs/": document.getElementsByClassName("api_docs"),
  "/dashboard/services/": document.getElementsByClassName("services"),
  "/dashboard/support/": document.getElementsByClassName("support_dashboard"),
};

// Function to highlight and de-highlight elements based on the current URL
function highlightDashboardElements() {
  const currentPath = window.location.pathname;

  for (const path in dashboardElements) {
    const elements = dashboardElements[path];
    if (currentPath === path) {
      for (let i = 0; i < elements.length; i++) {
        elements[i].classList.add("bg-warning");
        elements[i].classList.remove("bg-transparent");
      }
    } else {
      for (let i = 0; i < elements.length; i++) {
        elements[i].classList.remove("bg-warning");
        elements[i].classList.add("bg-transparent");
      }
    }
  }
}

// Check if the current URL is in the mapping and apply highlighting
if (dashboardElements.hasOwnProperty(window.location.pathname)) {
  highlightDashboardElements();
} else if (window.location.pathname.includes("/dashboard/ticket/") || window.location.pathname.includes("/dashboard/submit-ticket/")) {
  // Special case for the support dashboard
  highlightDashboardElements();
  const body = document.body;
  body.style.overflowX = "hidden";
  body.style.overflowY = "scroll";
}


// dashboard menu

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

// function for change service depend on service type

let service_selection = document.querySelector("#id_service");
let csrf_token = $("[name=csrfmiddlewaretoken]").val();

$("#id_service_type").change(function () {
  const serviceTypeId = $(this).val();
  const url = $("#new_order_form").attr("data-services-url");

  if(serviceTypeId){
  $.ajax({
    url: url,
    data: {
      serviceTypeId: serviceTypeId,
    },
    headers: {
      "X-CSRFToken": csrf_token,
    },
    success: function (data) {
      service_selection.innerHTML =
        "<option value='' selected>---------</option>";
      data.services.map((item) => {
        const option = document.createElement("option");
        option.textContent = item.title;
        option.setAttribute("value", item.id);
        service_selection.appendChild(option);
      });
    },
  });
}
});

// function for show description of choice service
let service_info = "";
let id_quantity = document.getElementById("id_quantity");

function updateServiceDetails(serviceId) {
  const url = $("#new_order_form").data("service-url");
  let desc_box = document.getElementById("desc_box");
  let title_service = document.getElementById("title_service");
  let min_service = document.getElementById("min_service");
  let max_service = document.getElementById("max_service");
  let price_per_unit_service = document.getElementById("price_per_unit_service");
  let no_choice_product = document.getElementById("no-choice-product");
  let product_spec_box = document.getElementById("product-spec-box");

  if (serviceId){
    $.ajax({
      url: url,
      data: {
        serviceId: serviceId,
      },
      headers: {
        "X-CSRFToken": csrf_token,
      },
      success: function (data) {
        if (data.service_detail.link_type === "instagram_profile") {
          document.getElementById("profile_link_label").classList = "d-block";
          document.getElementById("post_link_label").classList = "d-none";
          document.getElementById("telegram_link_label").classList = "d-none";
        } else if (data.service_detail.link_type === "instagram_post_link") {
          document.getElementById("profile_link_label").classList = "d-none";
          document.getElementById("post_link_label").classList = "d-block";
          document.getElementById("telegram_link_label").classList = "d-none";
        } else if (data.service_detail.link_type === "telegram_link") {
          document.getElementById("profile_link_label").classList = "d-none";
          document.getElementById("post_link_label").classList = "d-none";
          document.getElementById("telegram_link_label").classList = "d-block";
        }
        id_quantity.setAttribute("min", data.service_detail.min_order);
        id_quantity.setAttribute("max", data.service_detail.max_order);
        desc_box.innerHTML = "";
        service_info = data.service_detail;
        product_spec_box.classList.remove("d-none");
        no_choice_product.classList.add("d-none");
        let lines = data.service_detail.description.split("\n");
        for (const linesKey in lines) {
          const spec_line = document.createElement("p");
          spec_line.innerHTML = lines[linesKey].trim();
          desc_box.appendChild(spec_line);
        }
        title_service.innerHTML = data.service_detail.title;
        min_service.innerHTML = data.service_detail.min_order;
        max_service.innerHTML = data.service_detail.max_order;
        price_per_unit_service.innerHTML = data.service_detail.amount;
      },
    });
  }
  
}

$(document).ready(function () {
  if( $('#id_service').val() && $("#id_service_type").val() ) {
    const initialServiceId = $("#id_service").val();
    updateServiceDetails(initialServiceId);
  }
  $("#id_service").change(function () {
    if ( $(this).val() && $("#id_service_type").val()) {
      const selectedServiceId = $(this).val();
      updateServiceDetails(selectedServiceId);
    }
  });
  $("#id_service_type").change(function () {
    $("#id_service").val("");
      let no_choice_product = document.getElementById("no-choice-product");
      let product_spec_box = document.getElementById("product-spec-box");
      product_spec_box.classList.add("d-none");
      no_choice_product.classList.remove("d-none");

    if ( !$(this).val()) {
      $("#id_service").val("");
    }
  });
});


let total_price = document.getElementById("total_price");
let total_number = document.getElementById("total_number");
if (id_quantity) {
  id_quantity.addEventListener("input", (event) => {
    let quantity_input_value = parseInt(event.target.value);
    let product_amount = parseInt(service_info.amount);
    let quantity = parseInt(quantity_input_value);
    let max = parseInt(event.target.max);
    let min = parseInt(event.target.min);
    if (!isNaN(product_amount)) {
      if (!isNaN(quantity)) {
        if (parseInt(event.target.value) > max) {
          event.target.value = max;
          total_price.innerHTML = "";
          total_price.textContent = Num2persian(parseInt(product_amount * max));
          total_number.innerHTML = "";
          total_number.textContent = Num2persian(max.toString());
        } else {
          total_price.textContent = Num2persian(
            parseInt(product_amount * quantity)
          );
          total_number.textContent = Num2persian(quantity.toString());
        }
        if (parseInt(event.target.value) < min) {
          total_price.textContent = Num2persian(parseInt(product_amount * min));
          total_number.textContent = Num2persian(min.toString());
        } else {
          total_price.textContent = Num2persian(
            parseInt(product_amount * quantity)
          );
          total_number.textContent = Num2persian(quantity.toString());
        }
      } else if (event.target.value === "") {
        total_price.textContent = "--";
        total_number.textContent = "--";
      }
    }
  });
}

$(function () {
  $("#id_quantity").change(function () {
    const max = parseInt($(this).attr("max"));
    const min = parseInt($(this).attr("min"));
    if ($(this).val() > max) {
      $(this).val(max);
    } else if ($(this).val() < min) {
      $(this).val(min);
    }
  });
});

let complete_order_payment = document.getElementById("complete-order-payment");
if (complete_order_payment) {
  complete_order_payment.addEventListener("click", (e) => {
    let user_balance = parseInt(
      complete_order_payment.getAttribute("data-user-balance")
    );
    let total_amount = parseInt(
      complete_order_payment.getAttribute("data-total-amount")
    );
    let order_id = parseInt(
      complete_order_payment.getAttribute("data-order-id")
    );
    let data = {
      order_id: order_id,
      amount: total_amount,
    };
    $.ajax({
      url: "/orders/complete-order-payment/",
      dataType: "json",
      method: "POST",
      data: data,
      headers: {
        "X-CSRFToken": csrf_token,
      },
      success: function (response) {
        if (response.redirect) {
          window.location.href = response.redirect;
        }
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
}
