/* JavaScript for Watch page */

// Get the user ID from the URL params
const queryString = window.location.search;
let URLParam = new URLSearchParams(queryString);
const sessionID = URLParam.get("sessionID"); // Gets the user ID from the url parameters

// For Movie controlling for user to user
let movieControls = document.querySelector('#movie-player');

// Check if the session ID is provided in the URL
if (sessionID) {
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
            
            // Add the session ID to the session ID holder
            document.querySelector("#sessionID-input").value = sessionID;
    
        } else {
            console.log(json);
            ALERT_MESSAGE("#movie-alert", json.message);
        }
    });
} else {

    // Display a message showing that the session ID is missing
    ALERT_MESSAGE("#movie-alert", "Sorry! Your session ID is missing please try again later.");
}

// Store a variable that keeps track of the movie commands coming from another user
let incomingCommand = "";

// Copy Session ID to the clipboard if the user clicks on it
document.querySelector("#sessionID-input").onclick = () => {

    // Get the session ID
    let copyText = document.querySelector("#sessionID-input");

    // Select the text
    copyText.select();
    copyText.setSelectionRange(0, 99999); // For mobile devices
  
    // Copy the text
    document.execCommand("copy");
  
    // Alert the user that the link was successfully copied
    ALERT_MESSAGE("#movie-alert", `Copied session ID ${sessionID} to your clipboard`);
}

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
/* movieControls.onpause = () => {
    console.log("HEY, I'M PAUSED!  SENDING ACTION");
    websocketChat.send(JSON.stringify({
        "action": "pause", // Send the action
        "currentTime": movieControls.currentTime,
        "command": "video_controls",
    }));
}

// Used when the video is played
movieControls.onplay = () => {
    console.log("HEY, I'M PLAYING! SENDING ACTION");
    websocketChat.send(JSON.stringify({
        "action": "play", // Send the action
        "currentTime": movieControls.currentTime,
        "command": "video_controls",
    }));
} */

receivedAction = (data) => {
    console.log(data+" - 888");
    console.log(movieControls);
    document.querySelector('#movie-player').pause()
    movieControls.pause();
}

movieControls.onpause = () => {
    fetch(`${BACKEND_HOST}/movie/sessionStatus`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
            "sessionID": sessionID,
            "playStatus": "pause",
            "currentTime": movieControls.currentTime,
        })
    }).then(res => res.json()).then(json => {
        console.log(json);
    });

    // Send a message showing what action the user has just done
    fetch(`${BACKEND_HOST}/message/send`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
            "sessionID": sessionID,
            "message": `Paused movie`,
            "status": "alert",
        }),
    }).then(res => res.json()).then(json => {

        console.log(json);

        // Check reponse status
        if (json.status) {
            console.log(json.message);
        } else {
            ALERT_MESSAGE("#movie-chat-alert", json.message);
        }
    }).catch(() => {
        ALERT_MESSAGE("#movie-chat-alert", "Message was unable to be sent.");
    });
}

movieControls.onplay = () => {
    fetch(`${BACKEND_HOST}/movie/sessionStatus`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
            "sessionID": sessionID,
            "playStatus": "play",
            "currentTime": movieControls.currentTime,
        })
    }).then(res => res.json()).then(json => {
        console.log(json);
    });

    // Send a message showing what action the user has just done
    fetch(`${BACKEND_HOST}/message/send`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
            "sessionID": sessionID,
            "message": `Playing movie`,
            "status": "alert",
        }),
    }).then(res => res.json()).then(json => {

        console.log(json);

        // Check reponse status
        if (json.status) {
            console.log(json.message);
        } else {
            ALERT_MESSAGE("#movie-chat-alert", json.message);
        }
    }).catch(() => {
        ALERT_MESSAGE("#movie-chat-alert", "Message was unable to be sent.");
    });
}

