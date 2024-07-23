from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return open('web/index.html').read()

@app.route('/execute', methods=['POST'])
def execute():
    result = subprocess.run(['python3', 'scripts/current_rule.py'], capture_output=True, text=True)
    return result.stdout + result.stderr

if __name__ == '__main__':
    app.run(debug=True)
