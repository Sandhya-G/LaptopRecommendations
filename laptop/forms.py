from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from laptop.models import User, LapMod

class Insert(FlaskForm):

    picture = FileField('Insert Laptop Picture',
                       validators=[FileAllowed(['jpg', 'png', 'gif'])])
    modelNo = StringField('Model No',
                           validators=[DataRequired()])
    lapName = StringField('Laptop Name',
                          validators=[DataRequired()])
    brandName = StringField('Brand',
                          validators=[DataRequired()])
    ops = StringField('Operting System',
                            validators=[DataRequired()])
    rating = StringField('Ratings',
                            validators=[DataRequired()])
    weight = StringField('Weight',
                            validators=[DataRequired()])
    dimen = StringField('Resolution',
                            validators=[DataRequired()])
    warranty = StringField('Warranty',
                            validators=[DataRequired()])

    price = StringField('Price',
                      validators=[DataRequired()])
    processorName = StringField('Processor Name',
                      validators=[DataRequired()])
    processorType = StringField('Processor Type',
                            validators=[DataRequired()])
    speed = StringField('Speed',
                            validators=[DataRequired()])
    cores = StringField('No of Cores',
                            validators=[DataRequired()])
    gen = StringField('Generation',
                            validators=[DataRequired()])
    bit = StringField('Bit',
                            validators=[DataRequired()])
    cap = StringField('Disk Capacity',
                            validators=[DataRequired()])

    ram = StringField('RAM',
                            validators=[DataRequired()])
    mType = StringField('Memory Type',
                            validators=[DataRequired()])
    ssd = StringField('SSD',
                            validators=[DataRequired()])


    rpm = StringField('RPM',
                            validators=[DataRequired()])
    graphicsName = StringField('GPU',
                      validators=[DataRequired()])
    graphicsType = StringField('Graphics Type',
                            validators=[DataRequired()])
    graphicsCapacity = StringField('Graphics Capacity',
                            validators=[DataRequired()])
    batteryLife = StringField('Battery Life', validators=[DataRequired()])

    batteryPower = StringField('Battery Power',
                            validators=[DataRequired()])

    batteryCells = StringField('Battery Cells',
                            validators=[DataRequired()])
    Gaming = BooleanField('Gaming')
    General = BooleanField('General')
    WebDevelopment = BooleanField('Web Development')
    Programming = BooleanField('Programming')
    ML = BooleanField('Machine Learning')
    VR = BooleanField('Video Rendering')





    submit = SubmitField('Insert')

    def validate_modelNo(self, modelNo):
        id = LapMod.query.filter_by(model_id=modelNo.data).first()
        if id is not None:
            raise ValidationError('Please try different Model No')




class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class Delete(FlaskForm):
    modelNo = StringField('Model No',
                        validators=[DataRequired()])
    submit = SubmitField('Delete')

class UpdatePrice(FlaskForm):
    price = StringField('Price',
                          validators=[DataRequired()])
    submit = SubmitField('Update')

class UpdateRatings(FlaskForm):
    ratings = StringField('Ratings',
                          validators=[DataRequired()])
    submit = SubmitField('Update')




