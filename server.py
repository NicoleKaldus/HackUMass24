from flask import Flask, request, jsonify, send_from_directory
import chatbot
import json

app = Flask(__name__)
# CORS(app)


# svelte path
@app.route("/")
def base():
    return send_from_directory("client/public", "index.html")


# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory("client/public", path)


sam_tools = []
goose_tools = []
with open("sam_tools.json") as f:
    # t is a json containing an array of tools
    # each tool is a json object with a function
    t = json.load(f)
    sam_tools = t["tools"]
with open("goose_tools.json") as f:
    # t is a json containing an array of tools
    # each tool is a json object with a function
    t = json.load(f)
    goose_tools = t["tools"]


# init openai chatgpt-4o-mini
@app.route("/init", methods=["POST"])
def init_chatgpt():
    data = request.get_json()
    system_message = data.get("prompt", "")
    user_message = data.get("input", "")
    is_sam = data.get("isSam", False)
    tools = sam_tools if is_sam else goose_tools
    res = chatbot.start_chat(system_message, user_message, tools)
    return jsonify_chatbot_msg(res)


# query chatgpt
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_message = data.get("input", "")
    chat_history = data.get("history", [])
    is_sam = data.get("isSam", False)
    tools = sam_tools if is_sam else goose_tools
    res = chatbot.continue_chat(user_message, chat_history, tools, False)
    return jsonify_chatbot_msg(res)


def jsonify_chatbot_msg(message):
    # can't JSON serialize ChatCompletionMessage, so recreate it manually
    response, history = message[0], message[1]
    response = {
        "role": response.role,
        "content": response.content,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
