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
    			'<td>'+(i+1)+'</td>'+
    			'<td>'+data.open[i].code+'</td>'+
    			'<td> '+data.open[i].paid_at.day+'/'+data.open[i].paid_at.month+'/'+data.open[i].paid_at.year+' <br> '+data.open[i].paid_at.minute+':'+data.open[i].paid_at.second+'</td>'+
    			'<td>'+data.open[i].total_price+'</td>'+
    			'<td>'+data.open[i].address+'</td>'+
    			statusTdMaker(data.open[i].status)+
    			'<td><i class="fas fa-angle-down"></i></td>'+
    		'</tr>'+
    		'<tr class="oOrder'+i+'" style="display:none">'+
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
    						makeStatusRows(data.open[i].status)+
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
    			'<td>'+(i+1)+'</td>'+
    			'<td>'+data.closed[i].code+'</td>'+
    			'<td> '+data.closed[i].paid_at.day+'/ '+data.closed[i].paid_at.month+'/ '+data.closed[i].paid_at.year+' <br> '+data.closed[i].paid_at.minute+':'+data.closed[i].paid_at.second+'</td>'+
    			'<td>'+data.closed[i].total_price+'</td>'+
    			'<td>'+data.closed[i].address+'</td>'+
    			statusTdMaker(data.closed[i].status)+
    			'<td><i class="fas fa-angle-down"></i></td>'+
    		'</tr>'+
    		'<tr class="cOrder'+i+'" style="display:none">'+
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
    						makeStatusRows(data.closed[i].status)+
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
var rotate_factor=0
jQuery.fn.rotate = function(degrees) {
    $(this).css({'transform' : 'rotate('+ degrees +'deg)','transition':'all 0.3s'});
    return $(this);
};
$(document).on('click','.fa-angle-down',function(e){
    var thisEle=$(this)
    if(rotate_factor%2!=0){
        thisEle.parent().parent().siblings('.'+thisEle.parent().parent().attr('class')).slideUp(100)        
    }else{
        thisEle.parent().parent().siblings('.'+thisEle.parent().parent().attr('class')).slideDown(100)
    }
    rotate_factor += 1;
    var rotate_angle = (180 * rotate_factor) % 360;
    thisEle.rotate(rotate_angle);
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
		}else{
            return '<td class="greenBack">تحویل سفارش</td>'
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
function makeStatusRows(status){
	var statusType=status.split('_')[0]
	var statusLevel=status.split('_')[1]

	if(statusLevel=='checking'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img style="width:50px" src="/static/img/comp.gif">'+
    			'</td><td>'+
    				'<img class="levelsImg " src="/static/img/img2.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span  class="linkButtonAllow" data-toggle="modal" data-target="#cancelOrderModal">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButton">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButton">بازگشت کالا</span>'+
    			'</td></tr>'
	}else if(statusLevel=='preparing'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img2.jpg"><br><img  style="width:50px" src="/static/img/comp.gif">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButtonAllow" data-toggle="modal" data-target="#cancelOrderModal">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButton">بازگشت کالا</span>'+
    			'</td></tr>'
	}else if(statusLevel=='sending'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img2.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img  style="width:50px"  src="/static/img/comp.gif">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButton">بازگشت کالا</span>'+
    			'</td></tr>'
    }else if(statusLevel=='delivering'){
        return  '<tr><td>'+
                    '<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
                '</td><td>'+
                    '<img class="levelsImg" src="/static/img/img2.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
                '</td><td>'+
                    '<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
                '</td><td>'+
                    '<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
                '</td></tr>'+
                '<tr><td>'+
                    '<span  class="linkButtonDis">لغو سفارش</span>'+
                '</td><td>'+
                    '<span  class="linkButtonDis">لغو سفارش</span>'+
                '</td><td>'+
                    
                '</td><td>'+
                    '<span  class="linkButtonAllow" data-toggle="modal" data-target="#backOrderModal">بازگشت کالا</span>'+
                '</td></tr>'
	}else if(statusLevel=='canceled'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img2.jpg"><br><i class="fas fa-times-circle tickImg" style="font-size: 41px;color:red"></i>'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/more.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButtonDis">بازگشت کالا</span>'+
    			'</td></tr>'
	}else if(statusLevel=='returned'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img2.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButtonDis">بازگشت کالا</span>'+
    			'</td></tr>'
	}else if(statusLevel=='delivered'){
		return 	'<tr><td>'+
    				'<img class="levelsImg" src="/static/img/img1.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img2.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img3.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td><td>'+
    				'<img class="levelsImg" src="/static/img/img4.jpg"><br><img class="tickImg" src="/static/img/tick.png">'+
    			'</td></tr>'+
    			'<tr><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				'<span  class="linkButtonDis">لغو سفارش</span>'+
    			'</td><td>'+
    				
    			'</td><td>'+
    				'<span  class="linkButtonDis">بازگشت کالا</span>'+
    			'</td></tr>'
	}

}