readyMovieState = true;
setInterval(() => {
    if (readyMovieState) {

        readyMovieState = false;

        fetch(`${BACKEND_HOST}/movie/sessionStatus?sessionID=${sessionID}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
                "X-CSRFToken": CSRFTOKEN,
            },
        }).then(res => res.json()).then(json => {
            readyMovieState = true;
            if (json.status === 200) {
                
                if (json.sessionStatus.username != CURRENT_USER) {
    
                    let UserNotInList = false;
                    for (let i = 0; i < json.sessionStatus.doneList.length; i++) {
                        if (json.sessionStatus.doneList[i] != CURRENT_USER) {
                            UserNotInList = true;
                        }
                    }
                    /* console.log(`INT: ${movieControls.paused}`);
                    console.log(`INT 2: ${movieControls.playing}`);
                    console.log(json.sessionStatus.playStatus) */
                    if (json.sessionStatus.playStatus === "pause" && !movieControls.paused) {
                        movieControls.pause();
                        movieControls.currentTime = json.sessionStatus.currentTime; 
                        /* console.log("SERVER PAUSE VIDEO"); */
                    } else if (json.sessionStatus.playStatus === "play" && movieControls.paused) {
                        movieControls.play();
                        movieControls.currentTime = json.sessionStatus.currentTime; 
                        /* console.log("SERVER PLAY VIDEO"); */
                    }
                }
            } else {
                console.log(json);
            }
        });
    }
}, 100);

// Initialize variables for the chat/messagin
let cursor = 0;
let messages_list = []; // Hold all the IDs of the messages
let latest_message_id = 0;
let GoToPosition = false;

// Fetch all the messages of the session
fetch(`${BACKEND_HOST}/message/fetch?sessionID=${sessionID}`, {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
        //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
    },
}).then(res => res.json()).then(json => {
    
    // Check the response status
    if (json.status === 200) {
        // Loop through all the messages
        for (let i = 0; i < json.data.messages.length; i++) {
            createMessage(json.data.messages[i]);
            messages_list.push(json.data.messages[i].id);
        }

        // Get the latest message ID 
        if (json.data.messages.length > 0) {
            latest_message_id = json.data.messages[json.data.messages.length - 1].id;
        }

        // Add the cursor
        if (json.data.cursor) {
            cursor = json.data.cursor;
        }

        // Set a timeout to wait to get the Height of the chat to scroll down to the bottom
        setTimeout(() => {
            document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(".hero-1-message-holder").scrollHeight - document.querySelector(".hero-1-message-holder").clientHeight;

            // Trigger the recent message checker
            GetRecentMessages();
        }, 100);

        // Check if the chat is has any old text that can be loaded to fill the message row
        if (document.querySelector(".hero-1-message-holder").offsetWidth === document.querySelector(".hero-1-message-holder").clientWidth) {
            if (cursor > 0) {
                alert("HERE");
            }
        }

    } else {
        ALERT_MESSAGE("#movie-chat-alert", "An error happened when fetching all messages.");
        console.log(json.messages);
    }
});



GetRecentMessages = () => {
    setInterval(() => {
        fetch(`${BACKEND_HOST}/message/recent?sessionID=${sessionID}&messageID=${latest_message_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            },
        }).then(res => res.json()).then(json => {

            // Check response
            if (json.status === 200) {

                // Loop through messages
                for (let i = 0; i < json.data.length; i++) {
                    createMessage(json.data[i]);

                    // Add the message ID to the list of messages already loaded in
                    if (!messages_list.includes(json.data[i].id)) {
                        messages_list.push(json.data[i].id);

                        // Set a timeout to wait to get the Height of the chat to scroll down to the bottom
                        setTimeout(() => {
                            document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(".hero-1-message-holder").scrollHeight - document.querySelector(".hero-1-message-holder").clientHeight;
                        }, 100);
                    }
                }

                // Get the latest message ID
                if (json.data.length > 0) {
                    latest_message_id = json.data[json.data.length - 1].id;
                }

            } else {
                console.log(json);
            }
        });
    }, 1000);
}

