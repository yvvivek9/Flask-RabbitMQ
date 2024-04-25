from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/consumer_one', methods=['GET'])
def get_consumer_one():
    return jsonify({'consumer': 'Consumer One'}), 200

@app.route('/consumer_two', methods=['GET'])
def get_consumer_two():
    return jsonify({'consumer': 'Consumer Two'}), 200

@app.route('/consumer_three', methods=['GET'])
def get_consumer_three():
    return jsonify({'consumer': 'Consumer Three'}), 200

@app.route('/consumer_four', methods=['GET'])
def get_consumer_four():
    return jsonify({'consumer': 'Consumer Four'}), 200

@app.route('/producer', methods=['GET'])
def get_producer():
    return jsonify({'producer': 'Producer'}), 200

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
