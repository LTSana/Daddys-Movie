/* JavaScript for Watch page */

/* 1. Be able to control and manage movie time through websockets */
/* 2. Be able to Send Chat messages and use the chat to also send video logged. *User xxxx has paused the video */

// Get the user ID from the URL params
const queryString = window.location.search;
let URLParam = new URLSearchParams(queryString);
const sessionID = URLParam.get("sessionID"); // Gets the user ID from the url parameters

// Websocket for Movie controlling for user to user
let movieControls = document.querySelector('#movie-player');

fetch(`${BACKEND_HOST}/movie/session?sessionID=${sessionID}`, {
	headers: {
		"Content-Type": "application/json",
		//"Authorization": `${TOKEN.type} ${TOKEN.access}`,
	},
}).then(res => res.json()).then(json => {

	// Check response status
	if (json.status === 200) {

		console.log(json);

		// Remove the current video source
		document.querySelector("#movie-player > source").remove();
		// Add the source of the video
		const html_template = document.createElement("source");
		html_template.src = json.movie.source;
		html_template.type = "video/mp4";
		document.querySelector("#movie-player").append(html_template);

		// Add the title of the video
		document.querySelector("#movie-title-holder").innerHTML = json.movie.title;


	} else {
		console.log(json);
		ALERT_MESSAGE("#movie-alert", json.message);
	}
});

const websocketChat = new ReconnectingWebSocket(
	`${WEBSCKET_HOST}/ws/chat/${sessionID}/?token=${TOKEN.access}`
);

// Waiting set milliseconds to reconnect
websocketChat.timeoutInterval = 5000;

// Do actions after the websocket has connected and is open
websocketChat.onopen = (e) => {
	/* fetchMessages(_cursor); */
	pauseMovie(e);
};

pauseMovie = (e) => {
	websocketChat.send(JSON.stringify({
		"action": "pause", // Send the action
		"currentTime": movieControls.currentTime,
		"command": "video_controls",
	}));
}

// Store a variable that keeps track of the movie commands coming from another user
let incomingCommand = "";

// Display the incoming message from the sender
websocketChat.onmessage = (e) => {

	const data = JSON.parse(e.data);
	if (data.message) {
		if (data.message.command === "messages") {

			let loading_gif = false;

			// Start from the oldest 
			for (let i = data.message.messages.length - 1; i >= 0; i--) {

				// Prevent duplication
				if (!document.querySelector(`#message-id-${data.message.messages[i].id}`)) {
					loadMessage(data.message.messages[i]);

					// Remove the loading gif
					if (document.querySelector(".loading-gif-col")) {
						loading_gif = true;
						document.querySelector(".loading-gif-col").remove(); // Remove the loading gif
					}
				}
			}

			// Check if the user is loading old messages
			if (loading_gif) {
				// Send the user to the newest old messages (If not this it would scroll to top automatically)
				document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(`#message-id-${data.message.messages[data.message.messages.length - 1].id}`).offsetTop - 60;
			}

			// Add the cursors value
			_cursor = data.message.cursor;

			// Check if the chat is has any old text that can be loaded to fill the message row
			if (document.querySelector(".hero-1-message-holder").offsetWidth === document.querySelector(".hero-1-message-holder").clientWidth) {
				if (_cursor > 0) {
					fetchMessages(_cursor);
				}
			}

		} else if (data.message.command === "new_message") {
			// Prevent duplication
			if (!document.querySelector(`#message-id-${data.message.message.id}`)) {
				createMessage(data.message.message);
			}

			document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(".hero-1-message-holder").scrollHeight - document.querySelector(".hero-1-message-holder").clientHeight;

		} else if (data.message.command === "leave_room") {
			// Prevent duplication
			if (!document.querySelector(`#message-id-${data.message.message.id}`)) {
				alertMessage(data.message.message);
			}

			document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(".hero-1-message-holder").scrollHeight - document.querySelector(".hero-1-message-holder").clientHeight;
		} else if (data.message.action) {

			// Check what action the movie is in
			if (data.message.username != CURRENT_USER) {

				if (data.message.action === "pause") {
                    if (data.message.currentTime < (movieControls.currentTime + 10) && data.message.currentTime > (movieControls.currentTime - 10)) {
                        movieControls.pause();
                    }
					movieControls.currentTime = data.message.currentTime;
				} else if (data.message.action === "play") {
					movieControls.play();

					if (movieControls.currentTime != data.message.currentTime) {
						movieControls.currentTime = data.message.currentTime;
					}
				}
			}

			incomingCommand = data.message.username;
		}
	}
	// Scroll to the bottom of the chat if entering a new chat
	/* if (enter_new_chat) {
		enter_new_chat = false;
		// Set a timeout to wait to get the Height of the chat to scroll down to the bottom
		setTimeout(() => {
			document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(".hero-1-message-holder").scrollHeight - document.querySelector(".hero-1-message-holder").clientHeight;
		}, 100);
	} */
};

// Used when video is buffering or user moves from one timeline to another
/* movieControls.onwaiting = () => {
	console.log("HEY, I'M WAITING!! SENDING ACTION");
	if (incomingCommand != CURRENT_USER) {
		websocketChat.send(JSON.stringify({
			"action": "pause", // Send the action
			"currentTime": movieControls.currentTime,
			"command": "video_controls",
		}));
	} else {
		incomingCommand = "";
	}
} */

