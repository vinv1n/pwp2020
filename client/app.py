from flask import Flask


app = Flask(__name__, static_folder="static")


@app.route("/")
def client_index():
    return app.send_static_file("html/index.html")
