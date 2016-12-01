from main import generate_api_response
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/<pid>")
def report(pid=1):
    return render_template('report.html',pid=pid)

@app.route("/api")
def report_api():
    json_data = generate_api_response()
    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug=True)