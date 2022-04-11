function toggleModal(elem) {
    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector(elem).classList.toggle("hidden");
}

function updateCharacterCounter(input) {
    const counter = document.querySelector(`[data-input-name='${input.name}']`);
    counter.textContent = `${input.value.length} / ${input.getAttribute("maxlength")}`;
}

async function createUser() {
    const form = event.target.form;

    const userFirstName = form.user_first_name;
    const userLastName = form.user_last_name;
    const userEmail = form.user_email;
    const userHandle = form.user_handle;
    const userPassword = form.user_password;
    const userConfirmPassword = form.user_confirm_password;

    const userFirstNameValid = validName(userFirstName);
    const userLastNameValid = validName(userLastName);
    const userEmailValid = validEmail(userEmail);
    const userHandleValid = validHandle(userHandle);
    const userPasswordValid = validPassword(userPassword)
    
    if (!userFirstNameValid || !userLastNameValid || !userEmailValid || !userHandleValid || !userPasswordValid) {
        userPassword.value = "";
        userConfirmPassword.value = "";
        return false;
    }

    if (userPassword.value != userConfirmPassword.value) {
        userConfirmPassword.value = "";
        userConfirmPassword.classList.add("invalid");
        return false;
    } else {
        userConfirmPassword.classList.remove("invalid");
    }

    const connection = await fetch('/signup', {
        method: "POST",
        body: new FormData(form)
    });
    const response = await connection.json();
    console.log(connection);
    console.log(response);
    if (!connection.ok) {
        const info = response.info.toLowerCase();
        if (info.includes("email")) {
            document.querySelector(`.hint[data-input-name='${userEmail.name}']`).textContent = response.info;
            userEmail.classList.add("invalid");
            return false;
        }
        if (info.includes("username") || info.includes("brugernavn")) {
            document.querySelector(`.hint[data-input-name='${userHandle.name}']`).textContent = response.info;
            userHandle.classList.add("invalid");
            return false;
        }
        if (connection.status === 500) {
            document.querySelector("#error_message").textContent = "An error occured. Please try again.";
            document.querySelector("#error_message").classList.remove("hidden");
            return false;
        }
    } else {
        window.location.href = "/login";
    }
}

async function logIn() {
    const form = event.target.form;

    const userEmail = form.user_email;
    const userPassword = form.user_password;

    const userEmailValid = validEmail(userEmail);
    const userPasswordValid = validPassword(userPassword);
    if (!userEmailValid || !userPasswordValid) {
        userPassword.value = "";
        return false;
    }

    const connection = await fetch('/login', {
        method: "POST",
        body: new FormData(form)
    });
    const response = await connection.json();
    console.log(connection);
    console.log(response);

    if (!connection.ok) {
        const info = response.info.toLowerCase();
        if (info.includes("email")) {
            document.querySelector(`.hint[data-input-name='${userEmail.name}']`).textContent = response.info;
            userEmail.classList.add("invalid");
            return false;
        }
        if (info.includes("password") || info.includes("kodeordet")) {
            document.querySelector(`.hint[data-input-name='${userPassword.name}']`).textContent = response.info;
            userPassword.classList.add("invalid");
            return false;
        }
        if (connection.status === 500) {
            document.querySelector("#error_message").textContent = "An error occured. Please try again.";
            document.querySelector("#error_message").classList.remove("hidden");
            return false;
        }
    } else {
        window.location.href = "/home"
    }
}

