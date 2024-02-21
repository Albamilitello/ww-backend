// static/main.js

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/config")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});


/*    try:
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        payment_status = checkout_session['payment_status']
    except Exception as e:
        print(str(e))*/

/*    try:
        checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
        payment_status = checkout_session['payment_status']
    except Exception as e:
        print(str(e))*/