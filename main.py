from loader import *


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        status = users.login_user(request.form.get('login'), request.form.get('password'))
        if not status:
            flash('Неверный логин или пароль')
        else:
            session['authorized'] = True
            session['username'] = request.form.get("login")
            session['password_hash'] = request.form.get("password")
            print(session.items())
            if users.login_user(session.get('username'), session.get('password_hash')):
                return redirect(url_for("feed_page"))
            return redirect(url_for('login'))
    if session.get('authorized') and session.get("username") is not None:
        return redirect(url_for('feed_page'))
    return render_template("login.html")


@app.route("/feed", methods=['GET', 'POST'])
def feed_page():
    if request.method == "POST":
        flash(feed.create_post(users.get_user_by_username(session.get('username'))[0], request.form.get('text')))
        ...

    posts = feed.get_random_posts()
    return render_template('feed.html', posts=posts, users=users)


@app.route("/register")
def reg():
    return render_template("register.html")


valid_code = 0
username = None
email = None
password = None


@app.route("/verify", methods=["POST"])
def verify():
    global valid_code, username, email, password
    if request.method == "POST":
        if request.form.get('login') is not None and request.form.get('email') is not None and request.form.get("password") is not None:
            username = request.form.get('login')
            email = request.form.get('email')
            password = request.form.get('password')
        if valid_code == 0:
            valid_code = mailer_service.send_message(email)
        try:
            print(int(request.form.get("verif_code")), int(valid_code))
            if int(request.form.get("verif_code")) == int(valid_code):
                flash(users.register_user(username, email, password))
            else:
                flash("Код не верный")
        except Exception:
            ...
        return render_template("verify.html")


if __name__ == "__main__":
    app.run(debug=True)
