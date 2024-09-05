$(document).ready(function() {
    $('#add-to-cart-form').on('submit', function(e) {
        e.preventDefault();  // Prevent default form submission

        $.ajax({
            type: 'POST',  // Use POST for adding items to the cart
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function(response) {
                $('#add-to-cart-response').html('<p>' + response.message + '</p>');
            },
            error: function(xhr) {
                $('#add-to-cart-response').html('<p>' + xhr.responseJSON.message + '</p>');
            }
        });
    });
});
