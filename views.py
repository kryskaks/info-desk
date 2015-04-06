from infodesk import app
from flask import render_template, request, redirect, url_for, jsonify, session, flash
from datetime import datetime
from functools import wraps
import constants

users_map = {
"ksu": 
	{
		"logout": ["read"],
		"users": ["new", "read", "update", "role"]		
	},
"test":
	{
		"logout": ["read"],
		"index": ["read"],
		"users": ["read", "update"]
	}
}

def can_you(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		if not "user" in session:
			return "First login"

		resource = func.__name__

		user_access_list = users_map[session["user"]]

		if request.method == "POST":
			action = kwds.get("action", "update")
		else:
			action = "read"

		# check if action is available for resource
		if action not in constants.resources[resource]:
			return "Invalid action '%s' with %s" % (action, resource)

		if resource not in user_access_list or action not in user_access_list[resource]:
			return "Action '%s' with %s not allowed for %s" % (action, resource, session["user"])

		return func(*args, **kwds)

	return wrapper

@app.route('/login/<username>')
def login(username):
	session["user"] = username
	return "Logged in as %s" % username

@app.route('/logout')
@can_you
def logout():
	session.pop("user", None)
	return "Logged out!"

@app.route('/')
@can_you
def index():
	return "{0:%d-%m-%Y %H:%M:%S} => Hello, {1}, from info-desk!".format(datetime.now(), session["user"])

@app.route('/users', methods = ["GET"])	
@app.route('/users/<action>', methods = ["POST"])	
@app.route('/users/<int:uid>', methods = ["GET", "POST"])
@app.route('/users/<int:uid>/<action>', methods = ["POST"])
@can_you
def users(uid = None, action = None):
	if not uid and not action:
		return "All users"

	if request.method == "GET":
		return render_template("user.html", user = session["user"], user_id = uid)
		
	if not action:
		# post to update user, but not pw or role or access_list
		return "Update user %s" % uid

	return "User action %s" % action