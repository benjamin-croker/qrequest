from flask import Flask, render_template, request
import database as db

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           query_list=db.get_queries(),
                           description=db.SETTINGS['website_description'],
                           title=db.SETTINGS['website_title'])


@app.route('/setup/<string:query_filename>')
def setup(query_filename):
    return render_template('setup_query.html',
                           query=query_filename,
                           query_list=db.get_queries(),
                           params_list=db.get_params(query_filename),
                           title=db.SETTINGS['website_title'])


@app.route('/run/<string:query_filename>', methods=['POST'])
def run(query_filename):
    # TODO: check the form has the right data
    header, data = db.run_query(query_filename, request.form)
    return render_template('results.html',
                           query=query_filename,
                           query_list=db.get_queries(),
                           title=db.SETTINGS['website_title'],
                           header=header,
                           data=data)
