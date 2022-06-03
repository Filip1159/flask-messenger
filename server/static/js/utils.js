console.log(1)
const socket = io()
socket.on("connect", () => {
    console.log("on connect")
    socket.emit("my event", {data: "Im connected!"})
})
socket.on("Post messgae", (data) => {
    console.log("got message " + data)
    // TODO when data will be a message, render it
})
console.log(2)

const btn = document.querySelector(".newMessageInput__btn")

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
    // socket.emit("new message", {
    //     chatId,
    //     time: nowToSql(),
    //     content: input.value
    // })
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
