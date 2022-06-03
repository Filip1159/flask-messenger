const loginInput = document.querySelector("#login_input")
const passwordInput = document.querySelector("#password_input")

import ChatAPI from "./ChatAPI";

const onLogin = async () => {
    const username = loginInput.value
    const password = passwordInput.value
    const isSuccess = await ChatAPI.signIn(username, password)

}