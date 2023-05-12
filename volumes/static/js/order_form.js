// function for change service depend on service type

let service_selection = document.querySelector("#id_service");
let csrf_token = $("[name=csrfmiddlewaretoken]").val();

$("#id_service_type").change(function () {
  const serviceTypeId = $(this).val();
  const url = $("#new_order_form").attr("data-services-url");

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
});

// function for show description of choice service
let service_info = "";
let id_quantity = document.getElementById("id_quantity");

$("#id_service").change(function () {
  const serviceId = $(this).val();
  const url = $("#new_order_form").attr("data-service-url");
  let desc_box = document.getElementById("desc_box");
  let title_service = document.getElementById("title_service");
  let min_service = document.getElementById("min_service");
  let max_service = document.getElementById("max_service");
  let price_per_unit_service = document.getElementById(
    "price_per_unit_service"
  );
  let no_choice_product = document.getElementById("no-choice-product");
  let product_spec_box = document.getElementById("product-spec-box");
  let desc_lines = [];
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
      } else if (data.service_detail.link_type === "instagram_post_link") {
        document.getElementById("profile_link_label").classList = "d-none";
        document.getElementById("post_link_label").classList = "d-block";
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

if (window.location.pathname === "/dashboard/new-order/") {
  window.onload = function () {
    let service_type_select = document.getElementById("id_service_type");
    let service_select = document.getElementById("id_service");
    let id_link = document.getElementById("id_link");
    let id_quantity = document.getElementById("id_quantity");
    if (service_type_select) {
      service_type_select.selectedIndex = 0;
    }
    if (service_select) {
      service_select.selectedIndex = 0;
    }
    if (id_link) {
      id_link.value = "";
    }
    if (id_quantity) {
      id_quantity.value = "";
    }
  };
}

function openPaymentModal() {
  const modal = document.getElementById("paymentModal");
  const payment_modal = new bootstrap.Modal(modal);
  payment_modal.show();
}

let credit_payment = document.getElementById("credit_payment");
if (credit_payment) {
	credit_payment.addEventListener("click", (e) => {
		let instagram_link = document.getElementById("id_link");
		// if (instagram_link) {
		// if (instagram_link.value == null || instagram_link.value == "") {
		// 	document.getElementById("link-empty-error").classList.remove("d-none");
		// } else {
		// 	document.getElementById("link-empty-error").classList.add("d-none");
		// }
		// }
		let price_per_unit_service = document.getElementById(
		"price_per_unit_service"
		);
		let order_quantity = document.getElementById("id_quantity");
		let user_balance = parseInt(
		credit_payment.getAttribute("data-user-balance").replace(",", "")
		);
		let total_amount = parseInt(
		order_quantity.value * price_per_unit_service.textContent
		);
		let remain_price = 0;
		if (total_amount > user_balance) {
		e.preventDefault();
		openPaymentModal();
		// if (!(instagram_link.value == null || instagram_link.value == "")) {
		// 	openPaymentModal();
		// }
		remain_price = total_amount - user_balance;
		if (remain_price < 500) {
			document.getElementById("modal_body").innerHTML = `
			با توجه به اینکه حداقل مبلغ قابل پرداخت در درگاه بانکی ۵۰۰ تومان است، آیا میخواهید که مبلغ ۵۰۰ تومان را پرداخت کنید و مبلغ باقی مانده در پایان سفارش به اعتبار شما اضافه شود؟`;
			remain_price = 500;
		} else {
			document.getElementById("modal_body").innerHTML = `
			مبلغ قابل پرداخت برای این سفارش ${total_amount} تومان و اعتبار کیف پول شما ${parseInt(
			user_balance
			)} تومان هست. آیا میخواهید ${remain_price} تومان باقی مانده را آنلاین پرداخت کنید ؟ `;
		}
		} else {
		}
		let modal_pay_button = document.getElementById("modal_pay_button");
		modal_pay_button.addEventListener("click", (e) => {
		let data = {
			service_type: $("#id_service_type").val(),
			service: $("#id_service").val(),
			link: $("#id_link").val(),
			order_quantity: $("#id_quantity").val(),
			remain_price: remain_price,
		};
		$.ajax({
			url: "/orders/pay-remain-price/",
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
	});
}

function openCompletePaymentModal() {
  const modal = document.getElementById("completepaymentModal");
  const payment_modal = new bootstrap.Modal(modal);
  payment_modal.show();
}

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
    let remain_price = 0;
    if (total_amount > user_balance) {
      e.preventDefault();
      openCompletePaymentModal();
      remain_price = total_amount - user_balance;
      if (remain_price < 500) {
        document.getElementById(
          "modal_body"
        ).innerHTML = `با توجه به اینکه حداقل مبلغ قابل پرداخت در درگاه بانکی ۵۰۰ تومان است، آیا میخواهید که مبلغ ۵۰۰ تومان را پرداخت کنید و مبلغ باقی مانده در پایان سفارش به اعتبار شما اضافه شود؟`;
        remain_price = 500;
      } else {
        document.getElementById(
          "modal_body"
        ).innerHTML = `مبلغ قابل پرداخت برای این سفارش ${total_amount} تومان و اعتبار کیف پول شما ${parseInt(
          user_balance
        )} تومان هست. آیا میخواهید ${remain_price} تومان باقی مانده را آنلاین پرداخت کنید ؟ `;
      }
    } else {
    }
    let complete_order_button = document.getElementById(
      "complete-order-button"
    );
    complete_order_button.addEventListener("click", (e) => {
      let data = {
        order_id: order_id,
        remain_price: remain_price,
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
            console.log(response.redirect);
          }
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  });
}
