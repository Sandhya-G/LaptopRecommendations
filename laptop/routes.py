from flask import render_template, flash, redirect, url_for
import secrets,os
from PIL import Image
from laptop import app
from laptop.forms import Insert, RegistrationForm, LoginForm, UpdatePrice, UpdateRatings
from flask_login import current_user, login_user, logout_user, login_required
from laptop.models import User, LapMod, Processor, Graphics, Applications, Battery,Memory, triggerDelete, triggerInsert, triggerUpdate
from flask import request
from werkzeug.urls import url_parse
from laptop import db


@app.route("/")
@app.route("/home")
def home():
    form = Insert()
    laps = LapMod.query.all()
    return render_template("main.html",laps=laps, form =form)

@app.route("/insert", methods=['GET', 'POST'])
@login_required
def insert():
    form = Insert()

    try:
        if form.validate_on_submit():
            lap = LapMod(model_id =form.modelNo.data , name=form.lapName.data , brand=form.brandName.data, weight= form.weight.data,
                         dimensions=form.dimen.data, os= form.ops.data,warranty=form.warranty.data,ratings=form.rating.data,
                         price=form.price.data)

            p = Processor.query.filter_by(proName=form.processorName.data).first() and Processor.query.filter_by(proType=form.processorType.data).first() and Processor.query.filter_by(speed=form.speed.data).first() and Processor.query.filter_by(noCores=form.cores.data).first() and Processor.query.filter_by(bit=form.bit.data).first() and Processor.query.filter_by(gen=form.gen.data).first()
            if p is None:
                p = Processor(proName = form.processorName.data , proType= form.processorType.data ,
                        speed=form.speed.data ,noCores=form.cores.data ,bit= form.bit.data, gen = form.gen.data)
                db.session.add(p)
            lap.lapp = p

            m = Memory.query.filter_by(capacity=form.cap.data).first() and Memory.query.filter_by(ram =form.ram.data).first() and  Memory.query.filter_by(type = form.mType.data).first() and Memory.query.filter_by(ssd = form.ssd.data).first() and Memory.query.filter_by(rpm=form.rpm.data).first()
            if m is None :
                m = Memory(capacity=form.cap.data, ram=form.ram.data, type=form.mType.data, ssd=form.ssd.data,
                             rpm=form.rpm.data)
                db.session.add(m)

            lap.lapm = m

            g  = Graphics.query.filter_by(gName=form.graphicsName.data ).first() and Graphics.query.filter_by(gMemory=form.graphicsCapacity.data).first()
            if g is None:
                g = Graphics(gName=form.graphicsName.data, gType=form.graphicsType.data,
                                    gMemory=form.graphicsCapacity.data)
                db.session.add(g)
            lap.lapg = g



            b = Battery.query.filter_by(cells = form.batteryCells.data).first() and Battery.query.filter_by(power = form.batteryPower.data).first() and Battery.query.filter_by(life=form.batteryLife.data).first()
            if b is None :
                b = Battery(cells=form.batteryCells.data, power=form.batteryPower.data, life=form.batteryLife.data)
                db.session.add(b)
            lap.lapb = b


            if form.Gaming.data:
                appls = Applications.query.filter_by(application="Gaming").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.General.data:
                appls = Applications.query.filter_by(application="General").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.WebDevelopment.data:
                appls = Applications.query.filter_by(application="WebDevelopment").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.Programming.data:
                appls = Applications.query.filter_by(application="Programming").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.ML.data:
                appls = Applications.query.filter_by(application="ML").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.VR.data:
                appls = Applications.query.filter_by(application="VR").first()
                appls.apps.append(lap)
                db.session.commit()

            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                lap.image_file = picture_file
            db.session.commit()

            flash('New Laptop added', 'success')

            up = triggerInsert(userInsert=current_user.username, modelNo=lap.model_id)
            db.session.add(up)
            db.session.commit()
            return redirect(url_for('home'))
    except:
        db.session.rollback()
        flash('error occured', 'danger')
    return render_template('insert.html', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/laptopImages', picture_fn)
    output_size = (320, 320)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route("/Display/<string:lap_id>")
def Display(lap_id):
    lap = LapMod.query.get_or_404(lap_id)
    laps = LapMod.query.all()
    return render_template('display.html', lap=lap, name=lap.name ,laps=laps)

@app.route("/updatePrice/<string:lap_id>",methods=['GET', 'POST'])
def updatePrice(lap_id):
    if current_user.is_authenticated:
        form = UpdatePrice()
        if form.validate_on_submit():
            lap = LapMod.query.filter_by(model_id=lap_id).first()
            if lap is None:
                flash("Laptop doesn't exist", 'danger')
                return redirect(home)
            lap.price = form.price.data
            try:
                up = triggerUpdate(userUpdate=current_user.username, modelNo=lap_id)
                db.session.add(up)
                db.session.commit()
                flash('Laptop price updated', 'info')
                return redirect(url_for('home'))
            except:
                db.session.rollback()
    else:
        flash("Log in to update", 'info')
        return redirect(url_for('home'))
    return render_template('updatePrice.html', form=form)


@app.route("/updateRatings/<string:lap_id>",methods=['GET', 'POST'])
def updateRatings(lap_id):
    if current_user.is_authenticated:
        form = UpdateRatings()
        if form.validate_on_submit():
            lap = LapMod.query.filter_by(model_id=lap_id).first()
            if lap is None:
                flash("Laptop doesn't exist", 'danger')
                return redirect(url_for('home'))
            lap.ratings = form.ratings.data
            db.session.commit()
            flash('Laptop price updated', 'info')
            return redirect(url_for('home'))
    else:
        flash("Log in to update", 'info')
        return redirect(url_for('home'))
    return render_template('UpdateRating.html', form=form)

@app.route("/Apps/<int:id>")
def Apps(id):
    laps = Applications.query.filter_by(a_id=id).first()
    laps = laps.apps.all()
    return render_template('list.html', laps=laps)

@app.route("/delete/<string:lap_id>")
def delete(lap_id, methods=['GET', 'POST']):
    if current_user.is_authenticated:
        lap = LapMod.query.filter_by(model_id=lap_id).first()
        try:
            if lap is None:
                flash("Laptop doesn't exist", 'danger')
                return redirect(url_for('home'))
            db.session.delete(lap)
            db.session.commit()
            flash('Laptop deleted', 'danger')
            up = triggerDelete(userDelete=current_user.username, modelNo=lap_id)
            db.session.add(up)
            db.session.commit()
        except:
            db.session.rollback()
        return redirect(url_for('home'))
    else:
        flash("Log in to delete",'info')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