// Used when the video is paused
movieControls.onpause = () => {
    if (!movieControls.onseeked) {
        websocketChat.send(JSON.stringify({
            "action": "pause", // Send the action
            "currentTime": movieControls.currentTime,
            "command": "video_controls",
        }));
    }
}

// Used when the video is played
movieControls.onplay = () => {
	websocketChat.send(JSON.stringify({
		"action": "play", // Send the action
		"currentTime": movieControls.currentTime,
		"command": "video_controls",
	}));
}

// Display the messages
createMessage = (data) => {

	if (data.status === "message") {
		let message = data.content;
		let username = data.username;

		// Create the div to display the message
		let html_template = document.createElement("div");

		// Create the timestamps for the displayed messages
		let currentTime = ""
		let date_timestamp = `${new Date()}`; // Display the day the message was sent
		currentTime = `${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display that the message was sent now

		if (CURRENT_USER == username) {
			html_template.setAttribute("class", "col-xl-12 offset-xl-0 d-flex flex-column justify-content-end align-items-end sender-message");
			html_template.innerHTML = `<p class="d-flex flex-column justify-content-start align-items-end">
										<span class="username-span">${username}<br /></span>
										<span class="message-span">${message}</span>
										<span class="date-span">${currentTime}</span>
									</p>`;
		} else {
			html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-start align-items-start receiver-message");
			html_template.innerHTML = `<p class="d-flex flex-column justify-content-start align-items-start align-content-start">
										<span class="username-span">${username}<br /></span>
										<span class="message-span">${message}</span>
										<span class="date-span">${currentTime}</span>
									</p>`;
		}
		document.querySelector(".hero-1-message-holder").append(html_template);
	} else if (data.status === "alert_message") {
		alertMessage(data);
	}
}

// Display the loaded messages
loadMessage = (data) => {

	if (data.status === "message") {
		let id = data.id;
		let message = data.content;
		let author = data.author;

		// Create the div to display the message
		let html_template = document.createElement("div");

		// Get the time since message
		let m_timestamp = Math.round((new Date().getTime() - new Date(data.timestamp+" UTC").getTime()) / 60000);

		// Create the timestamps for the displayed messages
		let since_time = ""
		let date_timestamp = `${new Date(data.timestamp+" UTC")}`; // Display the day the message was sent
		if (m_timestamp < 60 && m_timestamp > 0) {
			since_time = `${m_timestamp} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of minutes gone by
		} else if ((m_timestamp / 60) > 0 && (m_timestamp / 60) < 25) {
			since_time = `${Math.round(m_timestamp / 60 % 24)} hours ${m_timestamp % 60} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of hours and minutes gone by
		} else if ((m_timestamp / 60) > 23) {				
			since_time = `${date_timestamp.split(":")[0]}:${date_timestamp.split(":")[1]}`;
		} else {
			since_time = `Now - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display that the message was sent now
		}

		if (author == username) {
			html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-end align-items-end");
			html_template.setAttribute("id", `message-id-${id}`);
			html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start sender-message">
									<span class="sender-message-author">${author}</span>
									${message.replace("\n", "<br>")}</p>
									<p class="text-break text-muted sender-message-timestamp">${since_time}</p>`;
		} else {
			html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-end align-items-start");
			html_template.setAttribute("id", `message-id-${id}`);
			html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start received-message">
										<span class="received-message-author">${author}</span>
										${message.replace("\n", "<br>")}</p>
										<p class="text-break text-muted received-message-timestamp">${since_time}</p>`;
		}
		document.querySelector(".hero-1-message-holder").prepend(html_template);
	} else if (data.status === "alert_message") {
		alertMessage(data);
	}
}

alertMessage = (data) => {

	let html_template = document.createElement("div");
	html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-start align-items-center");

	html_template.innerHTML = `<p class="text-break text-white-50 d-flex flex-column justify-content-start sender-message" id="message-id-1">${data.content}</p>`;

	document.querySelector(".hero-1-message-holder").append(html_template);
	websocketChat.close(); // Close the websockt connection
}

websocketChat.onclose = (e) => {
	console.error("Chat socket closed unexpectedly");
};

document.querySelector("#message-text-input").focus();

// Check if shift is being pressed
// If shift key is being pressed it allows user to create new lines
let shift_pressed = false;
document.querySelector("#message-text-input").onkeydown = (e) => {
	if (e.keyCode === 16) { // Shift pressed
		shift_pressed = true;
	}
};

// Check if enter key is being pressed
document.querySelector("#message-text-input").onkeyup = (e) => {

	// Check if the shift key is being released
	if (e.keyCode === 16) {
		shift_pressed = false
	}

	if (e.keyCode === 13 && !shift_pressed) {  // enter, return
		document.querySelector("#send-message-btn").click();
	}
};

document.querySelector("#send-message-btn").onclick = (e) => {

	// prevent the form from reloading the page

	const messageInputDom = document.querySelector("#message-text-input");
	const message = messageInputDom.value;
	websocketChat.send(JSON.stringify({
		"message": message, // Send the message
		"sessionID": sessionID, // Send the room ID
		"command": "new_message",
	}));
	messageInputDom.value = "";
};

receivedAction = (data) => {
	console.log(data+" - 888");
	console.log(movieControls);
	document.querySelector('#movie-player').pause()
	movieControls.pause();
}

websocketChat.onclose = (e) => {
	console.error("Movie socket closed unexpectedly");
};