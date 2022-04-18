let tweetTextInput;
let tweetImageInput;

window.addEventListener("DOMContentLoaded", () => {
    tweetTextInput = document.querySelectorAll("textarea.tweet-input");
    tweetImageInput = document.querySelectorAll("[type='file'].tweet-input");

    tweetTextInput.forEach(input => {
        input.addEventListener("input", () => {
            input.style.height = input.scrollHeight+"px";
            const button = document.querySelector(`button[data-form-id='${input.dataset.formId}']`)
            if (input.value.length > 0 && button.hasAttribute("disabled")) {
                button.removeAttribute("disabled");
            } 
            if (input.value.length === 0) {
                button.setAttribute("disabled", true);
            }
        });
    });
    tweetImageInput.forEach(input => {
        input.addEventListener("change", () => {
            const preview = document.querySelector(`[data-input-id='${input.id}']`);
            const image = input.files[0];
            preview.querySelector("img").src = URL.createObjectURL(image);
            preview.classList.remove("hidden");
        })
    });
});

function toggleModal(elem) {
    const tweetId = event.target.dataset.tweetId;
    const deleteBtn = document.querySelector(".btn-danger");
    if (tweetId !== undefined && deleteBtn) {
        deleteBtn.setAttribute("data-tweet-id", tweetId);
        closeAllMenus();
    }
    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector(elem).classList.toggle("hidden");
}

function toggleUpdateModal() {
    const tweetId = event.target.dataset.tweetId;

    const tweet = document.querySelector(`#tweet-${tweetId}`);
    const temp = document.querySelector("#update-tweet-temp");
    const dest = document.querySelector("#update-tweet");
    dest.innerHTML = "";
    const clone = temp.cloneNode(true).content;
    
    clone.querySelector("[name='tweet_id']").value = tweetId;
    clone.querySelector("#tweet_text_update").addEventListener("input", () => {
        const input = event.target;
        input.style.height = input.scrollHeight+"px";
    });
    clone.querySelector("#tweet_text_update").value = tweet.querySelector(".tweet_text").textContent;
    const tweetImg = tweet.querySelector('.tweet_image');
    if (tweetImg) {
        const src = tweetImg.src;
        const imageSrc = src.substring(src.lastIndexOf("/") + 1);
        clone.querySelector("[name='tweet_image_name'][type='hidden']").value = imageSrc;
        clone.querySelector(".preview img").src = src;
        clone.querySelector(".preview").classList.toggle('hidden');
    }
    clone.querySelector("#tweet_image_update").addEventListener("change", () => {
        const input = event.target;
        const preview = document.querySelector(`[data-input-id='${input.id}']`);
        const image = input.files[0];
        preview.querySelector("img").src = URL.createObjectURL(image);
        preview.classList.remove("hidden");
    });

    dest.appendChild(clone);

    closeAllMenus();
    toggleModal('#tweet-update-modal');
}

function toggleMenu() {
    const targetMenu = event.target.dataset.menu;    
    document.querySelector(`#${targetMenu}`).classList.toggle("hidden");
}

function closeAllMenus() {
    document.querySelectorAll(".menu").forEach(el => {
        el.classList.add("hidden");
    });
}

function updateCharacterCounter(input) {
    const counter = document.querySelector(`[data-input-name='${input.name}']`);
    counter.textContent = `${input.value.length} / ${input.getAttribute("maxlength")}`;
}

