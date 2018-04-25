$.ajax({
	type: 'GET',
	url: '/api/store/check/code',
	dataType: 'JSON',
	data: {
        code: String(code_value)
    },
	success: function (data, responseJSON) {
		// <div class="pCard">
		// 	<a class='link' href='#' > 
		// 		<img class='img-responsive' src='{% static "img/cloth1.jpg" %}' /> 
		// 		<h4 class='text-center' style='margin-top: 16px;margin-bottom: 20px;'>مانتو مجلسی</h4> 
		// 		<div class='row' style="margin-bottom: 15px;"> 
		// 			<div class='col-sm-6 cardIcons' style='margin-top: 6px;'> 
		// 				<img src="{% static 'img/basket.png' %}" class="basketProduct">
		// 				<img src="{% static 'img/like.png' %}" class="likeProduct">
		// 			</div> 
		// 			<div class='col-sm-6 cardPrice'> 
		// 				<span class="productPrice">120000</span> 
		// 			</div> 
		// 		</div> 
		// 	</a> 
		// </div>
	}
});