from flask import Flask, render_template, request, jsonify, Response
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


@app.route('/run/<string:query_filename>', methods=['POST', 'GET'])
def run(query_filename):
    # TODO: check the form has the right data
    # if it's a GET request, use the query string, otherwise use the form data
    if request.method == 'GET':
        query_params = request.args
    elif request.method == 'POST':
        query_params = request.form

    header, data = db.run_query(query_filename, query_params, data_format='list')
    return render_template('results.html',
                           query=query_filename,
                           query_list=db.get_queries(),
                           title=db.SETTINGS['website_title'],
                           header=header,
                           data=data)


@app.route('/api/<string:query_filename>.json')
def api_json(query_filename):
    query_params = request.args
    data = db.run_query(query_filename, query_params, data_format='dict')
    return jsonify(params=query_params, data=data)


@app.route('/api/<string:query_filename>.csv')
def api_csv(query_filename):
    query_params = request.args
    data = db.run_query(query_filename, query_params, data_format='csv')
    return Response(data, mimetype='text/csv')
