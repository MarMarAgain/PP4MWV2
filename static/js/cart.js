//Removes item from cart
$(document).ready(function() {
    console.log('jQuery ready and loaded');

    // Intercept form submission
    $('.remove-item-form').submit(function(event) {
        event.preventDefault();  // Prevent the default form submission
        console.log('Form submission intercepted');

        var form = $(this);  // Get the form
        var url = form.attr('action');  // Get the URL from form action
        var itemId = form.find('input[name="item_id"]').val();  // Get the item ID

        $.ajax({
            url: url,
            type: 'POST',
            data: form.serialize(),  // Serialize form data including CSRF token
            success: function(response) {
                console.log('AJAX success response:', response);
                if (response.success) {
                    form.closest('.cart-item').remove();  // Remove the cart item from the DOM
                    console.log('Item removed successfully');
                } else {
                    console.log('Error in response');
                }
            },
            error: function(xhr, errmsg, err) {
                console.log('AJAX error:', errmsg);
            }
        });
    });
});

//Update total price in bag ( header)
function updateCartTotal() {
    $.getJSON("{% url 'get_cart_total' %}", function(data) {
        $('#cart-total').text('€' + parseFloat(data.total).toFixed(2));
    });
}

