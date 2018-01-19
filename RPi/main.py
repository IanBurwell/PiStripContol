from flask import *
from flask_wtf import FlaskForm
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from wtforms import SubmitField, SelectField, DecimalField
from wtforms.validators import NumberRange
from wtforms_components import ColorField
import helpers
from flask_bootstrap import Bootstrap
from led_control import StripControl

app = Flask(__name__) # create the application instance :)
app.config['SECRET_KEY'] = 'secret key'
Bootstrap(app)
nav = Nav()
nav.init_app(app)
strips = StripControl()

@app.route('/')
def index():
    colors = helpers.getDataDict("current")
    return render_template("home.html", c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']))

@nav.navigation()
def top_nav():
    items = [View('Home', 'index'), View('Picker', 'picker'), View('Presets', 'presetList'), View('Sequencer', 'sequencer')]
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
        color = tuple([round(255*val, 2) for val in form.colorPick.data.rgb])
        if form.strip1.data:
            helpers.editDataItem('current', '0', color)
            strips.setStripColor(0, color)
            print(color)
        if form.strip2.data:
            helpers.editDataItem('current', '1', color)
            strips.setStripColor(1, color)
        if form.strip3.data:
            helpers.editDataItem('current', '2', color)
            strips.setStripColor(2, color)
        if form.strip4.data:
            helpers.editDataItem('current', '3', color)
            strips.setStripColor(3, color)
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
            strips.setStripColor(i, presetData[form.presets.data][i])
            helpers.editDataItem('current', str(i), presetData[form.presets.data][i])
    colors = helpers.getDataDict("current")
    return render_template("presets.html", c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']), form=form)

#PRESETS
class SequencerForm(FlaskForm):
    colorPick = ColorField(label='')

    s1 = SubmitField(label='1')
    s2 = SubmitField(label='2')
    s3 = SubmitField(label='3')
    s4 = SubmitField(label='4')
    s5 = SubmitField(label='5')
    s6 = SubmitField(label='6')
    s7 = SubmitField(label='7')
    s0 = SubmitField(label='0')

    c0 = SubmitField(label='1')
    c1 = SubmitField(label='2')
    c2 = SubmitField(label='3')
    c3 = SubmitField(label='4')

    onTime = DecimalField("On Time", places=2, validators=[NumberRange(min=0.00999999999, max=30, message="Must be 0.01-30")])
    fadeTime = DecimalField("Fade Time", places=2, validators=[NumberRange(min=0, max=30, message="Must be 0.01-30")])


@app.route('/sequencer', methods = ['GET','POST'])
def sequencer():
    form = SequencerForm(request.form)
    colors = helpers.getDataDict("current")
    tempSequence = helpers.getDataDict("sequences")['temp']
    if request.method == 'GET':
        form.onTime.data = helpers.getDataDict("sequences")['onTime']
        form.fadeTime.data = helpers.getDataDict("sequences")['fadeTime']
    if request.method == 'POST' and form.validate():
        color = tuple([round(255*val, 2) for val in form.colorPick.data.rgb])
        if form.s0.data:
            tempSequence[0] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s1.data:
            tempSequence[1] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s2.data:
            tempSequence[2] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s3.data:
            tempSequence[3] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s4.data:
            tempSequence[4] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s5.data:
            tempSequence[5] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s6.data:
            tempSequence[6] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.s7.data:
            tempSequence[7] = color
            helpers.editDataItem('sequences', 'temp', tempSequence)
        if form.c0.data:
            helpers.editDataItem('sequences', '0', tempSequence)
            strips.setState(sequence=helpers.getDataDict('sequences'))
        if form.c1.data:
            helpers.editDataItem('sequences', '1', tempSequence)
            strips.setState(sequence=helpers.getDataDict('sequences'))
        if form.c2.data:
            helpers.editDataItem('sequences', '2', tempSequence)
            strips.setState(sequence=helpers.getDataDict('sequences'))
        if form.c3.data:
            helpers.editDataItem('sequences', '3', tempSequence)
            strips.setState(sequence=helpers.getDataDict('sequences'))
        helpers.editDataItem('sequences', 'onTime', form.onTime.data)
        helpers.editDataItem('sequences', 'fadeTime', form.fadeTime.data)

    return render_template("sequencer.html", form=form,
                                            s0=helpers.tupleToHex(tempSequence[0]),
                                            s1=helpers.tupleToHex(tempSequence[1]),
                                            s2=helpers.tupleToHex(tempSequence[2]),
                                            s3=helpers.tupleToHex(tempSequence[3]),
                                            s4=helpers.tupleToHex(tempSequence[4]),
                                            s5=helpers.tupleToHex(tempSequence[5]),
                                            s6=helpers.tupleToHex(tempSequence[6]),
                                            s7=helpers.tupleToHex(tempSequence[7]),
                                            c0=helpers.tupleToHex(colors['0']),
                                            c1=helpers.tupleToHex(colors['1']),
                                            c2=helpers.tupleToHex(colors['2']),
                                            c3=helpers.tupleToHex(colors['3']))


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    except KeyboardInterrupt:
        strips.stop()
