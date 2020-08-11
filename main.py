from multiprocessing import Process
from flask import Flask, render_template, redirect

from control import control_loop
from sensors import read_sensors
from switch import Switch
from interface import read_interface, write_interface
from settings import INTERFACE_TEMP, INTERFACE_ACTIVE, COOL_PIN


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
        # This slows the page down significantly.
        # Acceptable since the page is hardly used.
        current_temp = read_sensors()[-1]  # Final entry is average.
        active = read_interface(INTERFACE_ACTIVE)
        # Provide current goal temp.

        if form.validate_on_submit():
            print("WRITING DATA")
            print("form data: " + str(form.temperature.data))

            write_interface(INTERFACE_TEMP, form.temperature.data)
        else:
            print(form.errors.items())

        form.temperature.data = read_interface(INTERFACE_TEMP)
        return render_template('index.html', form=form, current_temp=current_temp, active=active)

    @app.route('/start/', methods=('GET', 'POST'))
    def start():
        write_interface(INTERFACE_ACTIVE, 1)
        return redirect('/')

    @app.route('/stop/', methods=('GET', 'POST'))
    def stop():
        write_interface(INTERFACE_ACTIVE, 0)
        return redirect('/')

    return app


# Start temperature control loop.
switch = Switch(COOL_PIN)
control_process = Process(target=control_loop, args=(switch,))
control_process.start()


