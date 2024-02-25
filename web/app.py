from flask import Flask, render_template, jsonify


app = Flask(__name__)

#rest-api routes
@app.route("/messages/")
def messages():
    pass

@app.route("/messages/<word>")
def by_message_text():
    pass


#routes
@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)