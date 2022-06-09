const search = document.querySelector(".search__queryInput")
const results = document.querySelector(".search__queryResult__list")
const chats = document.querySelector(".leftPanel__chatContainer")
const chatsEmpty = document.querySelector(".leftPanel__empty")
const messages = document.querySelector(".messages__container")
const form = document.querySelector(".newMessageInput")
const fileInput = document.querySelector(".newMessageInput__fileInput")
const fileInputImg = document.querySelector(".newMessageInput__fileInputLabel__img")
const input = document.querySelector(".newMessageInput__input")
const submit = document.querySelector(".newMessageInput__btn")
const username = document.querySelector(".rightPanel__username")

const socket = io()

socket.on("connect", () => {
    socket.emit("connected")
})

socket.on("new message from server", message => {
    renderNewMessage(message)
    messages.scrollTop = messages.scrollHeight
    if (message.sender !== username.innerText)
        socket.emit("read message from client")
})

socket.on("read message from server", () => {
    updateReadAvatar()
})

socket.on("new chat", data => {
    renderNewChatItem(data.chat_id, data.recipient)
})

form?.addEventListener("submit", e => {
    e.preventDefault()
    if (fileInput.files || input.value !== "")
        postMessage()
    form.reset()
    fileInputImg.src = "/static/img/image_icon.png"
})

const postMessage = () => {
    const path = window.location.pathname
    const slashIndex = path.lastIndexOf("/")
    const chatId = path.substring(slashIndex + 1)
    const formData = new FormData(form)
    fetch(`/message/${chatId}`, {
        method: "POST",
        body: formData
    });
}

const updateNewMessageSubmitDisabled = () => {
    if (submit)
        submit.disabled = input.value === "" && fileInput.files.length === 0
}

input?.addEventListener("input", () => {
    fileInput.value = null
    fileInputImg.src = "/static/img/image_icon.png"
    updateNewMessageSubmitDisabled()
})

fileInput?.addEventListener("change", () => {
    input.value = ""
    const r = new FileReader()
    r.readAsDataURL(fileInput.files[0])
    r.onloadend = e => {
        fileInputImg.src = e.target.result
    }
    updateNewMessageSubmitDisabled()
})

window.addEventListener("load", () => {
    messages.scrollTop = messages.scrollHeight;
    updateNewMessageSubmitDisabled()
})

search.addEventListener("input", async () => {
    results.innerHTML = ""
    if (search.value !== "") {
        const res = await fetch(`/user/${search.value}`, {
            method: "GET"
        })
        const usersList = await res.json()
        renderUserQueryResults(usersList)
    }
})
