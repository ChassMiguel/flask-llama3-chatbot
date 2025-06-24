async function send() {
    const inputBox = document.getElementById("input");
    const chatBox = document.getElementById("chat");
    const prompt = inputBox.value.trim();
    
    if(!prompt) return;

    //Display user message
    chatBox.innerHTML += `<p class="user"><b>You:</b> ${prompt}</p>`;
    inputBox.value = "";

    //Send back user prompt to python Flask
    try {
        const res = await fetch("/chat", {
            method : "Post",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({prompt})
        });

        //Convert response to JSON
        const data = await res.json();

        //Display chatbot's reply
        chatBox.innerHTML += `<p class="bot"><b>Bot:</b> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        chatBox.innerHTML += `<p class="bot"><b>Bot:</b> Could not connect to server.</b>`;
    }
}