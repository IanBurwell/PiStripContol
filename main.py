from flask import *
from wtforms import *
from wtforms_components import ColorField
import helpers
app = Flask(__name__) # create the application instance :)

@app.route('/')
def index():
    return 'hallo'

#PICKER
class PickerForm(Form):
    colorPick = ColorField(label='')
    strip1 = SubmitField(label='1')
    strip2 = SubmitField(label='2')
    strip3 = SubmitField(label='3')
    strip4 = SubmitField(label='4')

@app.route('/picker', methods = ['GET','POST'])
def picker():
    form = PickerForm(request.form)
    if request.method == 'POST' and form.validate():
        helpers.setSelected('Custom')
        if form.strip1.data:
            helpers.setColor(0, tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip2.data:
            helpers.setColor(1, tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip3.data:
            helpers.setColor(2, tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
        if form.strip4.data:
            helpers.setColor(3, tuple([round(255*val, 2) for val in form.colorPick.data.rgb]))
    return render_template("picker.html", current=helpers.getCurrentColors(), form=form)

#PRESETS
class ColorForm(Form):
    presets = SelectField(u'Preset', coerce=str)

@app.route('/presets', methods = ['GET','POST'])
def presetList():
    form = ColorForm(request.form)
    form.presets.choices = helpers.getColorPresetNames()
    selected = helpers.getSelected()
    if request.method == 'POST' and form.validate():
        selected = form.presets.data
        helpers.setSelected(form.presets.data)
    return render_template("presets.html", form=form, selected=selected)


if __name__ == '__main__':
    app.run(debug=True)
