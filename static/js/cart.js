/* Removes items from cart */
$(document).ready(function() {
    // Submit form when Remove button is clicked
    $('.remove-item-btn').on('click', function(e) {
        e.preventDefault();
        var form = $(this).closest('form');
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                if (response.success) {
                    form.closest('.cart-item').remove(); // Remove the item from UI
                } else {
                    console.error('Failed to remove item from cart');
                }
            },
            error: function(response) {
                console.error('Error removing item from cart');
            }
        });
    });
});
