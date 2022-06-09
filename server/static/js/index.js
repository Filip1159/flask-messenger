const btn = document.querySelector(".newMessageInput__btn")
const username_span = document.querySelector(".rightPanel__username")
const messages_panel = document.querySelector(".messages__container")
const messages_container = document.querySelector(".messages__container")
const input = document.querySelector(".newMessageInput__input")
const searchInput = document.querySelector(".search__queryInput")
const searchResultList = document.querySelector(".search__queryResult__list")
const chatContainer = document.querySelector(".leftPanel__chatContainer")
const newMessageFileInput = document.querySelector(".newMessageInput__fileInput")
const newMessageForm = document.querySelector(".newMessageInput")

const socket = io()
socket.on("connect", () => {
    console.log("on connect")
    socket.emit("connected")
})

socket.on("Post message", message => {
    console.log(message)
    const new_msg = document.createElement("div")
    new_msg.classList.add("messages__singleMessage", `messages__singleMessage--${message.sender === username_span.innerText ? "myMsg" : "receivedMsg"}`)
    if (message.type === "text") {
        new_msg.innerText = message.content
    } else {
        new_msg.classList.add("messages__singleMessage--img")
        const message_img = document.createElement("img");
        message_img.classList.add("messages__singleMessage__img")
        message_img.src = `/static/img/messages/${message.content}`
        new_msg.appendChild(message_img)
    }
    const new_msg_tooltip = document.createElement("div")
    new_msg_tooltip.innerText = message.time
    new_msg_tooltip.classList.add("messages__singleMessage__tooltip")
    new_msg.appendChild(new_msg_tooltip)
    messages_panel.appendChild(new_msg)
    const messagesContainerEmptySpan = document.querySelector(".messages__container__empty");
    if (messagesContainerEmptySpan) {
        messages_container.removeChild(messagesContainerEmptySpan)
    }
    messages_container.scrollTop = messages_container.scrollHeight;
    if (message.sender !== username_span.innerText)
        socket.emit("Read message signal")
})

socket.on("Read message", () => {
    const old_read_avatar = document.querySelector(".seenAvatar")
    const avatar_img_src = old_read_avatar.src
    old_read_avatar.remove()
    const new_read_avatar = document.createElement("img")
    new_read_avatar.classList.add("seenAvatar")
    new_read_avatar.src = avatar_img_src
    new_read_avatar.alt = "Seen avatar"
    messages_container.appendChild(new_read_avatar)
})

newMessageForm.addEventListener("submit", e => {
    e.preventDefault()
    if (newMessageFileInput.files || input.value !== "")
        postMessage()
    newMessageForm.reset()
})

const postMessage = () => {
    const path = window.location.pathname
    const slashIndex = path.lastIndexOf("/")
    const chatId = path.substring(slashIndex + 1)
    if (newMessageFileInput.files) {
        const data = new FormData(newMessageForm)
        fetch(`/message/${chatId}`, {
            method: "POST",
            body: data
        });
    }
    else if (input.value !== "") {
        fetch(`/message/${chatId}`, {
            method: "POST",
            body: JSON.stringify({
                content: input.value
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        input.value = ""
    }
}

window.onload = () => {
    messages_container.scrollTop = messages_container.scrollHeight;
}

const renderNewChatItem = (chatId, recipient) => {
    const a = document.createElement("a")
    a.href = `/chats/${chatId}`
    const chatItem = document.createElement("div")
    chatItem.classList.add("chatItem")
    a.appendChild(chatItem)
    const img = document.createElement("img")
    img.src = `/static/img/avatars/${recipient.avatar_img}`
    img.alt = "User avatar"
    chatItem.appendChild(img)
    const chatData = document.createElement("div")
    chatData.classList.add("chatItem__chatData")
    chatItem.appendChild(chatData)
    const nameSurnameSpan = document.createElement("span")
    nameSurnameSpan.classList.add("chatItem__chatData__nameSurname")
    nameSurnameSpan.innerHTML = `${recipient.name} ${recipient.surname}`
    chatData.appendChild(nameSurnameSpan)
    const lastMessageSpan = document.createElement("span")
    lastMessageSpan.classList.add("chatItem__chatData__lastMessage")
    lastMessageSpan.innerHTML = "<<New chat>>"
    chatData.appendChild(lastMessageSpan)
    chatContainer.appendChild(a)
}

searchInput.addEventListener("input", async () => {
    searchResultList.innerHTML = ""
    if (searchInput.value !== "") {
        const res = await fetch(`/user/${searchInput.value}`, {
            method: "GET"
        })
        const data = await res.json()
        for (let user of data) {
            const userLi = document.createElement("li")
            userLi.innerText = `${user.name} ${user.surname} (${user.username})`
            userLi.addEventListener("click", async () => {
                const res = await fetch(`/chat/${user.id}`, {
                    method: "POST"
                })
                const data = await res.json()
                const chatContainerEmptySpan = document.querySelector(".leftPanel__empty");
                if (chatContainerEmptySpan) {
                    chatContainer.removeChild(chatContainerEmptySpan)
                }
                renderNewChatItem(data.id, user)
            })
            searchResultList.appendChild(userLi)
        }
    }
})