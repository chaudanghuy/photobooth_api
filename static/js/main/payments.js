// Image slider
let scrollAmount = 0;
const scrollStep = 220;

// Load payments at start
$(document).ready(function () {    
    // Load payments
    loadPayments();
});

// Togggle add payment
$('.add-payment').on('click', function (e) {
    e.preventDefault();
    // Hide edit payment form
    $('.edit-payment-container').addClass('d-none');
    // Show add payment form
    $('.add-payment-container').removeClass('d-none');
});

// cancel add payment
$('.cancel-add-payment').on('click', function (e) {
    $('.add-payment-container').addClass('d-none');
    // reset form
    $('#add-payment-form')[0].reset();
});    

$('body').on('change', '.add-photo-input', function (e) {
    e.preventDefault();
    var input = this;    
    var photoPreview = $(this).parent().find('.photo_preview');
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            photoPreview.attr('src', e.target.result);
        }
        photoPreview.show();
       reader.readAsDataURL(input.files[0]);
    }
});

// Delete payment
// $('body').on('click', '.delete-payment', function (e) {
//     e.preventDefault()
//     if (confirm('Are you sure you want to delete this payment?') == true) {
//         var paymentId = $(this).data('payment-id');
//         var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
//         $.ajax({
//             url: '/payments/api/' + paymentId,
//             type: 'DELETE',
//             headers: {'X-CSRFToken': csrfToken},
//             success: function (response) {
//                 // reload payments
//                 loadPayments();
//             }
//         })
//     }
// });

// Edit payment
$('body').on('click', '.edit-payment', function (e) {
    e.preventDefault();
    // Hide add payment form
    $('.add-payment-container').addClass('d-none');

    var paymentId = $(this).data('payment-id');
    $.ajax({
        url: '/payments/api/' + paymentId,
        type: 'GET',
        success: function (response) {
            // Edit payment
            $('.edit-payment-container').removeClass('d-none');

            var editPaymentForm = $('#edit-payment-form');
            
            // Set values
            editPaymentForm.find('#payment_id').val(response.id);
            editPaymentForm.find('#name').val(response.name);
            editPaymentForm.find('#code').val(response.code);
            editPaymentForm.find('#method').val(response.method);
            editPaymentForm.find('#appID').attr('src', response.appID);
            editPaymentForm.find('#key1').attr('src', response.key1);
            editPaymentForm.find('#key2').attr('src', response.key2);
            editPaymentForm.find('#endpoint_sandbox').attr('src', response.endpoint_sandbox);
            editPaymentForm.find('#endpoint_prod').attr('src', response.endpoint_prod);
            editPaymentForm.find('#token').attr('src', response.token);
            editPaymentForm.find('#username').attr('src', response.username);
            editPaymentForm.find('#password').attr('src', response.password);
            editPaymentForm.find('#is_active').val(response.is_active);
        }
    })
});

// cancel edit payment
$('.cancel-edit-payment').on('click', function (e) {
    $('.edit-payment-container').addClass('d-none');
    // reset form
    $('#edit-payment-form')[0].reset();
});

$('#edit-payment-form').on('submit', function (e) {
    e.preventDefault();
    var paymentId = $('#payment_id').val();    
    var formData = new FormData(this);
    $.ajax({
        url: '/payments/api/' + paymentId,
        type: 'PUT',
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Reset form
            $('#edit-payment-form')[0].reset();
            // Hide 
            $('.edit-payment-container').addClass('d-none');

            // reload payments
            loadPayments();
        }
    })
});

$('body').on('change', '.edit-photo-input', function (e) {
    e.preventDefault();
    var input = this;    
    var photoPreview = $(this).parent().find('.photo_preview');
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            photoPreview.attr('src', e.target.result);
        }
        photoPreview.show();
       reader.readAsDataURL(input.files[0]);
    }
});

// Submit payment use multipart/form-data
$('#upload-payment-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/payments/api',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Reset form
            $('#upload-payment-form')[0].reset();
            // Hide
            $('.add-payment-container').addClass('d-none');
            
            // reload payments
            loadPayments();
        }
    })
});

/******************** FUNCTIONAILITY  ******************/
function loadPayments() {
    $('.api-loading').removeClass('d-none');
    $('.add-payment-container').addClass('d-none');
    $('.image-list-payments').empty();
    $.ajax({
        url: '/payments/api',
        type: 'GET',
        success: function (response) {
            $('.api-loading').addClass('d-none');
            // reload payments
            const payments = response;
            payments.forEach(payment => {
                $('.image-list-payments').append(
                    '<div class="image-container payment-image-container" data-payment-id="' + payment.id + '" data-payment-title="' + payment.name + '">' +
                    '<img src="' + loadPaymentPhoto(payment.name) + '" data-src="' + loadPaymentPhoto(payment.name) + '" alt="background" class="image-background">' +
                    '<div class="image-title">' + payment.name + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-payment text-decoration-none text-white" data-payment-id="' + payment.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +                    
                    '</div>' +
                    '</div>'
                )
            })
        }
    })
}

function loadPaymentPhoto(name) {
    if (name == 'Cash') {
        return 'https://cdn.icon-icons.com/icons2/550/PNG/512/business-color_payment_icon-icons.com_53442.png';
    } else if (name == 'Zalopay') {
        return 'https://cdn.freebiesupply.com/logos/large/2x/zalo-1-logo-svg-vector.svg';
    } else if (name == 'Momo') {
        return 'https://cdn.haitrieu.com/wp-content/uploads/2022/10/Logo-MoMo-Square.png';
    } else if (name == 'REDEEM') {
        return 'https://cdn.iconscout.com/icon/premium/png-512-thumb/redeem-code-2443710-2029122.png';
    }
}

$('body').on('click', '.nav-button.left', function () {
    const imageList = $(this).closest('.image-list-container').find('.image-list');
    scrollAmount = Math.max(0, scrollAmount - scrollStep);
    imageList.css('transform', 'translateX(-' + scrollAmount + 'px)');
});

$('body').on('click', '.nav-button.right', function () {
    const imageList = $(this).closest('.image-list-container').find('.image-list');
    const maxScroll = imageList[0].scrollWidth - imageList.width();
    scrollAmount = Math.min(maxScroll, scrollAmount + scrollStep);
    imageList.css('transform', 'translateX(-' + scrollAmount + 'px)');
});

