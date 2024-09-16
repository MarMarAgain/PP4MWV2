// stripe_payment.js
document.addEventListener('DOMContentLoaded', function() {
    const stripe = Stripe(stripePublicKey);

    var form = document.getElementById('payment-form');

    form.addEventListener('submit', function(ev){
        ev.preventDefault();

        document.getElementById('submit-button').disabled=true;

        fetch(form.action,{
            methon:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
        })
            .then(response =>response.json())
            .then(session => {
                return stripe.redirectToCheckout({sessionID: session.id});
            })
            .then(function(result) {
                if (result.error){
                    alert(result.error.message);
                }
            })
            .catch(error =>{
                console.error('Error:', error);
                document.getElementById('submit-button').disabled=false;
            });
    });
});