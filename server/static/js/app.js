const searchInput = document.querySelector(".search__queryInput")
const searchResultList = document.querySelector(".search__queryResult__list")
const chatContainer = document.querySelector(".leftPanel__chatContainer")
const chatContainerEmptySpan = document.querySelector(".leftPanel__empty")
const messagesContainer = document.querySelector(".messages__container")
const newMessageForm = document.querySelector(".newMessageInput")
const newMessageFileInput = document.querySelector(".newMessageInput__fileInput")
const newMessageInputFileInputImg = document.querySelector(".newMessageInput__fileInputLabel__img")
const newMessageInput = document.querySelector(".newMessageInput__input")
const newMessageSubmit = document.querySelector(".newMessageInput__btn")
const rightPanelUsername = document.querySelector(".rightPanel__username")

const socket = io()

socket.on("connect", () => {
    socket.emit("connected")
})

socket.on("new message from server", message => {
    renderNewMessage(message)
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    if (message.sender !== rightPanelUsername.innerText)
        socket.emit("read message from client")
})

socket.on("read message from server", () => {
    updateReadAvatar()
})

newMessageForm.addEventListener("submit", e => {
    e.preventDefault()
    if (newMessageFileInput.files || newMessageInput.value !== "")
        postMessage()
    newMessageForm.reset()
    newMessageInputFileInputImg.src = "/static/img/image_icon.png"
})

const postMessage = () => {
    const path = window.location.pathname
    const slashIndex = path.lastIndexOf("/")
    const chatId = path.substring(slashIndex + 1)
    const formData = new FormData(newMessageForm)
    fetch(`/message/${chatId}`, {
        method: "POST",
        body: formData
    });
}

const updateNewMessageSubmitDisabled = () => {
    newMessageSubmit.disabled = newMessageInput.value === "" && newMessageFileInput.files.length === 0
}

newMessageInput.addEventListener("input", () => {
    newMessageFileInput.value = null
    newMessageInputFileInputImg.src = "/static/img/image_icon.png"
    updateNewMessageSubmitDisabled()
})

newMessageFileInput.addEventListener("change", () => {
    newMessageInput.value = ""
    const fileReader = new FileReader()
    fileReader.readAsDataURL(newMessageFileInput.files[0])
    fileReader.onloadend = e => {
        newMessageInputFileInputImg.src = e.target.result
    }
    updateNewMessageSubmitDisabled()
})

window.addEventListener("load", () => {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    updateNewMessageSubmitDisabled()
})

searchInput.addEventListener("input", async () => {
    searchResultList.innerHTML = ""
    if (searchInput.value !== "") {
        const res = await fetch(`/user/${searchInput.value}`, {
            method: "GET"
        })
        const usersList = await res.json()
        renderUserQueryResults(usersList)
    }
})
