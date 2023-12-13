function sendComment() {
    var urlElement = document.getElementById('comment-list-url');
		var url = urlElement.getAttribute('data-url');
		var name = document.getElementById('name-field').value;
		var phone_number = document.getElementById('phone-number-field').value;
		var content = document.getElementById('content-field').value;
		var page_idElement = document.getElementById('page-id');
		var page_id = page_idElement.getAttribute('data-pageid');
		var page_url = window.location.href;

		if (name === '' || phone_number === '' || content === '') {
			var alertBox = document.getElementById('comment-alert-box');
			alertBox.classList.remove('d-none');
			alertBox.classList.add('alert-warning');
			alertBox.innerHTML = 'لطفا همه فیلدها رو پر کن';
			return false;
		}

		var xhr = new XMLHttpRequest();
		var params = 'name=' + encodeURIComponent(name) +
			'&phone_number=' + encodeURIComponent(phone_number) +
			'&content=' + encodeURIComponent(content) +
			'&page_id=' + encodeURIComponent(page_id) +
			'&page_url=' + encodeURIComponent(page_url);

		xhr.open('GET', url + '?' + params, true);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				var response_data = JSON.parse(xhr.responseText);
				if (response_data.success) {
					var commentAlertBox = document.getElementById('comment-alert-box');
					commentAlertBox.classList.remove('d-none');
					commentAlertBox.classList.add('alert-success');
					commentAlertBox.innerHTML = 'ممنون بابت نظرت، نظر با ارزشت رو پیش خودمون نگه میداریم البته شاید برای بقیه هم به اشتراک گذاشتیم';
					document.getElementById('name-field').value = '';
					document.getElementById('phone-number-field').value = '';
					document.getElementById('content-field').value = '';
				}
			}
		};

		xhr.send();
}

function sendResponse() {
    var response_urlElement = document.getElementById('submit-response-url');
		var response_url = response_urlElement.getAttribute('data-url');
		var comment_idElement = document.getElementById('comment-id');
		var comment_id = comment_idElement.getAttribute('data-comment-id');
		var response_name = document.getElementById('response-name-field').value;
		var response_phone_number = document.getElementById('response-phone-number-field').value;
		var response_content = document.getElementById('response-content-field').value;

		var xhr = new XMLHttpRequest();
		var params = 'comment_id=' + encodeURIComponent(comment_id) +
			'&name=' + encodeURIComponent(response_name) +
			'&phone_number=' + encodeURIComponent(response_phone_number) +
			'&content=' + encodeURIComponent(response_content);

		xhr.open('GET', response_url + '?' + params, true);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				var response_data = JSON.parse(xhr.responseText);
				if (response_data.success) {
					var responseAlertBox = document.getElementById('response-alert-box');
					responseAlertBox.classList.remove('d-none');
					responseAlertBox.classList.add('alert-success');
					responseAlertBox.innerHTML = 'از ارسال پاسخ به این نظر ممنونم. سعی میکنیم نظرت رو سریع با بقیه به اشتراک بگذاریم';
					document.getElementById('response-name-field').value = '';
					document.getElementById('response-phone-number-field').value = '';
					document.getElementById('response-content-field').value = '';
				}
			}
		};

		xhr.send();
}