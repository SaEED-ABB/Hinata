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

$.ajax({
	type: 'GET',
	url: '/api/customer/get_favorites/',
	dataType: 'JSON',
	success: function (data) {
		$('.favoriteContainer').html('');
		for (var i =0; i < data.length; i++) {
			// if(data.products[i].is_in_basket){
			// 	var basketText="<i class='fas fa-shopping-basket basketProduct addToBasket' style='color:#00da00;' product_slug="+data.products[i].slug+"></i>";
			// }else{
			// 	var basketText="<i class='fas fa-shopping-basket basketProduct' style='color:#949494;font-size:26px;' product_slug="+data.products[i].slug+"></i>";
			// }
			$('.favoriteContainer').append('<div class="row" style="margin-bottom: 40px;">'+
	    		'<div class="row">'+
	    			'<img src="'+data[i].images[0].url+'" class="favoriteImg">'+
	    			'<img src="'+data[i].images[1].url+'" class="favoriteImg">'+
	    			'<img src="'+data[i].images[2].url+'" class="favoriteImg">'+
	    		'</div>'+
	    		'<div class="row">'+
		    		'<div class="col-sm-4 col-sm-offset-4 col-xs-12">'+
			    		'<div class="row">'+
			    			"<a class='' href='/store/product/"+data[i].product_slug+"' >"+
								"<h3 class='text-center' style='margin-top: 16px;margin-bottom: 20px;'>"+data[i].product_name+"</h3>"+
							"</a>"+
						'</div>'+
						"<div class='row' style='margin-bottom: 15px;'> "+
							"<div class='col-sm-6 cardIcons text-right' style='margin-top: 6px;'> "+
								'<i class="fas fa-times" product_slug="'+data[i].product_slug+'" style="color:#949494;font-size:26px;color:red;margin-left: 10%;"></i>'+
								'<i class="fas fa-shopping-basket basketProduct" style="color:#949494;font-size:26px;" product_slug="'+data[i].product_slug+'"></i>'+
							"</div> "+
							"<div class='col-sm-6 cardPrice text-left'> "+
								"<span class='productPrice'>"+data[i].price+"</span>"+
							"</div>"+
						"</div> "+
		    		'</div>'+
	    		'</div>'+
    		'</div>');
		}
	},
	error: function(){

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
$(document).on('click','.fa-times',function(){
	var parentElement=$(this).parent().parent().parent().parent().parent()
	$.ajax({
		type: 'POST',
		url: '/api/customer/delete_favorite/',
		dataType: 'JSON',
		data: {
	        product_slug: $(this).attr('product_slug')
	    },
		success: function (data) {
			parentElement.remove()
			toastr.success('محصول مورد نظر از سبد خرید حذف شد.')
		},
		error: function(){
			toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
		}
	});
})