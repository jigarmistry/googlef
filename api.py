from main import generate_api_response
from flask import Flask, render_template, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return "Google Finance Portfolio"


@app.route("/portfolio")
@app.route("/portfolio/<pid>")
def report(pid=2):
    return render_template('report.html', pid=pid)


@app.route("/api/<pid>")
def report_api(pid):
    json_data = generate_api_response(pid)
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(debug=True)
