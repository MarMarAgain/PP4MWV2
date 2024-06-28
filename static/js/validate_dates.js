document.addEventListener('DOMContentLoaded', function() {
    // bookedDates array is defined in the HTML template and available here
    bookedDates = bookedDates.map(function(dateStr) {
        return new Date(dateStr);
    });

    var form = document.getElementById('add-to-cart-form');
    var dateTimeInput = document.getElementById('date_time');

    form.addEventListener('submit', function(event) {
        var selectedDate = new Date(dateTimeInput.value);
        var isDateBooked = bookedDates.some(function(bookedDate) {
            return selectedDate.getTime() === bookedDate.getTime();
        });

        if (isDateBooked) {
            alert('This date and time is already booked. Please select another date and time.');
            event.preventDefault();
        }
    });
});
