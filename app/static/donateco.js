var DonateCoModule = (function () {
    var stripe;

    function init() {
        fetch(nhdata.configUrl, {method:'GET'})
            .then(nhdata.fetchStatus)
            .then(nhdata.fetchJson)
            .then(function(data){
                console.log({ConfigData:data});
                stripe = Stripe(data.publicKey);
            })
            .catch(function(error){
                console.log('An error occurred configuring stripe.', error);
            });
    }
    
    function redirectToCheckout(event, amountInput){
        var amount = $(amountInput).val();
        var formData = new FormData();
        formData.append('amount', amount);
        console.log({Event:event, Amount:amount});
        
        fetch(nhdata.checkoutUrl, {method:'POST', body:formData})
            .then(nhdata.fetchStatus)
            .then(nhdata.fetchJson)
            .then(function(data){
                console.log({CheckoutData:data});
                if(stripe){
                    return stripe.redirectToCheckout({sessionId: data.id});
                }
                else{
                    console.log('Error: The stripe object is not defined.');
                }
            })
            .then(function(result){
                console.log({SessionResult:result});
                if(result && result.error){
                    console.log({SessionErrorResult:result});
                    alert(result.error.message);
                }
            })
            .catch(function(error){
                console.log('An error occurred configuring the stripe checkout session.', error);
            });
    }

    function isNumber(event){
        var iKeyCode = (event.which) ? event.which : event.keyCode
        console.log(iKeyCode);
        if (iKeyCode > 31 && (iKeyCode < 48 || iKeyCode > 57))
            return false;

        return true;
    }

    return {
        init: init,
        redirectToCheckout:redirectToCheckout,
        isNumber: isNumber
    };
})();
