$(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(e) {
        e.preventDefault();
        $.ajax({
            type: 'GET',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response) {
                $('#add-to-cart-response').html('<p>' + response.message + '</p>');
            },
            error: function(response) {
                $('#add-to-cart-response').html('<p>' + response.responseJSON.message + '</p>');
            }
        });
    });
});