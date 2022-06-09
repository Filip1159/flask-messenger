const submitBtn = document.querySelector("#buttonSubmit")
const username = document.querySelector("#username")
const name = document.querySelector("#name")
const surname = document.querySelector("#surname")
const password = document.querySelector("#password")
const repeatPassword = document.querySelector("#repeat_password")
const info = document.querySelector(".signupPage__error")

const onlyLettersRegex = /^[a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]+$/
const lettersAndDigitsRegex = /^[0-9a-zA-ZąćęłńóśźżĄĘŁŃÓŚŹŻ]+$/
const firstUppercaseRegex = /^[A-Z]/
let usernameOldValue = "", nameOldValue = "", surnameOldValue = "", passwordOldValue = "", repeatPasswordOldValue = ""
let usernameValid = false, nameValid = false, surnameValid = false, passwordValid = false, repeatPasswordValid = false

const updateUsernameValid = () => {
    usernameValid = username.value.length >= 3 && lettersAndDigitsRegex.test(username.value)
    updateButtonDisabled()
}

const updateNameValid = () => {
    nameValid = onlyLettersRegex.test(name.value) && firstUppercaseRegex.test(name.value)
    updateButtonDisabled()
}

const updateSurnameValid = () => {
    surnameValid = onlyLettersRegex.test(surname.value) && firstUppercaseRegex.test(surname.value)
    updateButtonDisabled()
}

const updatePasswordValid = () => {
    passwordValid = password.value.length >= 8 && password.value.length <= 20 && /\d/.test(password.value) && !/\s/.test(password.value)
    updateRepeatPasswordValid()
    updateButtonDisabled()
}

const updateRepeatPasswordValid = () => {
    repeatPasswordValid = repeatPassword.value !== "" && password.value === repeatPassword.value
    updateButtonDisabled()
}

const updateButtonDisabled = () => {
    submitBtn.disabled = !(usernameValid && nameValid && surnameValid && passwordValid && repeatPasswordValid)
}

const addMultipleListeners = (element, events, listener) => {
    for (let e of events)
        element.addEventListener(e, listener)
}

const updateInfo = condition => {
    if (condition) info.style["color"] = "green"
    else info.style["color"] = "red"
}

document.addEventListener("keyup", () => {
    if (username.value !== usernameOldValue) {
        usernameOldValue = username.value
        updateUsernameValid()
        updateInfo(usernameValid)
    } else if (name.value !== nameOldValue) {
        nameOldValue = name.value
        updateNameValid()
        updateInfo(nameValid)
    } else if (surname.value !== surnameOldValue) {
        surnameOldValue = surname.value
        updateSurnameValid()
        updateInfo(surnameValid)
    } else if (password.value !== passwordOldValue) {
        passwordOldValue = password.value
        updatePasswordValid()
        updateInfo(repeatPassword)
        updateInfo(passwordValid)
    } else if (repeatPassword.value !== repeatPasswordOldValue) {
        repeatPasswordOldValue = repeatPassword.value
        updateRepeatPasswordValid()
        updateInfo(repeatPasswordValid)
    }
})

addMultipleListeners(username, ["mouseover", "focusin"], () => {
    info.innerText = "At least 3 characters long, may contain letters and digits"
    updateInfo(usernameValid)
})

addMultipleListeners(name, ["mouseover", "focusin"], () => {
    info.innerText = "Not blank, contains only letters, starts with uppercase"
    updateInfo(nameValid)
})

addMultipleListeners(surname, ["mouseover", "focusin"], () => {
    info.innerText = "Only letters, starts with upper case"
    updateInfo(surnameValid)
})

addMultipleListeners(password, ["mouseover", "focusin"], () => {
    info.innerText = "8 - 20 characters, contains only letters and at least one digit";
    updateInfo(passwordValid)
})

addMultipleListeners(repeatPassword, ["mouseover", "focusin"], () => {
    info.innerText = "Same as above";
    updateInfo(repeatPasswordValid)
})

document.querySelectorAll("input, label").forEach(element => {
    addMultipleListeners(element, ["mouseleave", "focusout"], () => {
        info.innerText = " ";
    })
})

window.addEventListener("load", updateButtonDisabled)