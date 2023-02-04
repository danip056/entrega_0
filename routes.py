import sys
import os
sys.path.append(os.path.dirname(__file__))

from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    jsonify
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError


from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app,db,login_manager,bcrypt
from models import User, Event, EventCategoryEnum
from forms import login_form, register_form, EventForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)



# Login route
@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )

# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            
            newuser = User(
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )
    
            db.session.add(newuser)
            db.session.commit()
            flash(f"Account Succesfully created", "success")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )
 
@app.route("/add_event/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def put_event():
    form = EventForm()
    if form.validate_on_submit():
        try:
            user_id = current_user.id
            name = form.name.data
            category = form.category.data
            place = form.place.data
            address = form.address.data
            start_datetime = form.start_datetime.data
            end_datetime = form.end_datetime.data
            is_virtual = form.is_virtual.data

            new_event = Event(
                user_id = user_id,
                name=name,
                category=EventCategoryEnum(category),
                place = place,
                address=address,
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                is_virtual=is_virtual,
            )

            db.session.add(new_event)
            db.session.commit()
            flash(f"Entry Succesfully created", "success")
            return redirect(url_for("add_event"))
        except:
            pass

    return render_template("add_event.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Add event"
        )

@app.route("/list_events/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def list_events():
    user_id = current_user.id
    events = Event.query.filter(Event.user_id == user_id).all()
    return jsonify([event.serialize() for event in events])

@app.route("/api/event/<id>", methods=("GET", "POST"), strict_slashes=False)
#@login_required
def show_event_api(id):
    user_id = current_user.id
    event = Event.query.get_or_404(id)
    return jsonify(event.serialize())

@app.route("/event/<id>", methods=("GET", "POST"), strict_slashes=False)
#@login_required
def show_event(id):
    event = show_event_api(id).json
    return render_template(
        "event_detail.html",
        event=event,
        )

@app.route("/event/<id>/delete", methods=("GET", "POST"), strict_slashes=False)
#@login_required
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/event/<id>/update", methods=("GET", "POST"), strict_slashes=False)
@login_required
def update_event(id):
    user_id = current_user.id
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)
    #form = form.populate_obj(event)
    if form.validate_on_submit():
        try:
            name = form.name.data
            category = form.category.data
            place = form.place.data
            address = form.address.data
            start_datetime = form.start_datetime.data
            end_datetime = form.end_datetime.data
            is_virtual = form.is_virtual.data

            event.name = name
            event.category = category
            event.place = place
            event.address = address
            event.start_datetime = start_datetime
            event.end_datetime = end_datetime
            event.is_virtual = is_virtual

            db.session.commit()

            flash(f"Entry Succesfully updated", "success")
            return redirect(url_for("update_event"))
        except:
            pass

    return render_template(
        "add_event.html",
        form=form,
        text="Update event",
        title="Update event",
        btn_action="Update event"
        )


# Home route
@app.route("/", methods=("GET", "POST"), strict_slashes=False)
@login_required
def home():
    response = list_events()
    return render_template("home.html",title="Home", events=response.json)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)