from django import forms
from django.utils.html import strip_tags

class LoginForm(forms.Form):
    """ Form for validating the login form """

    username = forms.CharField(
        max_length=1200,
        min_length=1,
        required=True,
        label="Username",
        help_text="Enter the username of your account",
        error_messages={
            "invalid": "Username is invalid! Please try again.",
            "required": "Username is required! Please provide one.",
            "max_length": "Username is too long to possibly be in our system.",
            "min_length": "Username is too short be could be the size of an atom.",
        }
    )

    password = forms.CharField(
        max_length=64, 
        min_length=8,
        required=True,
        label="Password",
        help_text="Account password. Needs to be 8 - 64 characters",
        widget=forms.PasswordInput,
        error_messages={
            "max_length": "Password is too long it wouldn't find in the key holder.",
            "min_length": "Password is too short it fell off the key holder.",
            "required": "Password is required! Please provide one.",
            "invalid": "Password was invalid! Please check your password.",
        },
    )


class MovieForm(forms.Form):
    """ Form for validating the movie requests and posts """

    # The options for the types of options
    ACTION_OPTION = (
        ("delete", "delete"),
        ("add", "add"),
        ("fetch", "fetch")
    )

    action = forms.ChoiceField(
		choices=ACTION_OPTION,
		required=True,
		label="Action option",
		help_text="The action option type.",
		error_messages={
			"invalid": "Action option is invalid! Please provide either fetch, add or delete.",
			"required": "Please provide a action option. Fetch, add or delete.",
		},
	)

    movieID = forms.IntegerField(
        min_value=0,
        required=False,
        label="Movie ID",
        help_text="The movie ID to look for the movie",
        error_messages={
            "invalid": "Movie ID is invalid! Please make sure it is an integer.",
            "min_value": "Movie ID is invalid! Please make sure it is a positive integer",
            "required": "Movie ID is required! Please provide one",
        }
    )

    title = forms.CharField(
        max_length=1200,
        min_length=1,
        required=False,
        label="Movie title",
        help_text="Enter the title of your movie",
        error_messages={
            "invalid": "Movie title is invalid! Please try again.",
            "required": "Movie title is required! Please provide one.",
            "max_length": "Movie title is too long to possibly be in our system.",
            "min_length": "Movie title is too short be could be the size of an atom.",
        }
    )

    link = forms.URLField(
        required=False,
        max_length=1500,
        label="Movie Link",
        help_text="The link to the movie",
        error_messages={
            "required": "Movie link is required! Please provide one.",
            "max_length": "Movie link is too Long! Please make sure it's less than 500 character.",
            "invalid": "Movie link is invalid! Please make sure your URL does not contain any special characters."
        }
    )

    def clean(self):
        cleaned_data = super(MovieForm, self).clean()
        action = cleaned_data.get("action")
        movieID = cleaned_data.get("movieID")
        title = cleaned_data.get("title")
        link = cleaned_data.get("link")

        if action == "add":
            if not title:
                self.add_error("title", "Movie title is required! Please provide one.")

            if not link:
                self.add_error("link", "Movie link is required! Please provide one.")

        if action == "delete":
            if not movieID:
                self.add_error("movieID", "Movie ID is required! Please provide one.")

        # Used to remove html tags from strings
        for item in self.fields.keys():
            try:
                if isinstance(cleaned_data[item], str):
                    cleaned_data[item] = strip_tags(cleaned_data[item])
            except KeyError:
                pass

        return cleaned_data
