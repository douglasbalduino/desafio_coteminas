import flask
import glob
import json


app = flask.Flask(__name__)
def get_data(path_name):
    file_name = glob.glob('data/'+path_name+'/*.json')[0]
    data = json.load(open(file_name))
    return data
@app.route('/')
def api():
    return 'API UP'

@app.route('/desvio_padrao/list', methods=['GET', 'POST'])
def get_desvio_padrao():
    data = get_data('desvio_padrao').get('data_list')
    return flask.jsonify(data)

@app.route('/media_rating/list', methods=['GET', 'POST'])
def get_media_rating():
    data = get_data('media_rating').get('data_list')
    return flask.jsonify(data)   

@app.route('/media_review/list', methods=['GET', 'POST'])
def get_media_review():
    data = get_data('media_review').get('data_list')
    return flask.jsonify(data)     

'''@app.route('/desvio_padrao/listByCategory/<category>', methods=['GET', 'POST'])
def get_list_by_category(category):    
    data = get_data('desvio_padrao').get('data_list')
    for i in data.get('data_list'):
        i.get(category)
    return flask.jsonify(data)'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


