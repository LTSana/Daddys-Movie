/* JavaScript for the login page */

// Get the next page to redirect to from the URL params
const queryString = window.location.search;
let URLParam = new URLSearchParams(queryString);
const nextPage = URLParam.get("next"); // Gets the next page to redirect to from the url parameters

// Add an event listener for when the login form is being submitted and POST the request to the backEnd
document.addEventListener("submit", (e) => {

    // Prevent the page from reloading
    e.preventDefault();

    // Used for reCAPTCHA v3
	grecaptcha.ready(() => {
		// Get the reCAPTCHA token
		grecaptcha.execute(document.querySelector("#site-key").value).then((token) => {
			$("#recaptcha").val(token);
		});
	});

    // Check for the reCAPTCHA token
    let RCTPTokenInterval = setInterval(() => {
        if (document.querySelector("#recaptcha").value) {
			clearInterval(RCTPTokenInterval);
			submitForm(); // Submit the form
		}
    }, 100);

    // Only submit the form when the reCAPTCHA token is available
    submitForm = () => {

        let username = document.querySelector("#username").value;
        let password = document.querySelector("#password").value;
        let recaptcha_token = document.querySelector("#recaptcha").value; // Get the reCAPTCHA token

        // fetch POST the user login credentials
        fetch(`${BACKEND_HOST}/core/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRFTOKEN,
            },
            body: JSON.stringify({
                "username": username,
                "password": password,
                "recaptcha_token": recaptcha_token,
            })
        }).then(res => res.json()).then(json => {

            // Check the status of the reponse
            if (json.status === 200) {

                // Get and store the authentication token
                localStorage.setItem("token", JSON.stringify(json.token));

                // Send the user to the index/home page or to the next page that the user was trying to access
                if (nextPage) {
                    location.href = nextPage;
                } else {
                    location.href = "/";
                }
            } else {
                console.log(json);
                if (json.message) {
                    ALERT_MESSAGE("#login-alert", json.message)
                } else {
                    ALERT_MESSAGE("#login-alert", "Something wen't wrong while sending request to the server.\nCheck concole logs.")
                }
            }
        }).catch( (err) => {
            console.log(err);
        });
    }
});
