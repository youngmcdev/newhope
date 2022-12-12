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
    
    function redirectToCheckout(event, amountInput, modalBody){
        var amount = $(amountInput).val();
        var formData = new FormData();
        formData.append('amount', amount);
        console.log({Event:event, Amount:amount});
        var okButton = $(event.target);
        okButton.attr('disabled', true);
        okButton.find('#spinner').show();
        var cancelButton = okButton.siblings('#modal-close-btn');
        cancelButton.attr('disabled', true);
        
        fetch(nhdata.checkoutUrl, {method:'POST', body:formData})
            .then(nhdata.fetchStatus)
            .then(nhdata.fetchJson)
            .then(function(data){
                console.log({CheckoutData:data});
                if(stripe){
                    return stripe.redirectToCheckout({sessionId: data.id});
                }
                else{
                    okButton.find('#spinner').hide();
                    cancelButton.attr('disabled', false);
                    console.log('Error: The stripe object is not defined.');
                    modalBody.html('<p>We apologize. Your request could not be completed. Please click <em>Cancel</em> and try again or contact us for help.</p><p>The stripe object is not defined.</p>');
                }
            })
            .then(function(result){
                console.log({SessionResult:result});
                if(result && result.error){
                    console.log({SessionErrorResult:result});
                    var message = '';
                    try{
                        console.log(result.error);
                        message = result.error.message;
                    }catch(err){
                        // not sure of the format of the result object yet.
                        console.log(err);
                    }
                    
                    okButton.find('#spinner').hide();
                    cancelButton.attr('disabled', false);
                    modalBody.html(`<p>We apologize. Your request could not be completed. Please click <em>Cancel</em> and try again or contact us for help.</p><p>${message}</p>`);
                }
            })
            .catch(function(error){
                okButton.find('#spinner').hide();
                cancelButton.attr('disabled', false);
                console.log('An error occurred configuring the stripe checkout session.', error);
                modalBody.html('<p>We apologize. Your request could not be completed. Please click <em>Cancel</em> and try again or contact us for help.</p>');
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
