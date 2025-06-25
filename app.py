from flask import Flask, request, jsonify, render_template
import requests, json, os

#Flask instansiation
app = Flask(__name__)

#When Homepage is opened. Render index.html
@app.route("/")
def home():
    return render_template("index.html")

#Receives POST request in JS backend and Directs it to Ollama
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("prompt", "")

    #Load memory
    insights = []
    if os.path.exists("memory.json"):
        with open("memory.json", "r") as f:
            insights = json.load(f).get("insights", [])

    memory_context = "\n".join(insights)
    
    #Add memory to prompt
    full_prompt = f"""Here are some things the user previously said:\n{memory_context}\n\nNow respond to: {user_input}"""

    res = requests.post("http://localhost:11434/api/generate", json={
        "model" : "llama3",
        "prompt": full_prompt,
        "stream" : False 

    })

    ai_response = res.json()["response"]

    #Extract insight from user input
    insight = extract_insight(user_input)
    memory_update = ""
    if insight:
        save_insight(insight)
        memory_update = f"✅ Memory updated: {insight}"
    
    return jsonify({
        "response" : ai_response,
        "memory" : memory_update
    })

#Simple Memory insight
def extract_insight(user_input):
    key_words = ["i prefer", "i like"]
    neg_words = ["i don't like", "i dislike"]
    lower_input = user_input.lower()
    for key in key_words:
        if lower_input.startswith(key):
            preference = lower_input.split(key, 1)[1].strip().rstrip(".")
            return f"User {key.split()[-1]}s {preference.split()[0]}"
    for key in neg_words:
        if lower_input.startswith(key):
            dislikes = lower_input.split(key, 1)[1].strip().rstrip(".")
            return f"User {key.split()[-1]}s {dislikes}"
    return None

def save_insight(insight):
    if not os.path.exists("memory.json"):
        with open("memory.json", "w") as f:
            json.dump({"insights": []}, f)

    with open("memory.json", "r+") as f:
        data = json.load(f)
        if insight not in data["insights"]:
            data["insights"].append(insight)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.flush()
            print("[Debug] Insight:", insight)
            print("[Debug] Saved insights:", data["insights"])
        
if __name__ == "__main__":
    app.run(debug = True)
