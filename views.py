# -*- coding: utf8 -*-
from datetime import datetime
from copy import deepcopy
import json
from functools import wraps
from flask import render_template, request, redirect, url_for, jsonify, session, flash

from infodesk import app
import constants
from models import User, Merchant

def can_you(func):
	@wraps(func)
	def wrapper(*args, **kwds):
		if not "uid" in session:
			return "First login"

		resource = func.__name__

		user = User.get_by_id(session["uid"])

		if not user.role in constants.roles:
			return "Unknown role for user %s" % user
	
		role_access_list = constants.roles[user.role]
		user_access_list = json.loads(user.access_list) if user.access_list else {}

		access_list = deepcopy(role_access_list)

		for rsc, acts in user_access_list.items():
			if rsc in access_list:
				access_list[rsc].append(acts)
			else:
				access_list[rsc] = acts

		if request.method == "POST":
			action = kwds.get("action", "update")
		else:
			action = "read"

		# check if action is available for resource
		if action not in constants.resources[resource]:
			return "Invalid action '%s' with %s" % (action, resource)

		if resource not in access_list or action not in access_list[resource]:
			return "Action '%s' with %s not allowed for %s" % (action, resource, user)

		return func(user = user, *args, **kwds)

	return wrapper

@app.route('/login/<username>')
def login(username):
	user = User.get_by_name(username)
	session["uid"] = user.id
	return "Logged in as %s" % username

@app.route('/logout')
@can_you
def logout(user):
	session.pop("uid", None)
	return "Logged out!"

@app.route('/')
@can_you
def index(user):
	return "{0:%d-%m-%Y %H:%M:%S} => Hello, {1}, from info-desk!".format(datetime.now(), user)

@app.route('/users', methods = ["GET"])	
@app.route('/users/<action>', methods = ["POST"])	
@app.route('/users/<int:uid>', methods = ["GET", "POST"])
@app.route('/users/<int:uid>/<action>', methods = ["POST"])
@can_you
def users(user, uid = None, action = None):
	if not uid and not action:
		return "All users"

	if request.method == "GET":
		return render_template("user.html", user = session["user"], user_id = uid)
		
	if not action:
		# post to update user, but not pw or role or access_list
		return "Update user %s" % uid

	return "User action %s" % action

@app.route('/merchants', methods = ["GET"])	
@app.route('/merchants/<action>', methods = ["POST"])	
@app.route('/merchants/<int:uid>', methods = ["GET", "POST"])
@app.route('/merchants/<int:uid>/<action>', methods = ["POST"])
@can_you
def merchants(user, mid = None, action = None):
	if not mid and not action:
		return "All merchants"

	if request.method == "GET":
		return render_template("merchants.html", user = session["user"], mid = mid)
		
	if not action:
		# post to update merchant, but not key
		return "Update merchant %s" % mid

	return "Merchant action %s" % action


@app.route('/merchant', methods = ["GET", "POST"])	
@app.route('/merchant/<action>', methods = ["POST"])
@can_you
def my_merchant(user, action = None):
	user = User.get_by_id(session["user"]) # ? что в сессии хранить
	my_merchant = user.merchant

	return "My merchant %s" % my_merchant

