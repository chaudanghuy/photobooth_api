// Image slider
let scrollAmount = 0;
const scrollStep = 220;

/******************** STICKER  ******************/
$(document).ready(function () {
    // Load stickers
    loadStickers();
});

// Togggle add sticker
$('.add-sticker').on('click', function (e) {
    e.preventDefault();
    // Hide edit sticker form
    $('.edit-sticker-container').addClass('d-none');
    // Show add sticker form
    $('.add-sticker-container').removeClass('d-none');
});

// cancel add sticker
$('.cancel-add-sticker').on('click', function (e) {
    $('.add-sticker-container').addClass('d-none');
    // reset form
    $('#add-sticker-form')[0].reset();
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

// Delete sticker
$('body').on('click', '.delete-sticker', function (e) {
    e.preventDefault()
    if (confirm('Are you sure you want to delete this sticker?') == true) {
        var stickerId = $(this).data('sticker-id');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/stickers/api/' + stickerId,
            type: 'DELETE',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                // reload stickers
                loadStickers();
            }
        })
    }
});

// Edit sticker
$('body').on('click', '.edit-sticker', function (e) {
    e.preventDefault();
    // Hide add sticker form
    $('.add-sticker-container').addClass('d-none');

    var stickerId = $(this).data('sticker-id');
    $.ajax({
        url: '/stickers/api/' + stickerId,
        type: 'GET',
        success: function (response) {
            // Edit sticker
            $('.edit-sticker-container').removeClass('d-none');

            var editStickerForm = $('#edit-sticker-form');
            
            // Set values
            editStickerForm.find('#sticker_id').val(response.id);
            editStickerForm.find('#category').val(response.category);
            editStickerForm.find('#title').val(response.title);
            editStickerForm.find('#device_id').val(response.device_id);
            editStickerForm.find('#photo_preview').attr('src', response.photo);
        }
    })
});

// cancel edit sticker
$('.cancel-edit-sticker').on('click', function (e) {
    $('.edit-sticker-container').addClass('d-none');
    // reset form
    $('#edit-sticker-form')[0].reset();
});

$('#edit-sticker-form').on('submit', function (e) {
    e.preventDefault();
    var stickerId = $('#sticker_id').val();    
    var formData = new FormData(this);
    $.ajax({
        url: '/stickers/api/' + stickerId,
        type: 'PUT',
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Reset form
            $('#edit-sticker-form')[0].reset();
            // Hide 
            $('.edit-sticker-container').addClass('d-none');

            // reload stickers
            loadStickers();
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

// Submit sticker use multipart/form-data
$('#upload-sticker-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/stickers/api',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Reset form
            $('#upload-sticker-form')[0].reset();
            // Hide
            $('.add-sticker-container').addClass('d-none');
            
            // reload stickers
            loadStickers();
        }
    })
});


/******************** FUNCTIONAILITY  ******************/
function loadStickers() {
    $('.api-loading').removeClass('d-none');
    $('.add-sticker-container').addClass('d-none');
    $('.image-list-stickers').empty();
    $.ajax({
        url: '/stickers/api',
        type: 'GET',
        success: function (response) {
            $('.api-loading').addClass('d-none');
            // reload stickers
            const stickers = response;
            stickers.forEach(sticker => {
                $('.image-list-stickers').append(
                    '<div class="image-container sticker-image-container" data-background-id="' + sticker.id + '" data-background-title="' + sticker.title + '">' +
                    '<img src="' + sticker.photo + '" data-src="' + sticker.photo + '" alt="background" class="image-background">' +
                    '<div class="image-title">' + sticker.title + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-sticker text-decoration-none text-white" data-sticker-id="' + sticker.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +
                    '<button class="delete-button">' +
                    '<a class="delete-sticker text-decoration-none text-white" data-sticker-id="' + sticker.id + '">' +
                    '<span class="mdi mdi-trash-can"></span> Delete</a>' +
                    '</button>' +
                    '</div>' +
                    '</div>'
                )
            })
        }
    })
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