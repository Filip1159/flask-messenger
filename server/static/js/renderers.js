const renderNewChatItem = (chatId, recipient) => {
    const a = document.createElement("a")
    a.href = `/chats/${chatId}`
    const chatItem = document.createElement("div")
    chatItem.classList.add("chatItem")
    a.appendChild(chatItem)
    addImageToChatItem(chatItem, recipient.avatar_img)
    addChatDataToChatItem(chatItem, recipient)
    chats.appendChild(a)
}

const addImageToChatItem = (chatItem, avatarImg) => {
    const img = document.createElement("img")
    img.classList.add("chatItem__img")
    img.src = `/static/img/avatars/${avatarImg}`
    img.alt = "User avatar"
    chatItem.appendChild(img)
}

const addChatDataToChatItem = (chatItem, recipient) => {
    const chatData = document.createElement("div")
    chatData.classList.add("chatItem__chatData")
    addNameSurnameSpanToChatData(chatData, recipient)
    addLastMessageSpanToChatData(chatData)
    chatItem.appendChild(chatData)
}

const addNameSurnameSpanToChatData = (chatData, recipient) => {
    const nameSurnameSpan = document.createElement("span")
    nameSurnameSpan.classList.add("chatItem__chatData__nameSurname")
    nameSurnameSpan.innerHTML = `${recipient.name} ${recipient.surname}`
    chatData.appendChild(nameSurnameSpan)
}

const addLastMessageSpanToChatData = chatData => {
    const lastMessageSpan = document.createElement("span")
    lastMessageSpan.classList.add("chatItem__chatData__lastMessage")
    lastMessageSpan.innerText = "Empty chat"
    chatData.appendChild(lastMessageSpan)
}

const renderUserQueryResults = usersList => {
    for (let user of usersList)
        renderUserQueryItem(user)
}

const renderUserQueryItem = user => {
    const userLi = document.createElement("li")
        userLi.innerText = `${user.name} ${user.surname} (${user.username})`
        userLi.addEventListener("click", async () => {
            const res = await fetch(`/chat/${user.id}`, {
                method: "POST"
            })
            const chat = await res.json()
            if (chatsEmpty)
                chats.removeChild(chatsEmpty)
            renderNewChatItem(chat.id, user)
        })
        results.appendChild(userLi)
}

const updateReadAvatar = () => {
    const oldReadAvatar = document.querySelector(".seenAvatar")
    const avatarImgSrc = oldReadAvatar.src
    oldReadAvatar.remove()
    const newReadAvatar = document.createElement("img")
    newReadAvatar.classList.add("seenAvatar")
    newReadAvatar.src = avatarImgSrc
    newReadAvatar.alt = "Seen avatar"
    messages.appendChild(newReadAvatar)
}

const renderNewMessage = message => {
    const messageDiv = document.createElement("div")
    messageDiv.classList.add("messages__singleMessage", `messages__singleMessage--${message.sender === username.innerText ? "myMsg" : "receivedMsg"}`)
    if (message.type === "text")
        messageDiv.innerText = message.content
    else
        renderNewMessageAsImage(messageDiv, message.content)
    renderMessageTooltip(messageDiv, message.time)
    messages.appendChild(messageDiv)
    const messagesContainerEmptySpan = document.querySelector(".messages__container__empty");
    if (messagesContainerEmptySpan)
        messages.removeChild(messagesContainerEmptySpan)
}

const renderMessageTooltip = (messageDiv, messageTime) => {
    const messageDivTooltip = document.createElement("div")
    messageDivTooltip.innerText = messageTime
    messageDivTooltip.classList.add("messages__singleMessage__tooltip")
    messageDiv.appendChild(messageDivTooltip)
}

const renderNewMessageAsImage = (messageDiv, imageName) => {
    messageDiv.classList.add("messages__singleMessage--img")
    const messageDivImg = document.createElement("img");
    messageDivImg.classList.add("messages__singleMessage__img")
    messageDivImg.src = `/static/img/messages/${imageName}`
    messageDiv.appendChild(messageDivImg)
}
