from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired


class ENSearchForm(FlaskForm) :

    """ Custom search form with data validation on / and /en """

    jobTitle = StringField('Job title', validators=[DataRequired()], default="Job Title")
    location = StringField('Location', validators=[DataRequired()], default="Location")
    country = SelectField(u'Country', choices=[('FR', 'France'), ('UK', 'United Kingdom'), ('US', 'United States')], validators=[DataRequired()])
    age = IntegerRangeField("Age", validators=[DataRequired()], default = 30)
    submit = SubmitField('Search')

class FRSearchForm(FlaskForm) :

    """ Custom search form with data validation on /fr """

    jobTitle = StringField('Job title', validators=[DataRequired()], default="Intitulé du poste")
    location = StringField('Location', validators=[DataRequired()], default="Localisation")
    country = SelectField(u'Country', choices=[('FR', 'France'), ('UK', 'Royaume-Uni'), ('US', 'États-Unis')], validators=[DataRequired()])
    age = IntegerRangeField("Age", validators=[DataRequired()], default = 30)
    submit = SubmitField('Rechercher')

import logging
import logging.handlers
import json

from flask import Flask, render_template, abort, request, send_from_directory
from jinja2 import TemplateNotFound

from jobsaggregator import JobsAggregator

class Server:

    """Flask server class"""

    __instance = None

    @staticmethod
    def getInstance():

        """ Static access method """

        if Server.__instance == None:

            Server()

        return Server.__instance

    def __init__(self):

        if Server.__instance != None:

            raise Exception("This class is a singleton!")

        else:

            Server.__instance = self

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler('logs/' + __name__ + '.log',
                                                  maxBytes=10000000, backupCount=100)
        fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
        self.logger.addHandler(fh)
        self.logger.info("Server created")

        self.app = Flask(__name__)
        self.app.add_url_rule("/", "index", self.indexEN, methods=['GET'])
        self.app.add_url_rule("/fr", "index_fr", self.indexFR, methods=['GET'])
        self.app.add_url_rule("/en", "index_en", self.indexEN, methods=['GET'])
        self.app.add_url_rule("/search", "search", self.search, methods=['POST'])
        self.app.add_url_rule("/download", "download", self.downloadCSV, methods=["POST"])

        self.app.secret_key = 'p|\xbf\xdbi\xf0\xf3\xa1mDb\x1a\x04\xc8\x07]'

        self.jobsAggreg = JobsAggregator()


    def getApp(self):

        """Function used in production server only"""

        return self.app


    def launchServer(self):

        """Function used in development server only"""

        self.logger.info("Launching server")
        self.app.run(debug=True, threaded=True)

    def indexFR(self):

        """This method is called when a request is sent to /fr"""

        try:

            form = FRSearchForm()

            if form.validate_on_submit():

                return render_template("index_fr.html")

            return render_template("index_fr.html", form=form)

        except TemplateNotFound:

            abort(404)

    def indexEN(self):

        """This method is called when a request is sent to the
        homepage OR to /en"""

        try:

            form = ENSearchForm()

            if form.validate_on_submit():



                return render_template("index_en.html")

            return render_template("index_en.html", form=form)

        except TemplateNotFound:

            abort(404)

    def search(self):

        """This method is called when a request is sent to /search, i.e.
        when the user submits a search form. This function returns the search
        results in JSON"""

        #search object for testing only, to be deleted
        search = {"job": request.form["jobTitle"],
          "location": request.form["location"],
          "country": request.form["country"]}

        age = request.form["age"]

        searchResults = self.jobsAggreg.findJob(search, request.form["uniqueID"], int(age))

        return json.dumps(searchResults);

    def downloadCSV(self):

        """This method is called when a request is sent to /download.
        This happens when an user wants to download a list of results in CSV.
        The request comes with an unique identifying number that allows to know
        what specific file should be returned to the user."""

        filename = str(request.form["uniqueID"]) + ".csv"

        return send_from_directory("csv", filename, as_attachment=True)