// Get the old messages when scrolling up
document.querySelector(".hero-1-message-holder").onscroll = () => {

    // Check if the user has scroll to the top
    if (document.querySelector(".hero-1-message-holder").scrollTop <= 0) {

        // Set a timeout for getting the old messages
        setTimeout(() => {

            fetch(`${BACKEND_HOST}/message/fetch?sessionID=${sessionID}&cursor=${cursor}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
                }
            }).then(res => res.json()).then(json => {

                // Check the response
                if (json.status === 200) {

                    // Loop through all messages
                    for (let i = json.data.messages.length - 1; i > 0; i--) {

                        // Check for duplicates
                        if (!messages_list.includes(json.data.messages[i].id)) {
                            loadMessage(json.data.messages[i]);
                            messages_list.push(json.data.messages[i].id);
                            GoToPosition = true;
                        }
                    }

                    // Add the cursor
                    if (json.data.cursor) {
                        cursor = json.data.cursor;
                    }

                    if (GoToPosition) {
                        // Send the user to the newest old messages (If not this it would scroll to top automatically)
                        document.querySelector(".hero-1-message-holder").scrollTop = document.querySelector(`#message-id-${json.data.messages[json.data.messages.length - 1].id}`).offsetTop - 60;

                        // Stop position snapping
                        GoToPosition = false;
                    }

                } else {
                    console.log(json);
                }
            });
        }, 500)
    }
}

// Prevent focus on message input
document.querySelector("#message-text-input").blur();

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
    
    //TODO

    // Send the message to the backend
    fetch(`${BACKEND_HOST}/message/send`, {
        method: "POST",
        headers: {
            "Content-type": "application/json",
            //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
            "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
            "sessionID": sessionID,
            "message": message,
            "status": "message",
        }),
    }).then(res => res.json()).then(json => {

        console.log(json);

        // Check reponse status
        if (json.status) {
            console.log(json.message);
        } else {
            ALERT_MESSAGE("#movie-chat-alert", json.message);
        }
    }).catch(() => {
        ALERT_MESSAGE("#movie-chat-alert", "Message was unable to be sent.");
    });

    messageInputDom.value = "";
};