function removeTweetImage() {
    const inputId = event.target.dataset.inputId;
    document.querySelector(`#${inputId}`).value = "";
    document.querySelector(`.preview[data-input-id='${inputId}'] img`).src = "";
    document.querySelector(`.preview[data-input-id='${inputId}']`).classList.add("hidden");
    const inputHidden = document.querySelector(`[type='hidden'][data-input-id='${inputId}']`)
    if (inputHidden) {
        inputHidden.value = "";
    }
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

async function tweet(fromModal) {
    const form = event.target.form;
    if (form.user_id.value === "") {
        return false;
    }
    if (form.tweet_text.value === "") {
        return false;
    } 

    const connection = await fetch("/tweet", {
        method: "POST",
        body: new FormData(form)
    });
    if (!connection.ok) {
        return
    } else {
        form.tweet_text.value = "";
        form.tweet_image.value = "";
        form.tweet_text.style.height = "30px";
        document.querySelector(`[data-input-id='${form.tweet_image.id}'] img`).src = "";
        document.querySelector(`[data-input-id='${form.tweet_image.id}']`).classList.add("hidden");
        document.querySelector(`button[data-form-id='${form.id}']`).setAttribute("disabled", true);
        if (fromModal) {
            toggleModal('#tweet-modal');
        }
    }
    const tweet = await connection.json();

    const temp = document.querySelector("#tweet_temp");
    const clone = temp.cloneNode(true).content;
    clone.querySelector("#tweet-").setAttribute("id", `tweet-${tweet.tweet_id}`);
    clone.querySelectorAll("a[data-tweet-id]").forEach(el => {
        el.setAttribute("data-tweet-id", tweet.tweet_id);
    });
    clone.querySelector(".user_image").src = `./images/${tweet.user_image_src}`;
    clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
    clone.querySelector(".user_handle").textContent += tweet.user_handle;
    clone.querySelector(".tweet_created_at_date").textContent = "Now";
    clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
    if (tweet.tweet_image != "") {
        clone.querySelector(".tweet_image").src = `./images/${tweet.tweet_image}`;
    } else {
        clone.querySelector(".tweet_image").remove();
    }

    const dest = document.querySelector("#tweets");
    const firstChild = dest.firstChild;
    dest.insertBefore(clone, firstChild);
}

async function deleteTweet() {
    const tweetId = event.target.dataset.tweetId;

    const connection = await fetch(`/tweet/${tweetId}`, {
        method: "DELETE"
    })
    if (!connection.ok) {
        return
    }
    document.querySelector(`#tweet-${tweetId}`).remove();
    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector("#tweet-delete-modal").classList.toggle("hidden");
}

async function updateTweet() {
    const form = event.target.form;
    const tweetId = form.tweet_id.value;
    
    const connection = await fetch(`/tweet/${tweetId}`, {
        method: "PUT",
        body: new FormData(form)
    });
    const response = await connection.json();
    if (!connection.ok) {
        return
    }
    
    const tweet = document.querySelector(`#tweet-${response.tweet_id}`);
    const tweetText = tweet.querySelector(".tweet_text");
    tweetText.textContent = response.tweet_text;

    const tweetImage = tweet.querySelector(".tweet_image");
    if (response.tweet_image === "" && tweetImage) {
        tweetImage.remove();
    } 
    if (response.tweet_image !== "" && !tweetImage) {
        const img = document.createElement("img");
        img.classList.add('tweet_image mb-2', 'w-full', 'rounded-xl', 'border', 'border-twitter-grey1-50');
        img.src = `./images/${response.tweet_image}`;
        tweetText.after(img);
    }
    if (response.tweet_image !== "" && tweetImage) {
        tweetImage.src = `./images/${response.tweet_image}`;
    }
    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector('#tweet-update-modal').classList.toggle("hidden");
}

async function followUser() {
    const [userId, followUserId, followUserHandle] = [event.target.dataset.userId, event.target.dataset.followUserId, event.target.dataset.followUserHandle];

    const connection = await fetch(`/follow/${userId}/${followUserId}`, {
        method: "POST"
    });
    if (!connection.ok) {
        return
    }
    const allFollowBtns = document.querySelectorAll(`a[data-user-id='${userId}'][data-follow-user-id='${followUserId}'][data-follow-user-handle='${followUserHandle}']`);
    allFollowBtns.forEach(btn => {
        const parent = btn.parentElement;
        const temp = document.querySelector("#unfollowTemp");
        const clone = temp.cloneNode(true).content;
        clone.querySelector("a").setAttribute("data-user-id", userId);
        clone.querySelector("a").setAttribute("data-unfollow-user-id", followUserId);
        clone.querySelector("a").setAttribute("data-unfollow-user-handle", followUserHandle);
        clone.querySelector("span").textContent += followUserHandle;
        parent.appendChild(clone);
        btn.remove();
    })
}

async function unfollowUser() {
    const [userId, unfollowUserId, unfollowUserHandle] = [event.target.dataset.userId, event.target.dataset.unfollowUserId, event.target.dataset.unfollowUserHandle];
    console.log(userId, unfollowUserId, unfollowUserHandle);

    const connection = await fetch(`/follow/${userId}/${unfollowUserId}`, {
        method: "DELETE"
    });
    console.log(connection);
    if (!connection.ok) {
        return
    }
    const allUnfollowBtns = document.querySelectorAll(`a[data-user-id='${userId}'][data-unfollow-user-id='${unfollowUserId}'][data-unfollow-user-handle='${unfollowUserHandle}']`);
    allUnfollowBtns.forEach(btn => {
        const parent = btn.parentElement;
        const temp = document.querySelector("#followTemp");
        const clone = temp.cloneNode(true).content;
        clone.querySelector("a").setAttribute("data-user-id", userId);
        clone.querySelector("a").setAttribute("data-follow-user-id", unfollowUserId);
        clone.querySelector("a").setAttribute("data-follow-user-handle", unfollowUserHandle);
        clone.querySelector("span").textContent += unfollowUserHandle;
        parent.appendChild(clone);
        btn.remove();
    })
}