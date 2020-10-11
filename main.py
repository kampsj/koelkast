from multiprocessing import Process
from flask import Flask, render_template, redirect

from control import control_loop
from sensors import read_sensors
from switch import Switch
from interface import read_interface, write_interface
from settings import INTERFACE_TEMP, INTERFACE_ACTIVE, COOL_PIN

import asyncio
from functools import wraps
import datetime as dt

def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

def create_app(test_config=None):
    # create and configure the app
    app = Flask('koelkast', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # a simple page that says hello
    @app.route('/', methods=('GET', 'POST'))
    @async_action
    async def index():
        """
        Main page with option to turn cooling on/off and change the goal temp.
        """
        from forms.temperature_form import TemperatureForm

        form = TemperatureForm()

        # This slows the page down significantly.
        # Acceptable since the page is hardly used.
        current_temp = await read_sensors() # Final entry is average.

        active = read_interface(INTERFACE_ACTIVE)

        if form.validate_on_submit():
            write_interface(INTERFACE_TEMP, form.temperature.data)

        # Provide current goal temp.
        form.temperature.data = read_interface(INTERFACE_TEMP)
        return render_template('index.html', form=form, current_temp=current_temp[-1], active=active)

    @app.route('/start/', methods=('GET', 'POST'))
    def start():
        """
        Route to activate the control loop
        """
        write_interface(INTERFACE_ACTIVE, 1)
        return redirect('/')

    @app.route('/stop/', methods=('GET', 'POST'))
    def stop():
        """
        Route to deactivate the control loop
        """
        write_interface(INTERFACE_ACTIVE, 0)
        return redirect('/')

    return app


# Start temperature control loop.
switch = Switch(COOL_PIN)
control_process = Process(target=control_loop, args=(switch,))
control_process.start()


