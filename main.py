import os
from multiprocessing import Process
from flask import Flask, render_template, redirect

from control import control_temp
from sensors import read_sensors
from interface import read_interface, write_interface
from settings import INTERFACE_TEMP, INTERFACE_ACTIVE

# Start temperature control loop.
control_process = Process(target=control_temp)
control_process.start()


def create_app(test_config=None):
    # create and configure the app
    app = Flask('koelkast', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # TODO initialise ACTIVE to 0

    # a simple page that says hello
    @app.route('/', methods=('GET', 'POST'))
    def index():
        from forms.temperature_form import TemperatureForm
        form = TemperatureForm()
        current_temp = read_sensors()[-1] # Final entry is average temp.
        active = read_interface(INTERFACE_ACTIVE)
        # Provide current goal temp.
        form.temperature.data = read_interface(INTERFACE_TEMP)
        if form.validate_on_submit():
            write_interface(INTERFACE_TEMP, form.temperature.data)

        return render_template('index.html', form=form, current_temp=current_temp, active=active)

    @app.route('/start/', methods=('GET', 'POST'))
    def start():
        write_interface(INTERFACE_ACTIVE, 1)
        print("START")
        return redirect('/')

    @app.route('/stop/', methods=('GET', 'POST'))
    def stop():
        write_interface(INTERFACE_ACTIVE, 0)
        print("STOP")
        return redirect('/')

    return app




