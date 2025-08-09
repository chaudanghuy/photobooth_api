// Image slider
let scrollAmount = 0;
const scrollStep = 220;

// selected background
let selectedBackground = null;
// selected background title
let selectedBackgroundTitle = null;
// selected frame
let selectedFrame = null;

// load background at start
$(document).ready(function () {
    // Load backgrounds
    loadBackgrounds();
});

/** Add background */
$('body').on('click', '.add-background', function () {
    $('.add-background-container').removeClass('d-none'); 
});

// Close add background
$('body').on('click', '.add-background-close', function () {
    $('.add-background-container').addClass('d-none');
});

// submit background
$('#upload-background-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/backgrounds/',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            notify();
            // reload backgrounds
            loadBackgrounds();
            // Hide form
            $('.add-background-container').addClass('d-none');
            // reset form
            $('#upload-background-form')[0].reset();
        }
    })
});

/** Edit background */
$('body').on('click', '.edit-background', function () {
    var backgroundId = $(this).data('background-id');
    $.ajax({
        url: '/backgrounds/api/' + backgroundId,
        type: 'GET',
        success: function (response) {
            // Show form
            $('.edit-background-container').removeClass('d-none');
            // hide form
            $('.add-background-container').addClass('d-none');

            // fill form
            var backgroundForm = $('#edit-background-form');
            backgroundForm.find('#background_id').val(response.id);
            backgroundForm.find('#background_title').val(response.title);
            backgroundForm.find('#photo_preview').attr('src', response.photo);
            backgroundForm.find('#photo_hover_preview').attr('src', response.photo_hover);
            backgroundForm.find('#photo_kr_preview').attr('src', response.photo_kr);
            backgroundForm.find('#photo_kr_hover_preview').attr('src', response.photo_kr_hover);
            backgroundForm.find('#photo_vn_preview').attr('src', response.photo_vn);
            backgroundForm.find('#photo_vn_hover_preview').attr('src', response.photo_vn_hover);
            backgroundForm.find('#price').val(response.price);            
        }
    })
});

// Close Edit background
$('body').on('click', '.cancel-edit-background', function () {
    $('.edit-background-container').addClass('d-none');    
});

// Update background
$('#edit-background-form').on('submit', function (e) {
    e.preventDefault();
    var backgroundId = $('#background_id').val();
    var formData = new FormData(this);
    $.ajax({
        url: '/backgrounds/api/' + backgroundId,
        type: 'PUT',
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            notify();
            // reload backgrounds
            loadBackgrounds();
            // Hide form
            $('.edit-background-container').addClass('d-none');
            // reset form
            $('#edit-background-form')[0].reset();
        }
    })
});

/** Delete background */
$('body').on('click', '.delete-background', function () {
    if (confirm('Are you sure you want to delete this background?') == true) {
        var backgroundId = $(this).data('background-id');
        $.ajax({
            url: '/backgrounds/api/' + backgroundId,
            type: 'DELETE',
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
            success: function (response) {
                // reload backgrounds
                loadBackgrounds();
            }
        })
    }
});

/******************** Layout ******************************************************/

$('body').on('click', '.background-image-container', function () {
    var backgroundId = $(this).data('background-id');
    var backgroundTitle = $(this).data('background-title');
    loadLayouts(backgroundId, backgroundTitle);
});

// Add layout
$('body').on('click', '.add-layout', function () {
    $('.add-layout-container').removeClass('d-none');

    var addLayoutContainer = $('.add-layout-container');    

    // Get frame selected
    var selectedFrameText = $('.choose-frame-layout option:selected').text();

    // Set add layout's title
    addLayoutContainer.find('.card-title').html("Create Layout - " + selectedFrameText);

    // Set background
    addLayoutContainer.find('#background').val(selectedBackground);

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
       photoPreview.show();
    }
});

// Close Add layout
$('body').on('click', '.cancel-add-layout', function () {
    $('.add-layout-container').addClass('d-none');
});

/** Delete background */
$('body').on('click', '.delete-layout', function () {
    if (confirm('Are you sure you want to delete this layout?') == true) {
        var layoutId = $(this).data('layout-id');
        $.ajax({
            url: '/layouts/api/' + layoutId,
            type: 'DELETE',
            headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
            success: function (response) {
                // reload layouts
                loadLayouts(selectedBackground, selectedBackgroundTitle);
            }
        })
    }
});

