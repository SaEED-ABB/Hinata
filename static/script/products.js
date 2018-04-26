var pageCount=1;
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
				if(data.products[i].favorite){
					var favoriteText="<img src='/static/img/liked.png' product_id="+data.products[i].id+" class='likeProduct addToFavorite'>";
				}else{
					var favoriteText="<img src='/static/img/like.png' product_id="+data.products[i].id+" class='likeProduct'>";
				}
				if(data.products[i].basket){
					var basketText="<img src='/static/img/basketed.png' product_id="+data.products[i].id+" class='basketProduct addToBasket'>";
				}else{
					var basketText="<img src='/static/img/basket.png' product_id="+data.products[i].id+" class='basketProduct '>";
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
	if(!$(this).hasClass('addToBasket')){
		$.ajax({
			type: 'GET',
			url: '/api/store/add_to_basket',
			dataType: 'JSON',
			data: {
		        size: 's',
		        color:'sdaf',
		        product: $(this).attr('product_id')
		    },
			success: function (data) {
				thisElement.addClass('addToBasket');
				thisElement.attr('src','/static/img/basketed.png')
			}
		});
	}else{
		$.ajax({
			type: 'GET',
			url: '/api/store/add_to_basket',
			dataType: 'JSON',
			data: {
		        size: 's',
		        color:'sdaf',
		        product: $(this).attr('product_id')
		    },
			success: function (data) {
				thisElement.removeClass('addToBasket');
				thisElement.attr('src','/static/img/basket.png')
			}
		});
	}
});
$(document).on('click touchstart','.likeProduct',function(){
	if(!$(this).hasClass('addToFavorite')){
		$.ajax({
			type: 'GET',
			url: '/api/store/add_favorite',
			dataType: 'JSON',
			data: {
		        product: $(this).attr('product_id')
		    },
			success: function (data) {
				thisElement.addClass('addToFavorite');
				thisElement.attr('src','/static/img/liked.png')
			}
		});
	}else{
		$.ajax({
			type: 'GET',
			url: '/api/store/delete_favorite',
			dataType: 'JSON',
			data: {
		        product: $(this).attr('product_id')
		    },
			success: function (data) {
				thisElement.removeClass('addToFavorite');
				thisElement.attr('src','/static/img/like.png')
			}
		});
	}
});