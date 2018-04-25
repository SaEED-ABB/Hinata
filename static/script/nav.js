$(document).ready(function(){
	$(window).scroll(function(){
		if(window.top.pageYOffset>=94){
			$('.smallNav').css('display','block');
		}else{
			$('.smallNav').css('display','none');
		}
	});
});

$(document).on('click touchstart','.loginButton',function(){
	$('.loginPopBack').fadeIn();
	$('.loginPop').fadeIn();
});
$(document).on('click touchstart','.loginPopBack:not(.loginPop)',function(){
	$('.loginPopBack').fadeOut();
	$('.loginPop').fadeOut();
});
$(document).on('click touchstart','.menuBarImg',function(){
	if($('.menu').css('display')=='none'){
		$('.menu').slideDown();
	}else{
		$('.menu').slideUp();
	}
});