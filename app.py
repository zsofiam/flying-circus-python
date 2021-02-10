from flask import Flask, session, redirect, url_for, escape, request, render_template
import data


app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def index():
    if 'email' in session and 'password' in session and session['email'] in data.users \
            and data.verify_password(session['password'], data.users[session['email']]):
        return '<small>Logged in as %s </small>' \
               '<h3>Hello, %s!</h3>' \
               '<p>We are so happy to see you here!<p>' \
               '<a href="/test">complete test</a>' \
               '<br><br>' \
               '<a href="/logout">Logout</a>' % (escape(session['email']), escape(session['email']))
    #return 'You are not logged in'
    return '<small>You are not logged in! </small>' \
           '<br><br>' \
           '<a href="/login">Login</a>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        password = session['password']
        if 'email' in session and 'password' in session and session['email'] in data.users \
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


@app.route('/test')
def test():
    if 'email' in session and 'password' in session and session['email'] in data.users \
            and data.verify_password(session['password'], data.users[session['email']]):
        questions=data.get_questions()
        score = 0
        return render_template("test.html", questions=questions)
    else:
        return redirect(url_for('index'))


@app.route('/result/', methods=["POST"])
def result():
    if request.method == "POST":
        print(request.form)
        questions = data.get_questions()
        score = 0
        for question in questions:
            print(question in request.form, request.form[question])
            if question in request.form and request.form[question] == 'True':
                score += 1
                print(score)
        print(score)
        return render_template("result.html", score=score)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()