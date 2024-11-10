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

# 
tools = []
with open("goose_tools.json") as f:
    # t is a json containing an array of tools
    # each tool is a json object with a function
    t = json.load(f)
    tools = t["tools"]


# init openai chatgpt-4o-mini
@app.route("/init", methods=["POST"])
def init_chatgpt():
    data = request.get_json()
    system_message = data.get("prompt", "")
    user_message = data.get("input", "")
    # print(data, user_message)
    # TODO (for backend): populate with functions, see chatbot.py
    # tools = None
    res = chatbot.start_chat(system_message, user_message, tools)
    # can't JSON serialize this, so recreate it manually
    return jsonify_chatbot_msg(res)


# query chatgpt
@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    user_message = data.get("input", "")
    chat_history = data.get("history", [])
    # TODO (for backend): populate with functions, see chatbot.py
    # tools = None
    res = chatbot.continue_chat(user_message, chat_history, tools, False)
    return jsonify_chatbot_msg(res)


def jsonify_chatbot_msg(message):
    # print(message, "\n")
    # can't JSON serialize this, so recreate it manually
    response, history = message[0], message[1]
    # print(history, "\n")
    response = {
        "role": response.role,
        "content": response.content,
    }
    # replace ChatCompletionMessage with JSONifiable one
    history[-1] = response
    # print(response, "\n")
    # print(history, "\n")
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
