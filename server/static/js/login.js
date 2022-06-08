const usernameInput = document.querySelector("#username")
const passwordInput = document.querySelector("#password")
const submitBtn = document.querySelector("#submitLogin")

const updateButtonDisabled = () => {
    submitBtn.disabled = usernameInput.value === "" || passwordInput.value === ""
}

usernameInput.addEventListener("input", updateButtonDisabled)
passwordInput.addEventListener("input", updateButtonDisabled)
window.addEventListener("load", updateButtonDisabled)
