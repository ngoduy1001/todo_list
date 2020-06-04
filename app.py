from flask import Flask, request
from flask import render_template
from flask import session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import SignUpForm, LoginForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'anaanatawa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    # posted_by =  db.Column(db.String, db.ForeignKey('user.id'))

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    # tasks = db.relationship('Task', backref = 'user')


db.create_all()


@app.route('/')
# def tasks_list():
#     tasks = Task.query.all()
#     return render_template('list.html', tasks=tasks)
def homepage():
    """View function for Home Page."""
    return render_template("base.html")

@app.route('/todo')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        # make a html for handling error here
        return redirect('/todo')

    task = Task(content)
    db.session.add(task)
    db.session.commit()
    return redirect('/todo')

@app.route('/deleteall', methods=['GET','POST', 'DELETE'])
def delete_all_task():
    try:
        db.session.query(Task).delete()
        db.session.commit()
    except:
        db.session.rollback()
    return redirect('/todo')

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/todo')

    db.session.delete(task)
    db.session.commit()
    return redirect('/todo')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return redirect('/todo')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/todo')

@app.route("/signup", methods=["POST", "GET"])
def signup():
    """View function for Showing Details of Each Pet.""" 
    form = SignUpForm()
    if form.validate_on_submit():
        # new_user = {"id": len(users)+1, "full_name": form.full_name.data, "email": form.email.data, "password": form.password.data}
        # users.append(new_user)
        new_user = User(full_name = form.full_name.data, email = form.email.data, password = form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return render_template("signup.html", form = form, message = "This Email already exists in the system! Please Log in instead.")
        finally:
            db.session.close()
        return render_template("signup.html", message = "Successfully signed up")
    return render_template("signup.html", form = form)

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # user = next((user for user in users if user["email"] == form.email.data and user["password"] == form.password.data), None)
        user = User.query.filter_by(email = form.email.data, password = form.password.data).first()
        if user is None:
            return render_template("login.html", form = form, message = "Wrong Credentials. Please Try Again.")
        else:
            # session['user'] = user
            session['user'] = user.id
            return render_template("login.html", message = "Successfully Logged In!")
    return render_template("login.html", form = form)

@app.route("/logout")
def logout():
    if 'user' in session:
        session.pop('user')
    return redirect(url_for('homepage'))

@app.route("/about")
def about():
    """View function for About Page."""
    return render_template("about.html")



if __name__ == '__main__':
    app.run(debug=True)
