var pageCount=1;

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

getProducts();
function getProducts(){
	$.ajax({
		type: 'GET',
		url: '/api/store/get_products',
		dataType: 'JSON',
		data: {
	        category: 's',
	        page: pageCount
	    },
		success: function (data) {
			for(var i=0; i<data.products.length;i++){
				if(data.products[i].is_favorite){
					var favoriteText="<i class='fas fa-heart likeProduct addToFavorite' style='color:red;' product_id="+data.products[i].id+" ></i>";
				}else{
					var favoriteText="<i class='fas fa-heart likeProduct' product_id="+data.products[i].id+" ></i>";
				}
				if(data.products[i].is_in_basket){
					var basketText="<i class='fas fa-shopping-basket basketProduct addToBasket' style='color:green;' product_id="+data.products[i].id+"></i>";
				}else{
					var basketText="<i class='fas fa-shopping-basket basketProduct' product_id="+data.products[i].id+"></i>";

				}
				$('.cards').append("<div class='pCard'>"+
						"<a class='link' href='#' >"+
							"<img class='img-responsive front' src="+data.products[i].front_image+" />" +
							"<img class='img-responsive back' style='display: none;' src="+data.products[i].back_image+" />"+
							"<h4 class='text-center' style='margin-top: 16px;margin-bottom: 20px;'>"+data.products[i].name+"</h4>"+
							"<div class='row' style='margin-bottom: 15px;'> "+
								"<div class='col-sm-6 cardIcons' style='margin-top: 6px;'> "+
									basketText+
									favoriteText+
								"</div> "+
								"<div class='col-sm-6 cardPrice'> "+
									"<span class='productPrice'>"+data.products[i].price+"</span>"+
								"</div>"+
							"</div> "+
						"</a>"+
					"</div>"
				);
			}
			if(!data.more){
				$('.moreButton').css('display','none');
			}else{
				pageCount=pageCount+1;
			}
		}
	});
}
$(document).on('mouseenter','.pCard a',function(){
	$(this).find('.front').css('display','none');
	$(this).find('.back').fadeIn();
});
$(document).on('mouseleave','.pCard a',function(){
	$(this).find('.front').fadeIn();
	$(this).find('.back').css('display','none');
});
$(document).on('click touchstart','.moreButton',function(){
	getProducts();
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
				url: '/api/store/remove_to_basket/',
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