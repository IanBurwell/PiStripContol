from flask import *
from flask_wtf import FlaskForm
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from wtforms import SubmitField, SelectField
from wtforms_components import ColorField
import helpers
from flask_bootstrap import Bootstrap

app = Flask(__name__) # create the application instance :)
app.config['SECRET_KEY'] = 'secret key'
Bootstrap(app)
nav = Nav()
nav.init_app(app)


@app.route('/')
def index():
    colors = helpers.getDataDict("current")
    return render_template("home.html", c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']))

@nav.navigation()
def top_nav():
    items = [View('Home', 'index'), View('Picker', 'picker'), View('Presets', 'presetList')]
    return Navbar('Strip Control', *items)

#PICKER
class PickerForm(FlaskForm):
    colorPick = ColorField(label='')
    strip1 = SubmitField(label='1')
    strip2 = SubmitField(label='2')
    strip3 = SubmitField(label='3')
    strip4 = SubmitField(label='4')


@app.route('/picker', methods = ['GET','POST'])
def picker():
    form = PickerForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.strip1.data:
            helpers.editDataItem('current', '0', tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip2.data:
            helpers.editDataItem('current', '1', tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip3.data:
            helpers.editDataItem('current', '2', tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip4.data:
            helpers.editDataItem('current', '3', tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
    colors = helpers.getDataDict("current")
    return render_template("picker.html", c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']), form=form)


#PRESETS
class ColorForm(FlaskForm):
    presets = SelectField(u'Preset', coerce=str)
    submit = SubmitField(label='Submit')


@app.route('/presets', methods = ['GET','POST'])
def presetList():
    form = ColorForm(request.form)
    names = list(helpers.getDataDict('presets').keys())
    form.presets.choices = [(name, name.title()) for name in names]
    presetData = helpers.getDataDict('presets')

    if request.method == 'POST' and form.validate():
        selected = 'Preset'
        for i in range(4):
            helpers.editDataItem('current', str(i), presetData[form.presets.data][i])
    colors = helpers.getDataDict("current")
    return render_template("presets.html", c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']), form=form)


if __name__ == '__main__':
    app.run(debug=True)
