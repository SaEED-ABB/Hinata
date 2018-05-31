$.ajax({
	type: 'GET',
	url: '/api/store/get_active_basket_info/',
	dataType: 'JSON',
	success: function (data) {
		var total_count=0;
		$('.basketContainer').html('');
		$('.basketContainer').append('<div class="row">'+
	    		'<div class="removeCol"></div>'+
	    		'<div class="prodCol">کالا</div>'+
	    		'<div class="colorCol">رنگ</div>'+
	    		'<div class="sizeCol">سایز</div>'+
	    		'<div class="numCol">تعداد</div>'+
	    		'<div class="priceCol">قیمت</div>'+
	    	'</div>');
			
		for (var i =0; data.products.length >i; i++) {
			total_count+=data.products[i].count;
			$('.basketContainer').append('<div class="row" product_slug="'+data.products[i].slug+'">'+
	    		'<div class="removeCol"><i class="fas fa-times" product_slug="'+data.products[i].slug+'"></i></div>'+
	    		'<div class="prodCol">'+
	    			'<h3>'+data.products[i].name+'</h3>'+
	    			'<img src="'+data.products[i].image+'" class="prodImg">'+
	    		'</div>'+
	    		'<div class="colorCol">'+makeColors(data.products[i].colors, data.products[i].slug)+'</div>'+
	    		'<div class="sizeCol">'+makeSizes(data.products[i].sizes, data.products[i].slug)+'</div>'+
	    		'<div class="numCol"><input  class="scale" type="number" value="'+data.products[i].count+'"></div>'+
	    		'<div class="priceCol">'+data.products[i].price+'</div>'+
	    	'</div>');
		}
		$('.basketContainer').append('<div class="row withoutBorder">'+
	    		'<div class="removeCol"></div>'+
	    		'<div class="prodCol"><button class="bigButton">خرید</button></div>'+
	    		'<div class="colorCol"></div>'+
	    		'<div class="sizeCol"></div>'+
	    		'<div class="numCol">'+total_count+'</div>'+
	    		'<div class="priceCol">'+data.total_price+'</div>'+
	    	'</div>');
	},
	error: function(){

	}
});
function makeColors(array,slug){
	var text="";
	for (var i =0; i < array.length; i++) {
		text+='<div class="color" color_slug="'+array[i].slug+'" style="background-color:'+array[i].code+'"></div>';
	}
	return text;
}
function makeSizes(array,slug){
	var text="";
	for (var i =0; i < array.length; i++) {
		text+='<div class="size" size_slug="'+array[i].slug+'">'+array[i].name+'</div>';
	}
	return text;
}
$(document).on('click','.fa-times',function(){
	var parentElement=$(this).parent().parent()
	$.ajax({
		type: 'POST',
		url: '/api/store/remove_from_basket/',
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