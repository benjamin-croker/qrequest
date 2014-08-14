from flask import Flask, render_template, request, jsonify, Response
import database as db

app = Flask(__name__)

def query_string_from_post(request_form):
    """ creates a query string from POST data
    """
    return '?'+'&'.join(["{}={}".format(k, request_form[k]) for k in request_form])


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
        query_params = request.args.to_dict()
    elif request.method == 'POST':
        query_params = request.form.to_dict()

    header, data = db.run_query(query_filename, query_params, data_format='list')
    # api links to download data in json and csv formats
    json_link = '/api/{}.json{}'.format(query_filename,
                                        query_string_from_post(query_params))
    csv_link = '/api/{}.csv{}'.format(query_filename,
                                        query_string_from_post(query_params))
    return render_template('results.html',
                           query=query_filename,
                           query_list=db.get_queries(),
                           title=db.SETTINGS['website_title'],
                           header=header,
                           data=data,
                           json_link=json_link,
                           csv_link=csv_link)


@app.route('/api/<string:query_filename>.json')
def api_json(query_filename):
    query_params = request.args.to_dict()
    data = db.run_query(query_filename, query_params, data_format='dict')
    return jsonify(params=query_params, data=data)


@app.route('/api/<string:query_filename>.csv')
def api_csv(query_filename):
    query_params = request.args.to_dict()
    data = db.run_query(query_filename, query_params, data_format='csv')
    return Response(data, mimetype='text/csv')
