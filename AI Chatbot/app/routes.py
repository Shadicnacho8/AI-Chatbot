from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User, Chat
from urllib.parse import urlsplit

from app.chatbot import Chatbot


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title="Chat")


@app.route('/chats', methods=["GET"])
@login_required
def getChats():
    query = sa.select(Chat).where(
        Chat.user_id == int(current_user.id))
    chats = db.session.scalars(query).all()
    chats = chats or []
    return jsonify([i.serialize for i in chats])


@app.route('/chats', methods=["DELETE"])
@login_required
def deleteChats():
    num_rows_deleted = db.session.query(Chat).delete()
    db.session.commit()
    return f'Deleted {num_rows_deleted}.'


@app.route('/chats/content', methods=["GET"])
@login_required
def getChatContent():
    message = request.args.get('msg')
    response = Chatbot.get_ai_response(self=Chatbot, msg=message)
    chat = Chat(msg=message, content=response, user=current_user)
    db.session.add(chat)
    db.session.commit()
    return jsonify(chat.serialize)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash('Already authenticated!', 'success')
        return redirect('index')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password!', 'error')
            return redirect(url_for('login'))
        login_user(user, True)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = 'index'
        flash("User logged in successfully!", 'success')
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration has been done! Please Login!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
