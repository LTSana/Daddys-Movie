/* JavaScript for Add movie page */

// Trigger the upload picture input
document.querySelector("#select-movie-cover-btn").onclick = () => {
  document.querySelector("#movie-cover-input").click() // trigger a click
}

// Check the profile picture
document.querySelector("#movie-cover-input").onchange = () => {
  let image = document.querySelector("#movie-cover-input");
  if (image.files[0].type.match("image.*")) {
      if (image.files && image.files[0]) {
          if (image.files[0].type == "image/png") {
              let img = image.files[0].size;
              let imgsize = img / 1024;
              if (imgsize <= 2000) {

                  const file = document.querySelector("#movie-cover-input");
                  // Preview image
                  let reader = new FileReader();
                  if (file.files[0].type.match("image.*")) {
                      reader.readAsDataURL(file.files[0]); // convert to base64 string
                  }
                  reader.addEventListener("loadend", () => {
                    document.querySelector("#movie-cover-name-label").innerHTML = "Cover image is ready!";
                    document.querySelector("#movie-cover-name-label").style.color = "rgb(97,255,0)";
                  }, false)
              } else {
                  document.querySelector("#movie-cover-name-label").innerHTML = "Image too large (2Mbs or less)";
                  document.querySelector("#movie-cover-name-label").style.color = "rgb(255,153,0)";
                  document.querySelector("#movie-cover-input").value = "";
              }
          } else if (image.files[0].type == "image/jpeg") {
              let img = image.files[0].size;
              let imgsize = img / 1024;
              if (imgsize <= 9000) {

                  const file = document.querySelector("#movie-cover-input");
                  // Preview image
                  let reader = new FileReader();
                  if (file.files[0].type.match("image.*")) {
                      reader.readAsDataURL(file.files[0]); // convert to base64 string
                  }
                  reader.addEventListener("loadend", () => {
                    document.querySelector("#movie-cover-name-label").innerHTML = "Cover image is ready!";
                    document.querySelector("#movie-cover-name-label").style.color = "rgb(97,255,0)";
                  }, false)
              } else {
                  document.querySelector("#movie-cover-name-label").innerHTML = "Image too large (2Mbs or less)";
                  document.querySelector("#movie-cover-name-label").style.color = "rgb(255,153,0)";
                  document.querySelector("#movie-cover-input").value = "";
              }
          } else {
              document.querySelector("#movie-cover-name-label").innerHTML = "Image not PNG/JPEG";
              document.querySelector("#movie-cover-name-label").style.color = "rgb(255,153,0)";
              document.querySelector("#movie-cover-input").value = "";
          }
      }
  } else {
      document.querySelector("#movie-cover-name-label").innerHTML = "Not Image file.";
      document.querySelector("#movie-cover-name-label").style.color = "rgb(255,153,0)";
      document.querySelector("#movie-cover-input").value = "";
  }
}

// Submit add movie form
document.querySelector("#add-movie-form").addEventListener("submit", (e) => {

  // prevent the page from reloading
  e.preventDefault()

  // Disable the submit button
  document.querySelector("#addmovie-form-btn").disabled = true;

  // Get the movie details
  let movieTitle = document.querySelector("#movie-title").value;
  let movieLink = document.querySelector("#direct-link").value;

  // Get the file
  let file = document.querySelector("#movie-cover-input");
  // Get the image in base64
  let reader = new FileReader();
  if (file.files[0].type.match("image.*")) {
      reader.readAsDataURL(file.files[0]); // convert to base64 string
  }
  reader.addEventListener("loadend", () => {
      fetch(`${BACKEND_HOST}/core/movies`,{
          method: "POST",
          headers: {
              "Content-Type": "application/json",
              //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
              "X-CSRFToken": CSRFTOKEN,
          },
          body: JSON.stringify({
              "action": "add",
              "title": movieTitle,
              "link": movieLink,
              "coverPicture": reader.result,
          })
      }).then(res => res.json()).then(json => {

          // Enable the submit button
          document.querySelector("#addmovie-form-btn").disabled = false;
          
          // Check the response status
          if (json.status === 200) {

            // Empty the fields
            document.querySelector("#movie-title").value = "";
            document.querySelector("#direct-link").value = "";
            document.querySelector("#movie-cover-input").value = "";
            document.querySelector("#movie-cover-name-label").innerHTML = "No file here yet.";
            document.querySelector("#movie-cover-name-label").style.color = "rgb(255,255,255)";

            // refresh the list of movies
            makeMovieList();

            ALERT_MESSAGE("#addmovie-alert", json.message);
          } else {
            console.log(json)
            ALERT_MESSAGE("#addmovie-alert", json.message);
          }
      })
  }, false);
});

// Attempt to get the all the movies
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

      // Ready the forms
      removeFormReady();
    } else {
      console.log(json);
    }
  });
}
makeMovieList();

createMovieList = (data) => {

  // Remove the no movies alert
  if (document.querySelector(".hero-1-col-1-movies-alert")) {
    document.querySelector(".hero-1-col-1-movies-alert").remove();
  }
  
  
  const html_template = document.createElement("div");
  html_template.setAttribute("class", "row hero-1-row-1-movies");
  html_template.setAttribute("id", `movie-row-${data.id}`);
  html_template.innerHTML = `
      <div class="col-xl-3">
      <img class="rounded" src="${data.cover}" width="100%" height="100%" />
      </div>
      <div class="col">
          <h4 class="text-break">${data.title}</h4>
          <form class="remove-movie-form" action="/movies?action=delete" method="POST" data-movieid="${data.id}">
              <span class="sr-only" id="csrf-token">{% csrf_token %}</span>
              <div class="form-group">
              <input type="hidden" class="form-control" name="movie-id" value="${data.id}" />
              <button class="btn btn-dark" type="submit">Remove Movie</button></div>
          </form>
      </div>
  `;

  // Add the template to the movie list
  document.querySelector(".hero-1-col-1-movies").append(html_template);
}

// Remove the movie
removeFormReady = () => {
  document.querySelectorAll(".remove-movie-form").forEach(form => {
  
    // Listen for when one of the forms is submitted
    form.addEventListener("submit", (e) => {
      
      // prevent the page from reloading
      e.preventDefault()
  
      console.log(form.dataset.movieid);
  
      fetch(`${BACKEND_HOST}/core/movies`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          //"Authorization": `${TOKEN.type} ${TOKEN.access}`,
          "X-CSRFToken": CSRFTOKEN,
        },
        body: JSON.stringify({
          "action": "delete",
          "movieID": form.dataset.movieid,
        })
      }).then(res => res.json()).then(json => {
        console.log(json);
        // Check the response status
        if (json.status === 200) {
          document.querySelector(`#movie-row-${form.dataset.movieid}`).remove();
          ALERT_MESSAGE("#addmovie-alert", json.message);
        } else {
          ALERT_MESSAGE("#addmovie-alert", json.message);
        }
      })
    });
  })
}
