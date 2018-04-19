import os
import pony.orm as pny

from dateutil import parser

from flask import (Flask, jsonify, render_template,
                   request, send_from_directory)

import models

from config import QUERY_LIMIT

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return 'invalid database', 404


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')


@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html')


@app.route('/datas', methods=['GET'])
def get_databases():
    res = {}

    start = request.args.get('start')
    end = request.args.get('end')
    limit = int(request.args.get('limit', QUERY_LIMIT))

    if start and end:
        start = parser.parse(start)
        end = parser.parse(end)

    for tablename in models.database.entities:
        table = models.database.entities.get(tablename)
        with pny.db_session:
            if start and end:
                query = table.select(lambda row: row.timestamp >= start and row.timestamp <= end)
            else:
                query = table.select()

            query = query.order_by(pny.desc(table.timestamp)).limit(limit)

        res.update({tablename: [(str(record.timestamp), record.value) for record in query]})

    return jsonify(res)


@app.route('/datas/<string:tablename>', methods=['GET'])
def get_database(tablename):
    if not hasattr(models, tablename):
        return "table not find"
    table = getattr(models, tablename)

    start = request.args.get('start')
    end = request.args.get('end')
    limit = int(request.args.get('limit', QUERY_LIMIT))

    if start and end:
        start = parser.parse(start)
        end = parser.parse(end)

    with pny.db_session:
        if start and end:
            query = table.select(lambda row: row.timestamp >= start and row.timestamp <= end)
        else:
            query = table.select()

        query = query.order_by(pny.desc(table.timestamp)).limit(limit)

    res = {tablename: [(str(record.timestamp), record.value) for record in query]}

    return jsonify(res)


def data_server():
    app.run(host='0.0.0.0', debug=True, threaded=True)

if __name__ == '__main__':
    app.run('0', debug=True, threaded=True)
