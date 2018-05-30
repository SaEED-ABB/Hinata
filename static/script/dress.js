toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-left",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut",
  "rtl": true
}



$(document).on('mouseover','#previousImg,#nextImg',function(){
	$(this).find('img').css('visibility','visible');
});

$(document).on('mouseout','#previousImg,#nextImg',function(){
	$(this).find('img').css('visibility','hidden');
});
product_slug=window.location.href.split('/')[5];
$('.likeProduct').attr('product_slug',product_slug);
$('.basketProduct').attr('product_slug',product_slug);
$.ajax({
	type: 'GET',
	url: '/api/store/get_next_prev_of_product/',
	dataType: 'JSON',
	data: {
        product_slug: product_slug
    },
	success: function (data) {
		if(data.next){
			$('.nextImgHref').attr("href",data.next.link)
			$('#nextImg').css("background-image",'url('+data.next.image+')')
		}else{
			$('#nextImg').css("visibility",'hidden')
		}
		if(data.prev){
			$(".previousImgHref").attr("href",data.prev.link)
			$('#previousImg').css("background-image",'url('+data.prev.image+')')
		}else{
			$('#previousImg').css("visibility",'hidden')
		}
	},
	error: function(){

	}
});
$.ajax({
	type: 'GET',
	url: '/api/store/get_product_info/',
	dataType: 'JSON',
	data: {
        product_slug: product_slug
    },
	success: function (data) {
		$('.dressProp h1').html(data.name);
		for(var i=0;i<data.colors.length;i++){
			$('.colors').append('<div class="color" id="'+data.colors[i].id+'" style="background-color:'+data.colors[i].color_code+'"></div>');
		}
		for(var i=0;i<data.sizes.length;i++){
			$('.sizes').prepend('<div class="size" id="'+data.sizes[i].id+'">'+data.sizes[i].name+'</div>');
		}
		$('.price').html(data.price + ' تومان');
		for(var i=0;i<data.properties.length;i++){
			$('.properties').prepend('<li>'+data.properties[i].property+'</li>');
		}
		if(data.is_in_user_active_basket==true){
			$('.basketProduct').css('color','#00da00');
			$('.basketProduct').addClass('addToBasket');
		}
		if(data.is_in_user_favorites==true){
			$('.likeProduct').css('color','red');
			$('.likeProduct').addClass('addToFavorite');
		}
		for(var i=0;i<data.images.length-2;i++){
			$('.images').prepend('<a href=""><img class="dressImages" src="'+data.images[i+2].other+'"></a>');
		}
		for(var i=0;i<data.comments.length;i++){
			$('.commentsContainer').append('<div class="comment row">'+
		           		'<div class="col-sm-2 col-xs-3 commentImgContainer">'+
		              		'<img class="comment_img  img-responsive" src="'+returnImage(data.comments[i].user_photo_url)+'" />'+
		            	'</div>'+
			            '<div class="col-sm-10 col-xs-9" style="padding-right:0">'+
			                '<h4>'+data.comments[i].name+'</h4>'+
			                '<p>'+data.comments[i].comment+'</p>'+
			            '</div>'+
		            '</div>');
		}
		
	}
});
function returnImage(param){
	if (param==""){
		return "http://s3.amazonaws.com/nvest/Blank_Club_Website_Avatar_Gray.jpg"
	}

	return param
}
$(document).on('click touchstart','.basketProduct',function(){
	var thisElement=$(this);
	if(logged=="True"){
		if(!$(this).hasClass('addToBasket')){
			$.ajax({
				type: 'POST',
				url: '/api/store/add_to_basket/',
				dataType: 'JSON',
				data: {
			        product_slug: $(this).attr('product_slug')
			    },
				success: function (data) {
					thisElement.addClass('addToBasket');
					thisElement.css('color','#00da00')
					toastr.success('محصول مورد نظر به شبد خرید اضافه شد.')
				},
				error: function(){
					toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
				}
			});
		}else{
			$.ajax({
				type: 'POST',
				url: '/api/store/remove_from_basket/',
				dataType: 'JSON',
				data: {
			        product_slug: $(this).attr('product_slug')
			    },
				success: function (data) {
					thisElement.removeClass('addToBasket');
					thisElement.css('color','#949494')
					toastr.success('محصول مورد نظر از سبد خرید حذف شد.')
				},
				error: function(){
					toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
				}
			});
		}
	}else{
		toastr.warning('ابتدا وارد سایت شوید.')
	}
});
$(document).on('click touchstart','.likeProduct',function(){
	var thisElement=$(this);
	if(logged=="True"){
		if(!$(this).hasClass('addToFavorite')){
			$.ajax({
				type: 'POST',
				url: '/api/customer/add_favorite/',
				dataType: 'JSON',
				data: {
			        product_slug: $(this).attr('product_slug')
			    },
				success: function (data) {
					thisElement.addClass('addToFavorite');
					thisElement.css('color','red')
					toastr.success('محصول مورد نظر به لیست علاقه مندی ها اضافه شد.')
				},
				error: function(){
					toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
				}
			});
		}else{
			$.ajax({
				type: 'POST',
				url: '/api/customer/delete_favorite/',
				dataType: 'JSON',
				data: {
			        product_slug: $(this).attr('product_slug')
			    },
				success: function (data) {
					thisElement.removeClass('addToFavorite');
					thisElement.css('color','#949494')
					toastr.success('محصول مورد نظر از لیست علاقه مندی ها حذف شد.')
				},
				error: function(){
					toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
				}
			});
		}
	}else{
		toastr.warning('ابتدا وارد سایت شوید.')
	}
});

$(document).on('click touchstart','.comment_btn',function(){
	var thisElement=$(this);
	if(logged=="True"){
		data={
			comment:$('.textarea-comment').val(),
			product_slug:product_slug
		}
	}else{
		data={
			comment:$('.textarea-comment').val(),
			product_slug:product_slug,
			session_name: $('.commentName').val(),
		}
	}

	$.ajax({
			type: 'POST',
			url: '/api/customer/add_comment/',
			dataType: 'JSON',
			data: data,
			success: function (data) {
				toastr.success('نظر شما با موفقیت ارسال شد و پس از تایید در سایت قرار می گیرد.')
			},
			error: function(){
				toastr.error('خطایی رخ داده است. لطفا مجددا تلاش نمایید.')
			}
		});

});

$(document).ready(function() {
	new RangeSlider($("#materialRangeSlider"), {
	    size: 1,
	    percentage: 50
	});	
	new RangeSlider($("#priceRangeSlider"), {
	    size: 1,
	    borderSize: 0.4,
	    percentage: 80
	});	
	new RangeSlider($("#styleRangeSlider"), {
	    size: 1,
	    borderSize: 0.4,
	    percentage: 60
	});		

});
