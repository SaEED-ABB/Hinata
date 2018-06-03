$.ajax({
	type: 'GET',
	url: '/api/store/get_history/',
	dataType: 'JSON',
	success: function (data) {
		$('.openOrdersTable').html('<tr class="trHead">'+
    			'<th>ردیف</th>'+
    			'<th>کد سفارش</th>'+
    			'<th>تاریخ ثبت</th>'+
    			'<th>قیمت</th>'+
    			'<th>آدرس</th>'+
    			'<th>وضعیت</th>'+
    			'<th></th>'+
    		'</tr>');
		for (var i =0; data.open.length >i; i++) {
			$('.openOrdersTable').append('<tr class="oOrder'+i+'">'+
    			'<td>'+i+'</td>'+
    			'<td>KJ093640GS</td>'+
    			'<td>27/06/1396 <br> 23:59</td>'+
    			'<td>'+data.open[i].total_price+'</td>'+
    			'<td>تهران-خیابان انقلاب-خیابان وصال-کوچه شاهد-پلاک 2</td>'+
    			statusTdMaker(data.open[i].status)+
    			'<td><i class="fas fa-angle-down"></i></td>'+
    		'</tr>'+
    		'<tr class="oOrder'+i+'">'+
    			'<td colspan="7">'+
    				'<div class="secondTableContainer">'+
    					'<table>'+
    						'<tr  class="trHead">'+
    							'<th>کلا</th>'+
    							'<th>رنگ</th>'+
    							'<th>سایز</th>'+
    							'<th>تعداد</th>'+
    							'<th>قیمت</th>'+
    						'</tr>'+
    						makeProductTables(data.open[i].products)+
    					'</table>'+
    				'</div>'+
    				'<div class="secondTableContainer">'+
    					'<table>'+
    						'<tr  class="trHead">'+
    							'<th>بررسی سفارش</th>'+
    							'<th>آماده ساززی</th>'+
    							'<th>ارسال</th>'+
    							'<th>تحویل کالا</th>'+
    						'</tr>'+
    						'<tr>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img1.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img2.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img3.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img4.jpg">'+
    							'</td>'+
    						'</tr>'+
    						'<tr>'+
    							'<td>'+
    							'</td>'+
    							'<td>'+
    								'<div class="color" color_slug="'+data.open[i].products+'" style="background-color:red"></div>'+
    							'</td>'+
    							'<td>'+
    								'<div class="size" size_slug="'+data.open[i].products+'">46</div>'+
    							'</td>'+
    							'<td>2</td>'+
    						'</tr>'+
    					'</table>'+
    				'</div>'+
    				'<div class="secondTableContainer"></div>'+
    			'</td>'+
    		'</tr>');
		}
		$('.closedOrdersTable').html('<tr class="trHead">'+
    			'<th>ردیف</th>'+
    			'<th>کد سفارش</th>'+
    			'<th>تاریخ ثبت</th>'+
    			'<th>قیمت</th>'+
    			'<th>آدرس</th>'+
    			'<th>وضعیت</th>'+
    			'<th></th>'+
    		'</tr>');
		for (var i =0; data.closed.length >i; i++) {
			$('.closedOrdersTable').append('<tr class="cOrder'+i+'">'+
    			'<td>1</td>'+
    			'<td>KJ093640GS</td>'+
    			'<td>27/06/1396 <br> 23:59</td>'+
    			'<td>'+data.closed[i].total_price+'</td>'+
    			'<td>تهران-خیابان انقلاب-خیابان وصال-کوچه شاهد-پلاک 2</td>'+
    			statusTdMaker(data.closed[i].status)+
    			'<td><i class="fas fa-angle-down"></i></td>'+
    		'</tr>'+
    		'<tr class="cOrder'+i+'">'+
    			'<td colspan="7">'+
    				'<div class="secondTableContainer">'+
    					'<table>'+
    						'<tr  class="trHead">'+
    							'<th>کلا</th>'+
    							'<th>رنگ</th>'+
    							'<th>سایز</th>'+
    							'<th>تعداد</th>'+
    							'<th>قیمت</th>'+
    						'</tr>'+
    						makeProductTables(data.closed[i].products)+
    					'</table>'+
    				'</div>'+
    				'<div class="secondTableContainer">'+
    					'<table>'+
    						'<tr  class="trHead">'+
    							'<th>بررسی سفارش</th>'+
    							'<th>آماده ساززی</th>'+
    							'<th>ارسال</th>'+
    							'<th>تحویل کالا</th>'+
    						'</tr>'+
    						'<tr>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img1.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img2.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img3.jpg">'+
    							'</td>'+
    							'<td>'+
    								'<img class="levelsImg" src="/static/img/img4.jpg">'+
    							'</td>'+
    						'</tr>'+
    						'<tr>'+
    							'<td>'+
    							'</td>'+
    							'<td>'+
    								'<div class="color" color_slug="'+data.closed[i].total_price+'" style="background-color:red"></div>'+
    							'</td>'+
    							'<td>'+
    								'<div class="size" size_slug="'+data.closed[i].total_price+'">46</div>'+
    							'</td>'+
    							'<td>2</td>'+
    						'</tr>'+
    					'</table>'+
    				'</div>'+
    				'<div class="secondTableContainer"></div>'+
    			'</td>'+
    		'</tr>');
		}
	},
	error: function(){
	}
});
function makeProductTables(array){
	var text="";
	for (var i =0; array.length >i; i++) {
			text+='<tr>'+
						'<td>'+
							'<img class="productImg" src="'+array[i].image+'">'+
							'<br>'+
							'<h3>'+array[i].name+'</h3>'+
						'</td>'+
						'<td>'+
							'<div class="color" color_slug="" style="background-color:'+array[i].desired_color+'"></div>'+
						'</td>'+
						'<td>'+
							'<div class="size" size_slug="">'+array[i].desired_size+'</div>'+
						'</td>'+
						'<td>'+array[i].count+'</td>'+
						'<td>'+array[i].price+'</td>'+
					'</tr>'
		}
	return text;
}
$(document).on('click','.fa-angle-down',function(){
	var thisEle=$(this)
	thisEle.attr('data-fa-transform','rotate-90')
	console.log(thisEle.parent().parent().attr('class'))
	thisEle.parent().parent().siblings('.'+thisEle.parent().parent().attr('class')).slideUp(2000)
})
function statusTdMaker(status){
	var statusType=status.split('_')[0]
	var statusLevel=status.split('_')[1]
	if(statusType=='open'){
		if(statusLevel=='checking'){
			return '<td class="yellowBack">در حال بررسی</td>'
		}else if(statusLevel=='preparing'){
			return '<td class="yellowBack">در حال آماده سازی</td>'
		}else if(statusLevel=='sending'){
			return '<td class="yellowBack">در حال ارسال</td>'
		}
	}else{
		if(statusLevel=='canceled'){
			return '<td class="redBack">لغو سفارش</td>'
		}else if(statusLevel=='returned'){
			return '<td class="redBack">بازگشت کالا</td>'
		}else if(statusLevel=='delivered'){
			return '<td class="greenBack">تحویل سفارش</td>'
		}
	}
}