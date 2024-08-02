from flask import Flask, jsonify, send_from_directory, Response
import subprocess
import json
import os
import logging

app = Flask(__name__)

def run_script(script_path):
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    return result.stdout

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
