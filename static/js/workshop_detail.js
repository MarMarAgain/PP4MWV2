// Waits for page to load, then returns back if workshop saved to cart sucessfully.
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

$(document).ready(function() {
    $('#add-to-cart-form').submit(function(e) {
        e.preventDefault();  // Prevent default form submission

        var formData = $(this).serialize();  // Serialize form data
        var actionUrl = $(this).attr('action');

        // Send POST request to add workshop to cart
        $.post(actionUrl, formData)
            .done(function(response) {
                // Process the response from the server
                if (response.success) {
                    $('#add-to-cart-response').html('<p class="success-message">Workshop added to cart!</p>');
                } else {
                    $('#add-to-cart-response').html('<p class="error-message">Failed to add workshop. Please try again.</p>');
                }
            })
            .fail(function(xhr, status, error) {
                console.error('Error:', error); // Log the error to console for debugging
                $('#add-to-cart-response').html('<p class="error-message">Workshop added!</p>');
            });
    });
});

/**/
