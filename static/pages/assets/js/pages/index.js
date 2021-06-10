/* JavaScript for index page */

// Get all the movies available
makeMovieList = () => {
    fetch(`${BACKEND_HOST}/core/movies?action=fetch`, {
        method: "GET",
        headers: {
        "Content-Type": "application/json",
        //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
        }
    }).then(res => res.json()).then(json => {

        // Check the response status
        if (json.status == 200) {

            // Loop through the movies
            for (let i = 0; i < json.movies.length; i++) {
                createMovieList(json.movies[i]);
            }

            readySessionCreation();
        } else {
            console.log(json);
        }
    });
}
makeMovieList();

createMovieList = (data) => {

    // Remove the no movies alert
    if (document.querySelector(".hero-2-col-2-movies-alert")) {
        document.querySelector(".hero-2-col-2-movies-alert").remove();
    }
    
    const html_template = document.createElement("div");
    html_template.setAttribute("class", "col-6 col-sm-4 col-md-3 col-lg-2 col-xl-2 hero-2-movie-col");
    html_template.innerHTML = `
    <a class="movie-link-creation" data-movieid="${data.id}">
    <div class="hero-2-movie-col-link-div">
        <div class="row">
            <div class="col-xl-12">
            <img class="rounded" width="100%" height="100%" src="${data.cover}" />
            </div>
        </div>
        <div class="row">
            <div class="col-xl-12">
                <h4 class="text-break text-center">${data.title}</h4>
            </div>
        </div>
    </div>
    </a>`;
  
    // Add the template to the movie list
    document.querySelector(".hero-2-col-2-movies").append(html_template);
}

// Ready to create the movie session
readySessionCreation = () => {

    // Get the nodes of all the movies in the list
    document.querySelectorAll(".movie-link-creation").forEach(movie => {
        movie.onclick = () => {

            // Create the movie session and receive the ID to the session
            fetch(`${BACKEND_HOST}/movie/create`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
                    "X-CSRFToken": CSRFTOKEN,
                },
                body: JSON.stringify({
                    "movieID": movie.dataset.movieid,
                })
            }).then(res => res.json()).then(json => {

                // Check the response status
                if (json.status === 200) {

                    console.log(json);
                    ALERT_MESSAGE("#home-page-alert", `${json.message} Session ID: ${json.session}`);
                    
                    // Go to the movie session
                    location.href = `/watcher?sessionID=${json.session}`;
                    
                } else {
                    console.log(json);
                    ALERT_MESSAGE("#home-page-alert", json.message);
                }
            });
        }
    });
}
