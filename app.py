from flask import Flask, jsonify, abort, request

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return 'invalid database', 404

@app.route('/datas', methods=['GET'])
def get_databases():
    start = request.args.get('start')
    end = request.args.get('end')
    return str(start) + str(end)

@app.route('/datas/Input<int:database_id>', methods=['GET'])
def get_database(database_id):
    if database_id > 5 or database_id < 1:
        abort(404)
    return str(database_id)

if __name__ == '__main__':
    app.run(debug=True)