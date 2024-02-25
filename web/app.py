from flask import Flask, render_template, jsonify

app = Flask(__name__)

#rest-api routes
@app.route("/messages/", methods=['GET'])
def messages():
    return jsonify()

@app.route("/messages/<word>", methods=['GET'])
def by_message_text(word):
    return jsonify()


#routes
@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def bad_request(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')