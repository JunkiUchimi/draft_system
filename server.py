from flask import Flask, jsonify, send_from_directory, Response, request
import subprocess
import json
import os
import logging

app = Flask(__name__)

def run_script(script_path):
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    return result.stdout


@app.route('/update_config', methods=['POST'])
def update_config():
    config_data = request.json
    try:
        with open('config/config.json', 'w') as config_file:
            json.dump(config_data, config_file, indent=4)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/current_output')
def get_current_output():
    output = run_script('scripts/current_rule.py')
    return Response(output, mimetype='text/plain')

@app.route('/enhanced_output')
def get_enhanced_output():
    output = run_script('scripts/enhanced_rule.py')
    return Response(output, mimetype='text/plain')

@app.route('/')
def serve_index():
    return send_from_directory('web', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
