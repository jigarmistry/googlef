from flask import Flask, render_template, jsonify
app = Flask(__name__)

@app.route("/")
def report():
    return render_template('report.html')

@app.route("/api")
def report_api():
    return jsonify({"name":"valuedd"})    

if __name__ == "__main__":
    app.run(debug=True)