$(document).ready(function() {
	new RangeSlider($("#materialRangeSlider"), {
	    size: 1,
	    borderSize: 0.4,
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

$(document).on('mouseover','#previousImg,#nextImg',function(){
	$(this).find('img').css('visibility','visible');
});

$(document).on('mouseout','#previousImg,#nextImg',function(){
	$(this).find('img').css('visibility','hidden');
});
product_id=window.location.href.split('/')[4];
$('.likeProduct').attr('product_id',product_id);
$('.basketProduct').attr('product_id',product_id);

$.ajax({
	type: 'GET',
	url: '/api/store/get_product_info/',
	dataType: 'JSON',
	data: {
        product_id: product_id
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
		if(data.is_in_user_active_basket=='true'){
			$('.basketProduct').css('color','green');
			$('.basketProduct').addClass('addToBasket');
		}
		if(data.is_in_user_favorites=='true'){
			$('.likeProduct').css('color','red');
			$('.likeProduct').addClass('addToFavorite');
		}
		for(var i=0;i<data.images.length-2;i++){
			$('.images').prepend('<img class="dressImages" src="'+data.images[i+2].other+'">');
		}
	}
});
$(document).on('click touchstart','.basketProduct',function(){
	var thisElement=$(this);
	if(logged=="True"){
		if(!$(this).hasClass('addToBasket')){
			$.ajax({
				type: 'POST',
				url: '/api/store/add_to_basket/',
				dataType: 'JSON',
				data: {
			        product_id: $(this).attr('product_id')
			    },
				success: function (data) {
					thisElement.addClass('addToBasket');
					thisElement.css('color','green')
				}
			});
		}else{
			$.ajax({
				type: 'POST',
				url: '/api/store/remove_from_basket/',
				dataType: 'JSON',
				data: {
			        product_id: $(this).attr('product_id')
			    },
				success: function (data) {
					thisElement.removeClass('addToBasket');
					thisElement.css('color','inherit')
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
			        product_id: $(this).attr('product_id')
			    },
				success: function (data) {
					thisElement.addClass('addToFavorite');
					thisElement.css('color','red')
				}
			});
		}else{
			$.ajax({
				type: 'POST',
				url: '/api/customer/delete_favorite/',
				dataType: 'JSON',
				data: {
			        product_id: $(this).attr('product_id')
			    },
				success: function (data) {
					thisElement.removeClass('addToFavorite');
					thisElement.css('color','inherit')
				}
			});
		}
	}else{
		toastr.warning('ابتدا وارد سایت شوید.')
	}
});