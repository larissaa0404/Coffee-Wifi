from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', render_kw={'class':"input"}, validators=[DataRequired()])
    location = StringField("Cafe Location On Google Maps(URL)",render_kw={'class':"input"}, validators=[DataRequired(), URL()])
    open = StringField("Opening Time e.g. 8 AM",render_kw={'class':"input"}, validators=[DataRequired()])
    close = StringField("Closing Time e.g. 5PM",render_kw={'class':"input"}, validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating",render_kw={'class':"input"}, choices=['☕',"☕️☕","☕️☕☕️","☕️☕️☕️️☕️️","☕️☕️☕️☕️☕️"], validators=[DataRequired()])
    wifi_rating = SelectField("Wifi Rating",render_kw={'class':"input"}, choices=["🌐","🌐🌐","🌐🌐🌐","🌐🌐🌐🌐","🌐🌐🌐🌐🌐"], validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class':"btn btn-lg"})

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET","POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():

      with open("cafe_data.csv", mode="a", encoding='utf-8') as file:
            file.write(f"\n{form.cafe.data};"
                       f"{form.location.data};"
                       f"{form.open.data};"
                       f"{form.close.data};"
                       f"{form.coffee_rating.data};"
                       f"{form.wifi_rating.data}")
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe_data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=';')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
