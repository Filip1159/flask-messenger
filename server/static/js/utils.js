const btn = document.querySelector(".newMessageInput__btn")
const username_span = document.querySelector(".rightPanel__username")
const messages_panel = document.querySelector(".messages__container")
const messages_container = document.querySelector(".messages__container")

const socket = io()
socket.on("connect", () => {
    console.log("on connect")
    socket.emit("my event", {data: "Im connected!"})
})
socket.on("Post message", (message) => {
    console.log("got message")
    console.log(message)
    const new_msg = document.createElement("div")
    new_msg.innerText = message.content
    new_msg.classList.add("messages__singleMessage", `messages__singleMessage--${message.sender === username_span.innerText ? "myMsg" : "receivedMsg"}`)
    const new_msg_tooltip = document.createElement("div")
    new_msg_tooltip.innerText = message.time
    new_msg_tooltip.classList.add("messages__singleMessage__tooltip")
    new_msg.appendChild(new_msg_tooltip)
    messages_panel.appendChild(new_msg)
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

const nowToSql = () => {
    const d = new Date();
    let yr = d.getFullYear(), mon = d.getMonth()+1, day = d.getDate(), h = d.getHours(), m = d.getMinutes(), s = d.getSeconds();
    if (mon < 10) mon = "0" + mon;
    if (day < 10) day = "0" + day;
    if (h < 10) h = "0" + h;
    if (m < 10) m = "0" + m;
    if (s < 10) s = "0" + s;
    return `${yr}-${mon}-${day}T${h}:${m}:${s}`;
}

btn.addEventListener("click", () => {
    const input = document.querySelector(".newMessageInput__input")
    console.log("CLICK!")
    const path = window.location.pathname
    const slashIndex = path.lastIndexOf("/")
    const chatId = path.substring(slashIndex+1)
    console.log(chatId)
    fetch("/message", {
        method: "POST",
        body: JSON.stringify({
            chatId,
            time: nowToSql(),
            content: input.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
})

window.onload = () => {
    console.log("scroll")
    messages_container.scrollTop = messages_container.scrollHeight;
}