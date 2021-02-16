const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/")
let messages = []

chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data)
    let message = data.message
    console.log("message from server: " + event.data)
    message.wasMe = false
    messages.push(message)
    appendMessage(message)
}

chatSocket.onclose = function (e) {
    console.error("Socket closed by server")
}

document.addEventListener("DOMContentLoaded", function (event) {
    document.querySelector("#chat-message-input").focus()
    document.querySelector("#chat-message-input").onkeypress = function (event) {
        if (event.keyCode === 13) {
            document.querySelector("#chat-message-submit").click()
        }
    }

    document.querySelector("#chat-message-submit").onclick = function (event) {
        const input = document.querySelector("#chat-message-input").value
        chatSocket.send(JSON.stringify({ "message": input }))
        let message = { "text": input, "author": "Me", "wasMe": true, "timestamp": Date.now() }
        console.log(JSON.stringify(message))
        //messages.push(JSON.stringify(message))
        //appendMessage(message)
        document.querySelector("#chat-message-input").value = ""
    }
})

function appendMessage(message) {
    let messageContainer = document.createElement("div")
    messageContainer.classList.add("message-container")
    if (message.wasMe) {
        messageContainer.classList.add("myMessage")
    } else {
        messageContainer.classList.add("otherMessage")
    }

    let authorElement = document.createElement("div")
    authorElement.classList.add("author")
    authorElement.textContent = message.author
    messageContainer.appendChild(authorElement)

    let textElement = document.createElement("p")
    textElement.classList.add("text")
    textElement.textContent = message.text
    messageContainer.appendChild(textElement)

    let dateElement = document.createElement("div")
    dateElement.classList.add("timestamp")
    dateElement.textContent = message.timestamp
    messageContainer.appendChild(dateElement)

    document.querySelector("#chat-log-container").appendChild(messageContainer)
}