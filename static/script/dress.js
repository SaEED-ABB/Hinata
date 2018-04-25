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