// Edit layout
$('body').on('click', '.edit-layout', function (e) {
    e.preventDefault();
    var layoutId = $(this).data('layout-id');
    hideAndResetAllForms();
    // show edit form
    var editLayoutContainer = $('.edit-layout-container');
    editLayoutContainer.removeClass('d-none');
    // reload layouts ?
    loadLayouts(selectedBackground, selectedBackgroundTitle);
    // load edit layout
    $.ajax({
        url: '/layouts/api/' + layoutId,
        type: 'GET',
        success: function(response) {
            // Fill form
            var editLayoutForm = editLayoutContainer.find('#edit-layout-form');
            editLayoutForm.find('#layout_id').val(response.id);
            editLayoutForm.find('#title').val(response.title);
            editLayoutForm.find('#position').val(response.position);
            editLayoutForm.find('#background').val(response.background);
            editLayoutForm.find('#frame').val(response.frame);
            editLayoutForm.find('#photo_preview').attr('src', response.photo);
            editLayoutForm.find('#photo_cover_preview').attr('src', response.photo_cover);
            editLayoutForm.find('#photo_full_preview').attr('src', response.photo_full);            
        }
    })    
});

// Close Edit layout
$('body').on('click', '.cancel-edit-layout', function () {
    $('.edit-layout-container').addClass('d-none');    
});

// Choose frame layout
$('.choose-frame-layout').on('change', function (e) {
    e.preventDefault();        
    loadLayouts(selectedBackground, selectedBackgroundTitle);
});

// Submit add Layout
$('#upload-layout-form').on('submit', function (e) {
    e.preventDefault();
    var formData = new FormData(this);
    $.ajax({
        url: '/layouts/api',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            notify();
            // reload layouts
            loadLayouts(selectedBackground, selectedBackgroundTitle);
            // Hide form
            $('.add-layout-container').addClass('d-none');
            // reset form
            $('#add-layout-form')[0].reset();
        }
    })
});

