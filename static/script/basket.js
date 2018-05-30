$.ajax({
	type: 'GET',
	url: '/api/store/get_active_basket_info/',
	dataType: 'JSON',
	success: function (data) {
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
			$('.basketContainer').append('<div class="row" product_slug="'+data.products[i].slug+'">'+
	    		'<div class="removeCol"><i class="fas fa-times" product_slug="'+data.products[i].slug+'"></i></div>'+
	    		'<div class="prodCol"></div>'+
	    		'<div class="colorCol">'+makeColors(data.products[i].colors, data.products[i].slug)+'</div>'+
	    		'<div class="sizeCol">'+makeSizes(data.products[i].sizes, data.products[i].slug)+'</div>'+
	    		'<div class="numCol">تعداد</div>'+
	    		'<div class="priceCol">قیمت</div>'+
	    	'</div>');
		}
	},
	error: function(){

	}
});
function makeColors(array,slug){
	for (var i =0; i < array.length; i++) {
		$('.row[product_slug="'+slug+'"] .colorCol').append('<div class="color" color_slug="'+array[i].slug+'" style="background-color:'+array[i].code+'"></div>')
	}
}
function makeSizes(array,slug){
	for (var i =0; i < array.length; i++) {
		$('.row[product_slug="'+slug+'"] .sizeCol').append('<div class="size" size_slug="'+array[i].slug+'">'+array[i].name+'></div>')
	}
}