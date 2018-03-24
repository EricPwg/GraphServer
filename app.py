import pony.orm as pny
from flask import Flask, jsonify, abort, request
from dateutil import parser

from models import Input1, Input2, Input3, Input4, Input5

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return 'invalid database', 404

@app.route('/datas', methods=['GET'])
def get_databases():
    res = {}
    for i in range(1, 6):
        tablename = 'Input' + str(i)
        start = parser.parse(request.args.get('start'))
        end = parser.parse(request.args.get('end'))
        with pny.db_session:
            k = pny.select((p.timestamp, p.value) for p in globals()[tablename] \
                            if p.timestamp >= start and p.timestamp <= end)[:]
        res.update({tablename: [(str(x[0]), x[1]) for x in k]})

    return jsonify(res)

@app.route('/datas/Input<int:database_id>', methods=['GET'])
def get_database(database_id):
    if database_id > 5 or database_id < 1:
        abort(404)
    tablename = 'Input' + str(database_id)
    start = parser.parse(request.args.get('start'))
    end = parser.parse(request.args.get('end'))
    with pny.db_session:
        k = pny.select((p.timestamp, p.value) for p in globals()[tablename] \
                        if p.timestamp >= start and p.timestamp <= end)[:]
    res = {tablename: [(str(x[0]), x[1]) for x in k]}

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)