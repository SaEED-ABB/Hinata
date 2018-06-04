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
	if(window.innerWidth>768){
		if($('.menu').css('display')=='none'){
			$('.menu').slideDown();
		}else{
			$('.menu').slideUp();
		}
	}
});
$(document).on('click touchstart','#entrance',function(){
	console.log($('[name=phone_number]').text());
	$.ajax({
		type: 'POST',
		url: '/api/customer/login/',
		dataType: 'JSON',
		data: {
	        phone_number:$('[name=phone_numberL]').val(),
	        password: $('[name=passwordL]').val()
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
	        first_name:$('[name=first_nameR]').val(),
	        last_name:$('[name=last_nameR]').val(),
	        phone_number:$('[name=phone_numberR]').val(),
	        password1:$('[name=password1R]').val(),
	        password2: $('[name=password2R]').val()
	    },
		success: function (data) {
			$('.registerPopBack').fadeOut();
			$('.registerPop').fadeOut();
		}
	});
});
/* Set the width of the side navigation to 250px */
function openNav() {
	if(window.innerWidth<=768){
    	document.getElementById("mySidenav").style.width = "250px";
    	$('.shadow').css('display','block')
    }
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    $('.shadow').css('display','none')
}