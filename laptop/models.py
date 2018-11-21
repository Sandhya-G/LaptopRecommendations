from werkzeug.security import generate_password_hash, check_password_hash
from laptop import db
from flask_login import UserMixin
from laptop import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))



application = db.Table('application',
    db.Column('model_id', db.Integer, db.ForeignKey('lap_mod.model_id')),
    db.Column('a_id', db.Integer, db.ForeignKey('applications.a_id'))
)

class User(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(63), unique=True)
    password_hash = db.Column(db.String(128),nullable=True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self):
        return (self.user_id)


class LapMod(db.Model):
    model_id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    brand = db.Column(db.String(32), nullable=False)
    image_file = db.Column(db.String(64),  default='default.jpg')
    weight = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None), nullable=False)
    dimensions = db.Column(db.String(64), nullable=False)
    os = db.Column(db.String(64), nullable=False)
    warranty = db.Column(db.String(32), nullable=False)
    ratings = db.Column(db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None), nullable=False)
    price = db.Column(db.String(32), nullable=False)
    # n to 1 relationship between a processor and laptop
    proc_id = db.Column(db.Integer, db.ForeignKey('processor.pro_id'))
    #n to 1 relationship between memory and laptop
    memo_id = db.Column(db.Integer, db.ForeignKey('memory.mem_id'))
    #n to 1 relationship between grapgics and laptop
    gid = db.Column(db.Integer, db.ForeignKey('graphics.g_id'))
    # n to 1 reationship between battery and laptop
    bid = db.Column(db.Integer, db.ForeignKey('battery.b_id'))
    # m-n relationship between laptop and application
    hasapps = db.relationship(
        'Applications', secondary=application,
        backref=db.backref('apps', cascade="all,delete-orphan",single_parent=True, lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.model_id)


class Processor(db.Model):
    pro_id = db.Column(db.Integer, primary_key=True)
    proName = db.Column(db.String(32), nullable=False)
    proType= db.Column(db.String(32), nullable=False)
    speed = db.Column(db.String(32), nullable=False)
    noCores = db.Column(db.String(32), nullable=False)
    bit = db.Column(db.Integer, nullable=False)
    gen = db.Column(db.Integer, nullable=False)
    plap = db.relationship('LapMod', backref='lapp', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.proName)

class Memory(db.Model):
    mem_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.String(15), nullable=False)
    ram = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20),nullable=False)
    ssd = db.Column(db.String(20), default='No')
    rpm = db.Column(db.String(15), nullable=False)
    mlap = db.relationship('LapMod', backref='lapm', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.capacity)

class Graphics(db.Model):
    g_id = db.Column(db.Integer, primary_key=True)
    gName = db.Column(db.String(32), nullable=False)
    gType = db.Column(db.String(32), nullable=False)
    gMemory = db.Column(db.String(32), nullable=False)
    glap = db.relationship('LapMod', backref='lapg', lazy='dynamic')



class Battery(db.Model):
    b_id = db.Column(db.Integer, primary_key=True)
    cells = db.Column(db.Integer, nullable=False)
    power = db.Column(db.String(32),nullable=False)
    life = db.Column(db.String(32),nullable=False)
    blap = db.relationship('LapMod', backref='lapb', lazy='dynamic')

class Applications(db.Model):
    a_id = db.Column(db.Integer, primary_key=True)
    application = db.Column(db.String(32), nullable=False)

class triggerInsert(db.Model):
    ti_id = db.Column(db.Integer, primary_key=True)
    userInsert = db.Column(db.String(32), nullable=False)
    modelNo = db.Column(db.String(32), nullable=False)

class triggerUpdate(db.Model):
    tu_id = db.Column(db.Integer, primary_key=True)
    userUpdate = db.Column(db.String(32), nullable=False)
    modelNo = db.Column(db.String(32), nullable=False)

class triggerDelete(db.Model):
    td_id = db.Column(db.Integer, primary_key=True)
    userDelete = db.Column(db.String(32), nullable=False)
    modelNo = db.Column(db.String(32), nullable=False)