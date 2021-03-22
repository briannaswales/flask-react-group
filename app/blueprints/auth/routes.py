from . import bp as auth
from app import db
from flask import current_app as app, request, url_for, jsonify
from .forms import UserInfoForm, LoginForm
from app.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.tokens import get_token

#  Thoughts
    #  Rewatch video on using Postman. See if it's applicable to troubleshoot flask.
    #  Resolve problems with signup. 
    #  Add comments
        #  Test if comments work in Postman

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    data = request.json

    if request.method == 'POST' and data['password'] == data['confirm_password']:
        token = None
        token_exp = None
        p = User(data['username'], data['email'], data['password'])
        # print(username, email, password)
        db.session.add(p)
        db.session.commit()
        return jsonify(p.to_dict())
    else:
        return "fail"
    
@auth.route('/login', methods=['GET', 'POST'])
def login():
    title = "EAT | Log In"
    # form = LoginForm()

    # print(request.method)
    # print(form.validate())

    if request.method == 'POST':
        data = request.json
        username = data['username']
        password = data['password']
        remember_me = data['remember_me']

        user = User.query.filter_by(username=username).first()

        if user is None or not check_password_hash(user.password, password):
            message = "Email and/or password is not valid. Please try again."    
            return jsonify({ 'message': message }), 404
        # never calls login function
        login_user(user,remember=remember_me)
        print(current_user)
        return jsonify(user.get_token())
        # return data??? on current user

    else:
        return jsonify("fail")
        # current user is authenticated

@auth.route('/logout')
def logout():
    logout_user()
    message = "You have logged out. Come back to EAT some more real soon!"    
    return jsonify({ 'message': message }), 201

# @auth.route('/myinfo')
# @login_required
# def myinfo():
#     title = "EAT | My Info"
#     data = {
#         "Username": current_user.username,
#         "Email": current_user.email,
#         "Password": current_user.password
#     }
#     return jsonify(data)