// Display the loaded messages
loadMessage = (data) => {
    
    if (data.status === "message") {
        console.log(data);
        let id = data.id;
        let message = data.message;
        let username = data.username;
        let user_id = data.user_id;

        // Create the div to display the message
        let html_template = document.createElement("div");

        // Get the time since message
        let m_timestamp = Math.round((new Date().getTime() - new Date(data.date+" UTC").getTime()) / 60000);

        // Create the timestamps for the displayed messages
        let since_time = ""
        let date_timestamp = `${new Date(data.date+" UTC")}`; // Display the day the message was sent
        if (m_timestamp < 60 && m_timestamp > 0) {
            since_time = `${m_timestamp} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of minutes gone by
        } else if ((m_timestamp / 60) > 0 && (m_timestamp / 60) < 25) {
            since_time = `${Math.round(m_timestamp / 60 % 24)} hours ${m_timestamp % 60} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of hours and minutes gone by
        } else if ((m_timestamp / 60) > 23) {				
            since_time = `${date_timestamp.split(":")[0]}:${date_timestamp.split(":")[1]}`;
        } else {
            since_time = `Now - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display that the message was sent now
        }

        if (user_id == CURRENT_USER_ID) {
            html_template.setAttribute("class", "col-xl-12 offset-xl-0 d-flex flex-column justify-content-end align-items-end sender-message");
            html_template.setAttribute("id", `message-id-${id}`);
            html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start align-items-end">
                                        <span class="username-span">${username}<br /></span>
                                        <span class="message-span">${message.replace("\n", "<br>")}</span>
                                        <span class="date-span">${since_time}</span>
                                    </p>`;
        } else {
            html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-start align-items-start receiver-message");
            html_template.setAttribute("id", `message-id-${id}`);
            html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start align-items-start align-content-start">
                                            <span class="username-span">${username}<br /></span>
                                            <span class="message-span">${message.replace("\n", "<br>")}</span>
                                            <span class="date-span">${since_time}</span>
                                        </p>`;
        }
        document.querySelector(".hero-1-message-holder").prepend(html_template);
    } else if (data.status === "alert") {
        alertMessage(data, "loadMessage");
    }
}

// Display the messages
createMessage = (data) => {

    if (data.status === "message") {
        let id = data.id;
        let message = data.message;
        let username = data.username;
        let user_id = data.user_id;

        // Create the div to display the message
        let html_template = document.createElement("div");

        // Get the time since message
        let m_timestamp = Math.round((new Date().getTime() - new Date(data.date+" UTC").getTime()) / 60000);

        // Create the timestamps for the displayed messages
        let since_time = ""
        let date_timestamp = `${new Date(data.date+" UTC")}`; // Display the day the message was sent
        if (m_timestamp < 60 && m_timestamp > 0) {
            since_time = `${m_timestamp} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of minutes gone by
        } else if ((m_timestamp / 60) > 0 && (m_timestamp / 60) < 25) {
            since_time = `${Math.round(m_timestamp / 60 % 24)} hours ${m_timestamp % 60} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of hours and minutes gone by
        } else if ((m_timestamp / 60) > 23) {				
            since_time = `${date_timestamp.split(":")[0]}:${date_timestamp.split(":")[1]}`;
        } else {
            since_time = `Now - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display that the message was sent now
        }

        if (user_id == CURRENT_USER_ID) {
            html_template.setAttribute("class", "col-xl-12 offset-xl-0 d-flex flex-column justify-content-end align-items-end sender-message");
            html_template.setAttribute("id", `message-id-${id}`);
            html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start align-items-end">
                                        <span class="username-span">${username}<br /></span>
                                        <span class="message-span">${message.replace("\n", "<br>")}</span>
                                        <span class="date-span">${since_time}</span>
                                    </p>`;
        } else {
            html_template.setAttribute("class", "col-xl-12 d-flex flex-column justify-content-start align-items-start receiver-message");
            html_template.setAttribute("id", `message-id-${id}`);
            html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start align-items-start align-content-start">
                                            <span class="username-span">${username}<br /></span>
                                            <span class="message-span">${message.replace("\n", "<br>")}</span>
                                            <span class="date-span">${since_time}</span>
                                        </p>`;
        }
        document.querySelector(".hero-1-message-holder").append(html_template);
    } else if (data.status === "alert") {
        alertMessage(data, "createMessage");
    }
}

alertMessage = (data, MessageStatus) => {

    let id = data.id;
    let message = data.message;
    let username = data.username;

    // Get the time since message
    let m_timestamp = Math.round((new Date().getTime() - new Date(data.date+" UTC").getTime()) / 60000);

    // Create the timestamps for the displayed messages
    let since_time = ""
    let date_timestamp = `${new Date(data.date+" UTC")}`; // Display the day the message was sent
    if (m_timestamp < 60 && m_timestamp > 0) {
        since_time = `${m_timestamp} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of minutes gone by
    } else if ((m_timestamp / 60) > 0 && (m_timestamp / 60) < 25) {
        since_time = `${Math.round(m_timestamp / 60 % 24)} hours ${m_timestamp % 60} minutes ago - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display the amount of hours and minutes gone by
    } else if ((m_timestamp / 60) > 23) {				
        since_time = `${date_timestamp.split(":")[0]}:${date_timestamp.split(":")[1]}`;
    } else {
        since_time = `Now - ${date_timestamp.split(" ")[4].split(":")[0]+":"+date_timestamp.split(" ")[4].split(":")[1]}`; // Display that the message was sent now
    }

    let html_template = document.createElement("div");
    html_template.setAttribute("class", "col-xl-12 offset-xl-0 d-flex flex-column justify-content-start align-items-center alert-message");
    html_template.setAttribute("id", `message-id-${id}`);
    html_template.innerHTML = `<p class="text-break d-flex flex-column justify-content-start align-items-center">
                                    <span class="message-span">${username} - ${message}<br /></span>
                                    <span class="date-span">${since_time}</span>
                                </p>`;

    if (MessageStatus === "loadMessage") {
        document.querySelector(".hero-1-message-holder").prepend(html_template);
    } else if (MessageStatus === "createMessage") {
        document.querySelector(".hero-1-message-holder").append(html_template);
    }
}
