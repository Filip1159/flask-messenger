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
    usernameValid = username.value.length >= 3 && lettersAndDigitsRegex.test(username.value);
    updateButtonDisabled();
}

const updateNameValid = () => {
    nameValid = onlyLettersRegex.test(name.value) && firstUppercaseRegex.test(name.value);
    updateButtonDisabled();
}

const updateSurnameValid = () => {
    surnameValid = onlyLettersRegex.test(surname.value) && firstUppercaseRegex.test(surname.value);
    updateButtonDisabled();
}

const updatePasswordValid = () => {
    passwordValid = password.value.length >= 8 && password.value.length <= 20 && /\d/.test(password.value) && !/\s/.test(password.value);
    updateButtonDisabled();
}

const updateRepeatPasswordValid = () => {
    repeatPasswordValid = repeatPassword.value !== "" && password.value === repeatPassword.value;
    updateButtonDisabled();
}

const updateButtonDisabled = () => {
    submitBtn.disabled = !(usernameValid && nameValid && surnameValid && passwordOldValue && repeatPasswordValid);
}

const addMultipleListeners = (element, events, listener) => {
    for (let e of events) {
        element.addEventListener(e, listener);
    }
}

document.addEventListener("keyup", () => {
    if (username.value !== usernameOldValue) {
        usernameOldValue = username.value;
        updateUsernameValid();
        if (usernameValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
    } else if (name.value !== nameOldValue) {
        nameOldValue = name.value;
        updateNameValid();
        if (nameValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
    } else if (surname.value !== surnameOldValue) {
        surnameOldValue = surname.value;
        updateSurnameValid();
        if (surnameValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
    } else if (password.value !== passwordOldValue) {
        passwordOldValue = password.value;
        updatePasswordValid();
        if (repeatPasswordValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
        if (passwordValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
    } else if (repeatPassword.value !== repeatPasswordOldValue) {
        repeatPasswordOldValue = repeatPassword.value;
        updateRepeatPasswordValid();
        if (repeatPasswordValid)
            info.style["color"] = "green";
        else
            info.style["color"] = "red";
    }
})

addMultipleListeners(username, ["mouseover", "focusin"], () => {
    info.innerText = "At least 3 characters long, may contain letters and digits"
    if (usernameValid) info.style["color"] = "green";
    else info.style["color"] = "red";
})

addMultipleListeners(name, ["mouseover", "focusin"], () => {
    info.innerText = "Not blank, contains only letters, starts with uppercase";
    if (nameValid) info.style["color"] = "green";
    else info.style["color"] = "red";
})

addMultipleListeners(surname, ["mouseover", "focusin"], () => {
    info.innerText = "Contains only letters, starts with upper case";
    if (surnameValid) info.style["color"] = "green";
    else info.style["color"] = "red";
})

addMultipleListeners(password, ["mouseover", "focusin"], () => {
    info.innerText = "Between 8 - 20 characters, contains only letters and at least one digit";
    if (passwordValid) info.style["color"] = "green";
    else info.style["color"] = "red";
})

addMultipleListeners(repeatPassword, ["mouseover", "focusin"], () => {
    info.innerText = "Same as above";
    if (repeatPasswordValid) info.style["color"] = "green";
    else info.style["color"] = "red";
})

document.querySelectorAll("input, label").forEach(element => {
    addMultipleListeners(element, ["mouseleave", "focusout"], () => {
        info.innerText = "";
    })
})
