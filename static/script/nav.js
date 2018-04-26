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
$(document).on('click touchstart','.loginPopBack',function(e){
	if(e.target !== e.currentTarget) return;
	$('.loginPopBack').fadeOut();
	$('.loginPop').fadeOut();
});
$(document).on('click touchstart','.registerButton',function(){
	$('.registerPopBack').fadeIn();
	$('.registerPop').fadeIn();
});
$(document).on('click touchstart','.registerPopBack',function(e){
	if(e.target !== e.currentTarget) return;
	$('.registerPopBack').fadeOut();
	$('.registerPop').fadeOut();
});
$(document).on('click touchstart','.menuBarImg',function(){
	if($('.menu').css('display')=='none'){
		$('.menu').slideDown();
	}else{
		$('.menu').slideUp();
	}
});
$(document).on('click touchstart','#entrance',function(){
	$.ajax({
		type: 'POST',
		url: '/api/customer/login/',
		dataType: 'JSON',
		data: {
	        username:$('[name=usernameL]').html(),
	        password: $('[name=passwordL]').html()
	    },
		success: function (data) {
			$('.loginPopBack').fadeOut();
			$('.loginPop').fadeOut();
		}
	});
});
$(document).on('click touchstart','#signup',function(){
	$.ajax({
		type: 'POST',
		url: '/api/customer/register/',
		dataType: 'JSON',
		data: {
	        firstname:$('[name=firstnameR]').html(),
	        lastname:$('[name=lastnameR]').html(),
	        email:$('[name=numberR]').html(),
	        password: $('[name=passwordR]').html()
	    },
		success: function (data) {
			$('.registerPopBack').fadeOut();
			$('.registerPop').fadeOut();
		}
	});
});