$('#edit-layout-form').on('submit', function (e) {
    e.preventDefault();
    var editLayoutContainer = $('.edit-layout-container');
    var layoutId = editLayoutContainer.find('#layout_id').val();
    var formData = new FormData(this);
    $.ajax({
        url: '/layouts/api/' + layoutId,
        type: 'PUT',
        headers: {'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()},
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            // Notify
            notify();
            // reload layouts
            loadLayouts(selectedBackground, selectedBackgroundTitle);
            // Hide form
            $('.edit-layout-container').addClass('d-none');
            // reset form
            $('#edit-layout-form')[0].reset();
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

/******************** Layout ******************************************************/

// Load backgrounds
function loadBackgrounds() {
    $('.api-loading').removeClass('d-none');
    $('.add-background-container').addClass('d-none');
    $('.image-list-background').empty();
    $.ajax({
        url: '/backgrounds/api',
        type: 'GET',
        success: function (response) {
            $('.api-loading').addClass('d-none');
            // reload backgrounds
            const backgrounds = response;
            backgrounds.forEach(background => {
                $('.image-list-background').append(
                    '<div class="image-container background-image-container" data-background-id="' + background.id + '" data-background-title="' + background.title + '">' +
                    '<img src="' + background.photo + '" data-src="' + background.photo + '" data-hover="' + background.photo_hover + '" alt="background" class="image-background">' +
                    '<div class="image-title">' + background.title + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-background text-decoration-none text-white" data-background-id="' + background.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +
                    '<button class="delete-button">' +
                    '<a class="delete-background text-decoration-none text-white" data-background-id="' + background.id + '">' +
                    '<span class="mdi mdi-trash-can"></span> Delete</a>' +
                    '</button>' +
                    '</div>' +
                    '</div>'
                )
            })
        }
    })
}

function loadLayouts(backgroundId, backgroundTitle) {
    var layoutContainer = $('.list-layouts-container');

    // check if passing param frame in url
    var frameId = frameId = layoutContainer.find('.choose-frame-layout').val();

    // show layout container
    layoutContainer.removeClass('d-none');
    layoutContainer.find('.card-title').html(backgroundTitle);

    $('.image-list-layouts').empty();

    // load layouts
    $.ajax({
        url: '/layouts/api/group-by-background/' + backgroundId + '/frame/' + frameId,
        type: 'GET',
        success: function (response) {
            selectedBackground = backgroundId;
            selectedBackgroundTitle = backgroundTitle;

            //reset add layout form
            resetAddLayoutForm();

            const layouts = response;
            layouts.forEach(layout => {
                $('.image-list-layouts').append(
                    '<div class="image-container">' +
                    '<img src="' + layout.photo_full + '" data-src="' + layout.photo + '" data-hover="' + layout.photo_hover + '" alt="layout" class="image-layout">' +
                    '<div class="layout-title">' + layout.title + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-layout text-decoration-none text-white" data-layout-id="' + layout.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +
                    '<button class="delete-button">' +
                    '<a class="delete-layout text-decoration-none text-white" data-layout-id="' + layout.id + '">' +
                    '<span class="mdi mdi-trash-can"></span> Delete</a>' +
                    '</button>' +
                    '</div>' +
                    '</div>'
                )
            })
        }
    });
}

function loadLayoutsByFrame(backgroundId, backgroundTitle, frameId) {
    // show layout container
    var layoutContainer = $('.list-layouts-container');
    layoutContainer.removeClass('d-none');
    layoutContainer.find('.card-title').html(backgroundTitle);

    $('.image-list-layouts').empty();

    // load layouts
    $.ajax({
        url: '/layouts/api/group-by-background/' + backgroundId,
        type: 'GET',
        success: function (response) {
            selectedBackground = backgroundId;
            const layouts = response;
            layouts.forEach(layout => {
                $('.image-list-layouts').append(
                    '<div class="image-container">' +
                    '<img src="' + layout.photo_full + '" data-src="' + layout.photo + '" data-hover="' + layout.photo_hover + '" alt="layout" class="image-layout">' +
                    '<div class="layout-title">' + layout.title + '</div>' +
                    '<div class="action-buttons">' +
                    '<button class="edit-button">' +
                    '<a class="edit-layout text-decoration-none text-white" data-layout-id="' + layout.id + '">' +
                    '<span class="mdi mdi-pencil"></span> Edit</a>' +
                    '</button>' +
                    '<button class="delete-button">' +
                    '<a class="delete-layout text-decoration-none text-white" data-layout-id="' + layout.id + '">' +
                    '<span class="mdi mdi-trash-can"></span> Delete</a>' +
                    '</button>' +
                    '</div>' +
                    '</div>'
                )
            })
        }
    });
}

function previewPhoto(event, preview) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function() {
        var img = document.getElementById(preview);
        img.src = reader.result;
        img.style.display = 'block';
    }
    reader.readAsDataURL(input.files[0]);
}

function notify() {
    // Notify
    // const toastLiveExample = document.getElementById('liveToast');
    // const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    // toastBootstrap.show();
}

$(".image-background").mouseover(function () {
    $(this).attr('src', $(this).data("hover"));
}).mouseout(function () {
    $(this).attr('src', $(this).data("src"));
});

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

/**********   FUNCIONALITY   **********/
function resetAddLayoutForm() {
    var addLayoutContainer = $('.add-layout-container');
    // Get frame selected
    var selectedFrameText = $('.choose-frame-layout option:selected').text();
    // Get frame id selected
    var selectedFrameId = $('.choose-frame-layout option:selected').val();

    // reset title
    addLayoutContainer.find('.card-title').html("Create Layout - " + selectedFrameText);
    // reset frame selected    
    addLayoutContainer.find('#frame').val(selectedFrameId);
    // reset background selected
    addLayoutContainer.find('#background').val(selectedBackground);    
}

function hideAndResetAllForms() {
    // hide all layout form
    var addLayoutContainer = $('.add-layout-container');
    addLayoutContainer.addClass('d-none');
    var editLayoutContainer = $('.edit-layout-container');
    editLayoutContainer.addClass('d-none');
    // hide all background form
    var addBackgroundContainer = $('.add-background-container');
    addBackgroundContainer.addClass('d-none');
    var editBackgroundContainer = $('.edit-background-container');
    editBackgroundContainer.addClass('d-none');
}