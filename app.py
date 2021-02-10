from flask import Flask, session, redirect, url_for, escape, request, render_template
import data


app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'email' in session and 'password' in session and session['email'] in data.users \
            and data.verify_password(session['password'], data.users[session['email']]):
        return 'Logged in as %s <br/><br/><a href="/logout">Logout</a>' % escape(session['email'])
    #return 'You are not logged in'
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        password = session['password']
        if 'email' in session and 'password' in session and session['email'] in data.users\
                and data.verify_password(password, data.users[session['email']]):
            return redirect("/")
        else:
            return '''Wrong password!
            <br/><br/>
            <a href="/logout">Back to main page</a>'''
    return '''
        <form method="post">
            <label for="email">Email:</label>
            <p><input type=email id="email" name=email>
            <br/><br/>
            <label for="password">Password:</label>
            <p><input type=password id="password" name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('email', None)
    session.pop('password', None)
    return redirect(url_for('index'))

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         data_manager.create_comment(request.form.get('name'), request.form.get('text'))
#
#     comments = data_manager.get_comments()
#     return render_template('index.html', comments=comments)


if __name__ == '__main__':
    app.run()