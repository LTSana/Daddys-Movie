/* JavaSrcipt for all pages */

// Get CSRF
getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
        return cookieValue;
    }
const CSRFTOKEN = getCookie("csrftoken");

// The backend that we are going to be connecting our APIs
const BACKEND_HOST = ``;
let ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
const WEBSCKET_HOST = `${ws_scheme}://${window.location.host}`
const TOKEN = JSON.parse(localStorage.getItem("token"));
/* if (localStorage.getItem("token") && localStorage.getItem("token") != "undefined") {
	TOKEN = JSON.parse(localStorage.getItem("token"));
} else {
	TOKEN = {"type": "", "access": "", "refresh": "", "expire": 0};
} */

// User information
let CURRENT_USER = null;

// Check if the user is logged in by verifying the access token
// If the access token has expired refresh the token
fetch(`${BACKEND_HOST}/core/currentUser`, {
	method: "GET",
	headers: {
		"Content-Type": "application/json",
		//"Authorization": `${TOKEN.type} ${TOKEN.access}`,
	},
}).then(res => res.json()).then(json => {

	// Check the response status
	if (json.status === 200) {

		CURRENT_USER = json.data.username;
		console.log(json);
	} else {

		// Attempt to refresh the access token
		/* fetch(`${BACKEND_HOST}/token-refresh/`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
				"refresh": TOKEN.refresh,
			}),
		}).then(res => res.json()).then(json => {

			// Check the response status
			if (json.access) {
				
				// Replace the access token we have now with the new one
				TOKEN.access = json.access;

				// Update the local storage token
				localStorage.setItem("token", JSON.stringify(TOKEN));

				// Reload the page
				location.reload()
			} else {

				// Remove the token from the local storage if the refresh token is also expired
				localStorage.removeItem("token");
				TOKEN = {"type": "", "access": "", "refresh": "", "expire": 0};
			}
		}); */
	}
});

// Logout the user
if (document.querySelector("#navbar-logout-btn")) {

	document.querySelector("#navbar-logout-btn").onclick = () => {
		fetch(`${BACKEND_HOST}/core/logout`, {
			method: "GET",
			headers: {
				"Content-Type": "application/json",
				//"Authorization": `${TOKEN.type} ${TOKEN.access}`,
			}
		}).then(res => res.json()).then(json => {

			// Check response status
			if (json.status === 200) {

				// Remove all TOKENs
				localStorage.removeItem("token");

				// Send the user to the login page
				location.href = "/login";
			} else {
				console.log(json);
			}
		});
	}
}
