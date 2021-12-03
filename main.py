from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from roommates_bill import room

app = Flask(__name__)


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class BillFormPage(MethodView):

    def get(self):
        bill_form = BillForm()
        return render_template('bill_form_page.html', billform=bill_form)


class ResultsPage(MethodView):

    def post(self):
        billform = BillForm(request.form)

        the_bill = room.Bill(float(billform.amount.data), billform.period.data)
        roommate1 = room.Roommate(billform.name1.data, float(billform.days_in_house1.data))
        roommate2 = room.Roommate(billform.name2.data, float(billform.days_in_house2.data))

        return f"{roommate1.name} pays {roommate1.pays(the_bill, roommate2)}"


class BillForm(Form):
    amount = StringField("Bill Amount: ", default="100")
    period = StringField("Bill Period: ", default="December 2020")

    name1 = StringField("Name: ", default="John")
    days_in_house1 = StringField("Days in the house: ", default="20")

    name2 = StringField("Name: ", default="Marry")
    days_in_house2 = StringField("Days in the house: ", default="12")

    button = SubmitField("Calculate")


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/bill_form', view_func=BillFormPage.as_view('bill_form_page'))
app.add_url_rule('/results', view_func=ResultsPage.as_view('results'))

app.run(debug=True)
