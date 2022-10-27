Two questions

1. is our reroute via request.referrer a good way to do this?
    a. it goes to top of page...
    b. we need to re-render html because jinja needs to fill/unfill stars!!
        i. so... cache-ing problem??
        
2. what is up with our db.relationship User <--> Liked Message

3. what is in the session anyway?
what about
@app.after_request
def history_()
    history = session.get('history', [])
    history.append((
        request.endpoint,
        request.args
    ))
# is this good??


How is the logged in user being kept track of?
The persistent memory for the logged-in user is in the session (browser session, using the underlying technology of cookies)

What is Flask’s g object?
It is a global object (can be used like a container, setting its properties to relevant data, like the user class instance), available everywhere throughout the Flask app on a per-request basis.

What is the purpose of add_user_to_g?
That is why before every request, we write @app.before_request functions that access the session and get the user instance, and put it in the g object for every single request. We can then very conveniently access user properties inside Jinja without having to explicitly passing it in with every render_template call (especially for putting csrf tokens into every logout form button!)

What does @app.before_request mean?
It runs every time, before any route (not unlike setUp in unittest)
