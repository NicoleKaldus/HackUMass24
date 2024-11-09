from flask import Flask, request, jsonify, send_from_directory
import random

app = Flask(__name__)
#CORS(app)

#svelte path
@app.route("/")
def base():
    return send_from_directory("client/public", "index.html")

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


#test function, returns a random number
@app.route("/rand")
def hello():
    return str(random.randint(1, 100))

if __name__ == "__main__":
    app.run(debug=True)

