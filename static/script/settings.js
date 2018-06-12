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
$.ajax({
	type: 'GET',
	url: '/api/customer/get_addresses/',
	dataType: 'JSON',
	success: function (data) {
		
	},
	error: function(){
	}
});
$.ajax({
    type: 'GET',
    url: '/api/customer/get_user_info/',
    dataType: 'JSON',
    success: function (data) {
        $('#first_name').val(data.first_name)
        $('#last_name').val(data.last_name)
        $('#phone_number').val(data.phone_number)
    },
    error: function(){
    }
});
$(document).on('click touchstart','.fa-trash-alt',function(){
    $.ajax({
        type: 'GET',
        url: '/api/customer/delete_address/',
        dataType: 'JSON',
        success: function (data) {
            
        },
        error: function(){
            toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
        }
    });
})
$(document).on('click touchstart','.fa-edit',function(){
    $.ajax({
        type: 'GET',
        url: '/api/customer/edit_address/',
        dataType: 'JSON',
        success: function (data) {
            
        },
        error: function(){
            toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
        }
    });
})
$(document).on('click touchstart','#addAddrress',function(){
    $.ajax({
        type: 'GET',
        url: '/api/customer/edit_address/',
        dataType: 'JSON',
        success: function (data) {
            
        },
        error: function(){
        }
    });
})
$(document).on('click touchstart','#edit_info',function(){
    $.ajax({
        type: 'POST',
        url: '/api/customer/edit_user/',
        dataType: 'JSON',
        data:{
            first_name: $('#first_name').val(),
            last_name: $('#last_name').val(),
            phone_number: $('#phone_number').val()
        },
        success: function (data) {
            toastr.success('اطلاعات کاربری شما با موفقیت تغییر یافت.')
        },
        error: function(){
            toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
        }
    });
})
$(document).on('click touchstart','#changePassword',function(){
    $.ajax({
        type: 'POST',
        url: '/api/customer/change_password/',
        dataType: 'JSON',
        data:{
            old_password: $('#old_pass').val(),
            new_password: $('#new_pass').val(),
            new_password_confirm: $('#new_pass_repeat').val()
        },
        success: function (data) {
            toastr.success('رمز شما با موفقیت تغییر یافت.')
        },
        error: function(){
            toastr.error('مشکلی خ داده است. لطفا ممجددا امتحان کنید.')
        }
    });
})