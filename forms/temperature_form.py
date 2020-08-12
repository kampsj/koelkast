from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired


class TemperatureForm(FlaskForm):
    """
    Simple temperature form.
    """
    temperature = FloatField("Temperatuur", validators=[DataRequired()])
    submit = SubmitField("Update")
