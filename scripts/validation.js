function validDigit(digit) {
    const NaN = isNaN(digit);
    if (NaN) {
        return false;
    }
    return true;
}

function validName(input) {
    const validity = input.validity;
    const hint = document.querySelector(`.hint[data-input-name='${input.name}']`);
    const typeOfName = input.name.substring(input.name.indexOf("_") + 1, input.name.lastIndexOf("_"));
    const min = parseInt(input.getAttribute("minlength"));
    const max = parseInt(input.getAttribute("maxlength"));
    if (validity.valueMissing) {
        input.classList.add("invalid");
        hint.textContent = `Please enter your ${typeOfName} name.`;
        return false;
    } else if (validity.tooShort || input.value.length < min) {
        input.classList.add("invalid");
        hint.textContent = `Your ${typeOfName} name should be more than ${min} characters.`;
        return false;
    } else if (validity.tooLong || input.value.length > max) {
        input.classList.add("invalid");
        hint.textContent = `Your ${typeOfName} name should be less than ${max} characters.`;
        return false;
    } else {
        input.classList.remove("invalid");
        hint.textContent = "";
    }
    return true;
} 

function validEmail(input) {
    const validity = input.validity;
    const hint = document.querySelector(`.hint[data-input-name='${input.name}']`);
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (validity.valueMissing) {
        input.classList.add("invalid");
        hint.textContent = "Please enter your e-mail.";
        return false;
    } else if (validity.typeMismatch || validity.patternMismatch || !re.test(input.value.toLowerCase())) {
        input.classList.add("invalid");
        hint.textContent = "Please enter a valid e-mail."
        return false;
    } else {
        input.classList.remove("invalid");
        hint.textContent = "";
    }
    return true;
}

function validHandle(input) {
    const validity = input.validity;
    const hint = document.querySelector(`.hint[data-input-name='${input.name}']`);
    const re = /^(?!.*[\.\-\_]{2}).*^[a-zA-Z0-9\.\-\_]*$/gm;
    const min = input.getAttribute("minlength");
    const max = input.getAttribute("maxlength");

    if (validity.valueMissing) {
        input.classList.add("invalid");
        hint.textContent = "Please enter your desired username.";
        return false;
    } else if (validity.tooShort || input.value.length < min) {
        input.classList.add("invalid");
        hint.textContent = `Your username should be more than ${min} characters.`;
        return false;
    } else if (validity.tooLong || input.value.length > max) {
        input.classList.add("invalid");
        hint.textContent = `Your username should be less than ${max} characters.`;
        return false;
    } else if (validity.patternMismatch || !re.test(input.value.toLowerCase())) {
        input.classList.add("invalid");
        hint.textContent = "Only alphanumeric characters and '.' '-' or '_' allowed. Special characters can't be repeated.";
        return false;
    } else {
        input.classList.remove("invalid");
        hint.textContent = "";
    }
    return true;  
}

function validPassword(input) {
    const validity = input.validity;
    const hint = document.querySelector(`.hint[data-input-name='${input.name}']`);
    const min = parseInt(input.getAttribute("minlength"));
    // const re = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/gm;

    if (validity.valueMissing) {
        input.classList.add("invalid");
        hint.textContent = `Please enter a password.`;
        return false;
    } else if (validity.tooShort || input.value.length < min) {
        input.classList.add("invalid");
        hint.textContent = `Your password should be more than ${min} characters.`;
        return false;
    } else if (validity.patternMismatch //|| !re.test(input.value.toLowerCase())
    ) {
        input.classList.add("invalid");
        hint.textContent = `Password should contain min. one lowercase letter, one uppercase letter and one number.`;
        return false;
    } else {
        input.classList.remove("invalid");
        hint.textContent = "";
    }
    return true;
}

function validText(input) {
    const validity = input.validity;
    const min = parseInt(input.getAttribute("minlength"));
    const max = parseInt(input.getAttribute("maxlength"));

    if (validity.valueMissing) {
        return false;
    }
    if (validity.tooShort || input.value.length < min) {
        return false;
    }
    if (validity.tooLong || input.value.length > max) {
        return false;
    }
    return true;
}

function validDescription(input) {
    const validity = input.validity;
    const hint = document.querySelector(`.hint[data-input-name='${input.name}']`);
    const min = parseInt(input.getAttribute("minlength"));
    const max = parseInt(input.getAttribute("maxlength"));

    if (validity.valueMissing) {
        input.classList.add("invalid");
        hint.textContent = `Please create your bio.`;
        return false;
    } else if (validity.tooShort || input.value.length < min) {
        input.classList.add("invalid");
        hint.textContent = `Your bio should be more than ${min} characters.`;
        return false;
    } else if (validity.tooLong || input.value.length > max) {
        input.classList.add("invalid");
        hint.textContent = `Your bio should be less than ${max} characters.`;
        return false;
    } else {
        input.classList.remove("invalid");
        hint.textContent = "";
    }
    return true;
}