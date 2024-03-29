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
	$('.moreButton img').addClass('spin');
	var data={};
	data.page=pageCount;
	data.category="s"
	for (var i = 0; $('.selectBoxes').find('select').length >i; i++) {
		if(i==0){
			data.filter_slug_sort_by=$('.selectBoxes').find('select').eq(i).attr('filter_slug')
			data.filter_option_slug_sort_by=$('.selectBoxes').find('select').eq(i).val()
		}
		if(i==1){
			data.filter_slug_1=$('.selectBoxes').find('select').eq(i).attr('filter_slug')
			data.filter_option_slug_1=$('.selectBoxes').find('select').eq(i).val()
		}
		if(i==2){
			data.filter_slug_2=$('.selectBoxes').find('select').eq(i).attr('filter_slug')
			data.filter_option_slug_2=$('.selectBoxes').find('select').eq(i).val()
		}
		
	}
	$.ajax({
		type: 'GET',
		url: '/api/store/get_products',
		dataType: 'JSON',
		data:data,
		success: function (data) {
			for(var i=0; i<data.products.length;i++){
				if(data.products[i].is_in_user_favorites){
					var favoriteText="<i class='fas fa-heart likeProduct addToFavorite' style='color:red;font-size:26px;' product_slug="+data.products[i].slug+" ></i>";
				}else{
					var favoriteText="<i class='fas fa-heart likeProduct' style='color:#949494;font-size:26px;' product_slug="+data.products[i].slug+" ></i>";
				}
				if(data.products[i].is_in_user_active_basket){
					var basketText="<i class='fas fa-shopping-basket basketProduct addToBasket' style='color:#00da00;font-size:26px;' product_slug="+data.products[i].slug+"></i>";
				}else{
					var basketText="<i class='fas fa-shopping-basket basketProduct' style='color:#949494;font-size:26px;' product_slug="+data.products[i].slug+"></i>";
				}
				$('.cards').append("<div class='pCard'>"+
						"<a class='link' href='/store/product/"+data.products[i].slug+"' >"+
							"<img class='img-responsive front' src="+data.products[i].front_image+" />" +
							"<img class='img-responsive back' style='display: none;' src="+data.products[i].back_image+" />"+
						"</a>"+
						'<div class="swiper-container" style="display:none">'+
						    '<div class="swiper-wrapper">'+
						    	"<div class='swiper-slide'><img src="+data.products[i].front_image+" /></div>"+
								"<div class='swiper-slide'><img src="+data.products[i].back_image+" /></div>"+
						    '</div>'+
						    '<div class="swiper-pagination"></div>'+
						'</div>'+
						"<a class='' href='/store/product/"+data.products[i].slug+"' >"+
							"<h4 class='text-center' style='margin-top: 16px;margin-bottom: 20px;'>"+data.products[i].name+"</h4>"+
						"</a>"+
						"<div class='row' style='margin-bottom: 15px;'> "+
							"<div class='col-sm-6 cardIcons' style='margin-top: 6px;'> "+
								basketText+
								favoriteText+
							"</div> "+
							"<div class='col-sm-6 cardPrice'> "+
								"<span class='productPrice'>"+data.products[i].price+"</span>"+
							"</div>"+
						"</div> "+
					"</div>"
				);
				$('.moreButton img').removeClass('spin');
				var swiper = new Swiper('.swiper-container', {
			      	pagination: {
				        el: '.swiper-pagination',
				        dynamicBullets: true,
			      	},
			    });
			}
			if(!data.more){
				$('.moreButton').css('display','none');
			}else{
				pageCount=pageCount+1;
			}
		},
		error: function(){
			toastr.error('بارگذاری محصولات با مشکل مواجه شده است. لطفا صفحه را بارگذاری مجدد نمایید.')
			$('.moreButton img').removeClass('spin');
		}
	});
}
$(document).on('mouseenter','.pCard a',function(){
	$(this).find('.front').css('display','none');
	$(this).find('.back').fadeIn(50);
});
$(document).on('mouseleave','.pCard a',function(){
	$(this).find('.front').fadeIn(50);
	$(this).find('.back').css('display','none');
});
$(document).on('click touchstart','.moreButton img',function(){
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
$(document).ready(function(){
	var swiper = new Swiper('.swiper-container', {
      pagination: {
        el: '.swiper-pagination',
        dynamicBullets: true,
      },
    });
})
$(document).on('change','select',function(){
	$('.cards').html('');
	getProducts();
});
