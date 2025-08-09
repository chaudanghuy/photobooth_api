// Image slider
let scrollAmount = 0;
const scrollStep = 220;

// Load frames at start
$(document).ready(function () {    
    // Load frames
    loadFrames();
});

// Togggle add frame
$('.add-frame').on('click', function (e) {
    e.preventDefault();
    // Hide edit frame form
    $('.edit-frame-container').addClass('d-none');
    // Show add frame form
    $('.add-frame-container').removeClass('d-none');
});

// cancel add frame
$('#cancel-add-frame').on('click', function (e) {
    $('.add-frame-container').addClass('d-none');
    // reset form
    $('#add-frame-form')[0].reset();
});    

// Delete frame
$('body').on('click', '.delete-frame', function (e) {
    e.preventDefault()
    if (confirm('Are you sure you want to delete this frame?') == true) {
        var frameId = $(this).data('frame-id');
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url: '/frames/api/' + frameId + '/delete',
            type: 'DELETE',
            headers: {'X-CSRFToken': csrfToken},
            success: function (response) {
                // reload frames
                loadFrames();
            }
        })
    }
});

// Edit frame
$('body').on('click', '.edit-frame', function (e) {
    e.preventDefault();
    // Hide add frame form
    $('.add-frame-container').addClass('d-none');

    var frameId = $(this).data('frame-id');
    $.ajax({
        url: '/frames/api/' + frameId,
        type: 'GET',
        success: function (response) {
            // Edit frame
            $('.edit-frame-container').removeClass('d-none');

            var editFrameForm = $('#edit-frame-form');
            
            // Set values
            editFrameForm.find('#frame_id').val(response.id);
            editFrameForm.find('#title').val(response.title);
            editFrameForm.find('#position').val(response.position);
            editFrameForm.find('#device_id').val(response.device_id);
            editFrameForm.find('#photo_preview').attr('src', response.photo);
            editFrameForm.find('#photo_hover_preview').attr('src', response.photo_hover);
            editFrameForm.find('#price').val(response.price);
            editFrameForm.find('#id').val(response.id);
        }
    })
});

// cancel edit frame
$('#cancel-edit-frame').on('click', function (e) {
    $('.edit-frame-container').addClass('d-none');
    // reset form
    $('#edit-frame-form')[0].reset();
});

$('#edit-frame-form').on('submit', function (e) {
    e.preventDefault();
    var frameId = $('#frame_id').val();
    var formData = new FormData(this);
    $.ajax({
        url: '/frames/api/' + frameId,
        type: 'PUT',
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            const toastLiveExample = document.getElementById('liveToast');
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
            toastBootstrap.show();
            
            // Reset form
            $('#edit-frame-form')[0].reset();
            // Hide 
            $('.edit-frame-container').addClass('d-none');

            // reload frames
            loadFrames();
        }
    })
});

// Submit frame use multipart/form-data
$('#upload-frame-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/frames/',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            const toastLiveExample = document.getElementById('liveToast');
            const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
            toastBootstrap.show();
            
            // Reset form
            $('#upload-frame-form')[0].reset();
            // Hide
            $('.add-frame-container').addClass('d-none');
            
            // reload frames
            loadFrames();
        }
    })
});

$('body').on('change', '.add-photo-input', function (e) {
    e.preventDefault();
    var input = this;    
    var photoPreview = $(this).parent().find('.photo_preview_add');
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            photoPreview.attr('src', e.target.result);
        }
        photoPreview.show();
       reader.readAsDataURL(input.files[0]);
       photoPreview.show();
    }
});

$('body').on('change', '.edit-photo-input', function (e) {
    e.preventDefault();
    var input = this;    
    var photoPreview = $(this).parent().find('.photo_preview_edit');
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            photoPreview.attr('src', e.target.result);
        }
        photoPreview.show();
       reader.readAsDataURL(input.files[0]);
    }
});

$('body').on('click', '.nav-button.left', function () {
    const imageList = $('.image-list');
    scrollAmount = Math.max(0, scrollAmount - scrollStep);
    imageList.css('transform', 'translateX(-' + scrollAmount + 'px)');
});

$('body').on('click', '.nav-button.right', function () {
    const imageList = $('.image-list');
    const maxScroll = imageList[0].scrollWidth - imageList.width();
    scrollAmount = Math.min(maxScroll, scrollAmount + scrollStep);
    imageList.css('transform', 'translateX(-' + scrollAmount + 'px)');
});

$('body').on('click', '.image-frame', function () {
    var frameId = $(this).data('frame-id');
    window.location.href = '/backgrounds/?frame=' + frameId;
});

function loadFrames() {
    $('.api-loading').removeClass('d-none');
    $('.add-frame-container').addClass('d-none');
    $('.image-list').empty();
    $.ajax({
        url: '/frames/api',
        type: 'GET',
        success: function (response) {
            $('.api-loading').addClass('d-none');
            // reload frames
            const frames = response;
            frames.forEach(frame => {
                $('.image-list').append(
                    '<div class="image-container">' +
                    '<img src="' + frame.photo + '" alt="frame" class="image-frame" data-frame-id="' + frame.id + '">' +
                    '<div class="image-title">' + frame.title + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-frame text-decoration-none text-white" data-frame-id="' + frame.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +
                    '<button class="delete-button">' +
                    '<a class="delete-frame text-decoration-none text-white" data-frame-id="' + frame.id + '">' +
                    '<span class="mdi mdi-trash-can"></span> Delete</a>' +
                    '</button>' +
                    '</div>' +
                    '</div>'
                )
            })
        }
    })
}

function previewPhoto(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function () {
        var img = document.getElementById('photo_preview');
        img.src = reader.result;
        img.style.display = 'block';
    }
    reader.readAsDataURL(input.files[0]);
}

function previewPhotoHover(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function () {
        var img = document.getElementById('photo_hover_preview');
        img.src = reader.result;
        img.style.display = 'block';
    }
    reader.readAsDataURL(input.files[0]);
}