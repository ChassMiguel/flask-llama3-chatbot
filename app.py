from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("prompt", "")

    res = requests.post("http://localhost:11434/api/generate", json={
        "model" : "llama3",
        "prompt": user_input,
        "stream" : False 

    })

    return jsonify(res.json())

if __name__ == "__main__":
    app.run(debug = True)
