$(document).ready(function(){
    // Get key
    fetch("/donateco-config")
        .then((result) => { return result.json(); })
        .then((data) => {
            // Initialize Stripe.js
            const stripe = Stripe(data.publicKey);
            //nhdata['stripe'] = stripe;
            console.log({Key:data.publicKey, Data:data, Stripe:nhdata.stripe});

            // Event handler
            var submitButton = document.querySelector("#submitBtn");
            if(!submitButton) return "Submit button not foound"
            submitButton.addEventListener("click", () => {
                // Get Checkout Session ID
                console.log('submit button clicked');
                fetch("/create-checkout-session")
                    .then((result) => { return result.json(); })
                    .then((data) => {
                        console.log({Data:data, Method:'create-checkout-session-then2'});
                        // Redirect to Stripe Checkout
                        return stripe.redirectToCheckout({sessionId: data.id})
                    })
                    .then((res) => {
                        console.log({Data:res, Method:'create-checkout-session-then3'});
                    });
            });
    });
});