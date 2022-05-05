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

function updateInputHeight() {
    const input = event.target;
    input.style.height = input.scrollHeight+"px";
    const button = document.querySelector(`button[data-form-id='${input.dataset.formId}']`)
    if (input.value.length > 0 && button.hasAttribute("disabled")) {
        button.removeAttribute("disabled");
    } 
    if (input.value.length === 0) {
        button.setAttribute("disabled", true);
    }
}

function updateUserImage() {
    const input = event.target;
    const imgEl = document.querySelector(`[data-input-id='${input.id}']`);
    const image = input.files[0];
    imgEl.src = URL.createObjectURL(image);
}

function updateUserCoverImage() {
    const input = event.target;
    const elem = document.querySelector(`[data-input-id='${input.id}']`);
    const image = input.files[0];
    elem.style.backgroundImage = `url('${URL.createObjectURL(image)}')`;
}

function updatePreviewImage() {
    const input = event.target;
    const preview = document.querySelector(`[data-input-id='${input.id}']`);
    const image = input.files[0];
    preview.querySelector("img").src = URL.createObjectURL(image);
    preview.classList.remove("hidden");
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
    const [userId, tweetText] = [form.user_id, form.tweet_text];
    const [validUserId, validTweetText] = [validDigit(userId.value), validText(tweetText)];

    if (!validUserId || !validTweetText) {
        return 
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
            document.querySelector("body").classList.toggle("overflow-hidden");
            document.querySelector("#tweet-modal").classList.toggle("hidden");
        }
    }
    const tweet = await connection.json();

    const temp = document.querySelector("#tweet_temp");
    const clone = temp.cloneNode(true).content;
    clone.querySelector("#tweet-").setAttribute("id", `tweet-${tweet.tweet_id}`);
    clone.querySelectorAll("a[data-tweet-id]").forEach(el => {
        el.setAttribute("data-tweet-id", tweet.tweet_id);
    });
    clone.querySelector(".user_image").src = `/images/${tweet.user_image_src}`;
    clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
    clone.querySelector(".user_name").setAttribute("href", `/profile/${tweet.user_handle}`);
    clone.querySelector(".user_handle").textContent += tweet.user_handle;
    clone.querySelector(".tweet_created_at_date").textContent = "Now";
    clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
    clone.querySelector(".total_likes").textContent = tweet.tweet_total_likes;
    if (tweet.tweet_image != "") {
        clone.querySelector(".tweet_image").src = `/images/${tweet.tweet_image}`;
    } else {
        clone.querySelector(".tweet_image").remove();
    }

    const dest = document.querySelector("#tweets");
    const firstChild = dest.firstChild;
    dest.insertBefore(clone, firstChild);
}

async function deleteTweet() {
    const tweetId = event.target.dataset.tweetId;

    const validTweetId = validDigit(tweetId);
    if (!validTweetId) {
        return
    }

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
    const tweetText = form.tweet_text;

    const [validTweetId, validTweetText] = [validDigit(tweetId), validText(tweetText)];

    if (!validTweetId || !validTweetText) {
        return
    }
    
    const connection = await fetch(`/tweet/${tweetId}`, {
        method: "PUT",
        body: new FormData(form)
    });
    const response = await connection.json();
    if (!connection.ok) {
        return
    }
    
    const tweet = document.querySelector(`#tweet-${response.tweet_id}`);
    const tweetTextEl = tweet.querySelector(".tweet_text");
    tweetTextEl.textContent = response.tweet_text;

    const tweetImage = tweet.querySelector(".tweet_image");
    if (response.tweet_image === "" && tweetImage) {
        tweetImage.remove();
    } 
    if (response.tweet_image !== "" && !tweetImage) {
        const img = document.createElement("img");
        img.classList.add('tweet_image mb-2', 'w-full', 'rounded-xl', 'border', 'border-twitter-grey1-50');
        img.src = `/images/${response.tweet_image}`;
        tweetTextEl.after(img);
    }
    if (response.tweet_image !== "" && tweetImage) {
        tweetImage.src = `/images/${response.tweet_image}`;
    }
    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector('#tweet-update-modal').classList.toggle("hidden");
}

async function updateUser() {
    const form = event.target.form;
    const userId = form.user_id;
    const userImageSrc = form.user_image_src;
    const userImageName = form.user_image_name;
    const userCoverImage = form.user_cover_image;
    const userCoverImageName = form.user_cover_image_name;
    const userDescription = form.user_description;

    const validId = validDigit(userId.value);
    if (!validId) {
        return false;
    }
    if (userImageName.value === "") {
        return false;
    }
    const userDescriptionValid = validDescription(userDescription);
    if (!userDescriptionValid) {
        return false;
    }
    const connection = await fetch(`/user/${userId.value}`, {
        method: "PUT",
        body: new FormData(form)
    });
    const response = await connection.json();
    const hint = document.querySelector("#update_user_error_message");
    if (!connection.ok) {
        hint.textContent = response.info;
        hint.classList.remove("hidden");
        return false;
    }
    hint.classList.add("hidden");
    const responseImagePath = `/images/${response.user_image_src}`
    form.querySelector("img").src = responseImagePath;
    document.querySelectorAll(".user_image").forEach(img => {
        img.src = responseImagePath;
    });
    document.querySelector("#tweet-modal img").src = responseImagePath;
    document.querySelector(`[onclick="toggleModal('#user-menu')"] img`).src = responseImagePath;
    document.querySelector("#user-menu img").src = responseImagePath;
    form.querySelector("[data-input-id='user_cover_image'").style.backgroundImage = `url('/images/${response.user_cover_image}')`;
    document.querySelector(".bg-twitter-grey1-50.bg-cover.bg-center.bg-no-repeat").style.backgroundImage = `url('/images/${response.user_cover_image}')`;
    document.querySelector(".user_description").textContent = response.user_description;

    userImageSrc.value = "";
    userImageName.value = response.user_image_src;
    userCoverImage.value = "";
    userCoverImageName.value = response.user_cover_image;
    userDescription.value = "";

    document.querySelector("body").classList.toggle("overflow-hidden");
    document.querySelector("#update-user-modal").classList.toggle("hidden");
}

async function followUser() {
    const [userId, followUserId, followUserHandle] = [event.target.dataset.userId, event.target.dataset.followUserId, event.target.dataset.followUserHandle];
    const [validUserId, validFollowUserId] = [validDigit(userId), validDigit(followUserId)]
    if (!validUserId || !validFollowUserId) {
        return
    }
    
    const connection = await fetch(`/follow/${userId}/${followUserId}`, {
        method: "POST"
    });
    if (!connection.ok) {
        return
    }

    const allFollowMenuItems = document.querySelectorAll(`a[data-user-id='${userId}'][data-follow-user-id='${followUserId}'][data-follow-user-handle='${followUserHandle}']`);
    if (allFollowMenuItems) {
        allFollowMenuItems.forEach(item => {
            const parent = item.parentElement;
            const temp = document.querySelector("#unfollowTemp");
            const clone = temp.cloneNode(true).content;
            clone.querySelector("a").setAttribute("data-user-id", userId);
            clone.querySelector("a").setAttribute("data-unfollow-user-id", followUserId);
            clone.querySelector("a").setAttribute("data-unfollow-user-handle", followUserHandle);
            clone.querySelector("span").textContent += followUserHandle;
            parent.appendChild(clone);
            item.remove();
            closeAllMenus();

            const followingEl = document.querySelector("#numFollowing");
            if (followingEl && followingEl.parentElement.dataset.userId === userId) {
                const numFollowers = parseInt(followingEl.textContent);
                followingEl.textContent = numFollowers + 1;
            }
        });
    }
    
    const allFollowBtns = document.querySelectorAll(`button[data-user-id='${userId}'][data-follow-user-id='${followUserId}'][data-follow-user-handle='${followUserHandle}']`);
    if (allFollowBtns) {
        allFollowBtns.forEach(btn => {
            const parent = btn.parentElement;
            const temp = document.querySelector("#unfollowBtnTemp");
            const clone = temp.cloneNode(true).content;
            clone.querySelector("button").setAttribute("data-user-id", userId);
            clone.querySelector("button").setAttribute("data-unfollow-user-id", followUserId);
            clone.querySelector("button").setAttribute("data-unfollow-user-handle", followUserHandle);
            parent.appendChild(clone);
            btn.remove();

            const followersEl = document.querySelector("#numFollowers");
            const numFollowers = parseInt(followersEl.textContent);
            followersEl.textContent = numFollowers + 1;
        })
    }
}

async function unfollowUser() {
    const [userId, unfollowUserId, unfollowUserHandle] = [event.target.dataset.userId, event.target.dataset.unfollowUserId, event.target.dataset.unfollowUserHandle];

    const [validUserId, validUnfollowUserId] = [validDigit(userId), validDigit(unfollowUserId)]
    if (!validUserId || !validUnfollowUserId) {
        return
    }

    const connection = await fetch(`/follow/${userId}/${unfollowUserId}`, {
        method: "DELETE"
    });
    if (!connection.ok) {
        return
    }

    const allUnfollowMenuItems = document.querySelectorAll(`a[data-user-id='${userId}'][data-unfollow-user-id='${unfollowUserId}'][data-unfollow-user-handle='${unfollowUserHandle}']`);
    if (allUnfollowMenuItems) {
        allUnfollowMenuItems.forEach(item => {
            const parent = item.parentElement;
            const temp = document.querySelector("#followTemp");
            const clone = temp.cloneNode(true).content;
            clone.querySelector("a").setAttribute("data-user-id", userId);
            clone.querySelector("a").setAttribute("data-follow-user-id", unfollowUserId);
            clone.querySelector("a").setAttribute("data-follow-user-handle", unfollowUserHandle);
            clone.querySelector("span").textContent += unfollowUserHandle;
            parent.appendChild(clone);
            item.remove();
            closeAllMenus();

            const followingEl = document.querySelector("#numFollowing");
            if (followingEl && followingEl.parentElement.dataset.userId === userId) {
                const numFollowers = parseInt(followingEl.textContent);
                followingEl.textContent = numFollowers - 1;
            }
        })
    }

    const allUnfollowBtns = document.querySelectorAll(`button[data-user-id='${userId}'][data-unfollow-user-id='${unfollowUserId}'][data-unfollow-user-handle='${unfollowUserHandle}']`);
    if (allUnfollowBtns) {
        allUnfollowBtns.forEach(btn => {
            const parent = btn.parentElement;
            const temp = document.querySelector("#followBtnTemp");
            const clone = temp.cloneNode(true).content;
            clone.querySelector("button").setAttribute("data-user-id", userId);
            clone.querySelector("button").setAttribute("data-follow-user-id", unfollowUserId);
            clone.querySelector("button").setAttribute("data-follow-user-handle", unfollowUserHandle);
            parent.appendChild(clone);
            btn.remove();

            const followersEl = document.querySelector("#numFollowers");
            const numFollowers = parseInt(followersEl.textContent);
            followersEl.textContent = numFollowers - 1;
        })
    }
}

async function likeTweet() {
    const [tweetId, userId] = [event.target.dataset.tweetId, event.target.dataset.userId];

    const [validTweetId, validUserId] = [validDigit(tweetId), validDigit(userId)];
    if (!validTweetId || !validUserId) {
        return
    } 

    const connection = await fetch(`/like/${tweetId}/${userId}`, {
        method: "POST"
    });
    if (!connection.ok) {
        return
    }

    const likeBtn = document.querySelector(`.tweet-btn[data-tweet-id='${tweetId}'][data-user-id='${userId}']`);
    likeBtn.removeAttribute("onclick");
    likeBtn.setAttribute("onclick", "unlikeTweet()");
    likeBtn.classList.remove("text-twitter-grey1");
    likeBtn.classList.add("text-twitter-pink1");
    likeBtn.querySelector("i").classList.remove("fa-regular");
    likeBtn.querySelector("i").classList.add("fa-solid");
    const likeBtnSpan = document.querySelector(`.tweet-btn[data-tweet-id='${tweetId}'][data-user-id='${userId}'] ~ .total_likes`);
    likeBtnSpan.classList.remove("text-twitter-grey1");
    likeBtnSpan.classList.add("text-twitter-pink1");
    likeBtnSpan.textContent = parseInt(likeBtnSpan.textContent)+1;
}

async function unlikeTweet() {
    const [tweetId, userId] = [event.target.dataset.tweetId, event.target.dataset.userId];

    const [validTweetId, validUserId] = [validDigit(tweetId), validDigit(userId)];
    if (!validTweetId || !validUserId) {
        return
    } 

    const connection = await fetch(`/like/${tweetId}/${userId}`, {
        method: "DELETE"
    });

    if (!connection.ok) {
        return
    }

    const unlikeBtn = document.querySelector(`.tweet-btn[data-tweet-id='${tweetId}'][data-user-id='${userId}']`);
    unlikeBtn.removeAttribute("onclick");
    unlikeBtn.setAttribute("onclick", "likeTweet()");
    unlikeBtn.classList.remove("text-twitter-pink1");
    unlikeBtn.classList.add("text-twitter-grey1");
    unlikeBtn.querySelector("i").classList.remove("fa-solid");
    unlikeBtn.querySelector("i").classList.add("fa-regular");
    const unlikeBtnSpan = document.querySelector(`.tweet-btn[data-tweet-id='${tweetId}'][data-user-id='${userId}'] ~ .total_likes`);
    unlikeBtnSpan.classList.remove("text-twitter-pink1");
    unlikeBtnSpan.classList.add("text-twitter-grey1");
    unlikeBtnSpan.textContent = parseInt(unlikeBtnSpan.textContent)-1;
}

async function loadTweets() {
    const [userId, offset, btn] = [event.target.dataset.userId, event.target.dataset.offset, event.target];
    
    const [idValid, offsetValid] = [validDigit(userId), validDigit(offset)];
    
    if (!offsetValid) {
        return
    }

    let connection;
    if (userId !== "") {
        if (!idValid) {
            return 
        }
        connection = await fetch(`/tweets/${userId}/following/${offset}`, {
            method: "GET"
        });
    } else {
        connection = await fetch(`/tweets/${offset}`, {
            method: "GET"
        })
    }

    if (!connection.ok) {
        return
    }
    if (connection.status === 204) {
        btn.remove();
        return
    }
    const response = await connection.json();
    const tweets = response.tweets;
    const liked_tweets = response.liked_tweets;
    const follows = response.follows;
    const user_id = response.user_id;

    if (tweets.length < 10) {
        btn.remove();
    } else {
        btn.setAttribute("data-offset", parseInt(offset) + 10);
    }

    tweets.forEach(tweet => {
        const temp = document.querySelector("#tweet_temp");
        const clone = temp.cloneNode(true).content;
        clone.querySelector("#tweet-").setAttribute("id", `tweet-${tweet.tweet_id}`);
        clone.querySelectorAll("a[data-tweet-id]").forEach(el => {
            el.setAttribute("data-tweet-id", tweet.tweet_id);
        });
        clone.querySelector(".user_image").src = `/images/${tweet.user_image_src}`;
        clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
        clone.querySelector(".user_name").setAttribute("href", `/profile/${tweet.user_handle}`);
        clone.querySelector(".user_handle").textContent += tweet.user_handle;
        clone.querySelector(".tweet_created_at_date").textContent = tweet.tweet_created_at_date;
        clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
        if (clone.querySelector(".total_likes")) {
            clone.querySelector(".total_likes").textContent = tweet.tweet_total_likes;
        }
        if (tweet.tweet_image != "") {
            clone.querySelector(".tweet_image").src = `/images/${tweet.tweet_image}`;
        } else {
            clone.querySelector(".tweet_image").remove();
        }
        let tweet_index = -1;
        if (liked_tweets.length > 0) {
            tweet_index = liked_tweets.findIndex(item => item === tweet.tweet_id);
        }
        if (tweet_index !== -1) {
            clone.querySelector(".tweet-btn.pink").setAttribute("onclick", "unlikeTweet()");
            clone.querySelector(".tweet-btn.pink").classList.remove("text-twitter-grey1");
            clone.querySelector(".tweet-btn.pink").classList.add("text-twitter-pink1");
            clone.querySelector(".tweet-btn.pink i").classList.remove("fa-regular");
            clone.querySelector(".tweet-btn.pink i").classList.add("fa-solid");
            clone.querySelector(".total_likes").classList.add("text-twitter-pink1");
        } 
        clone.querySelector(".tweet-btn.pink").setAttribute("data-tweet-id", tweet.tweet_id);
        clone.querySelector(".tweet-btn.pink").setAttribute("data-user-id", user_id);

        if (user_id === "") {
            clone.querySelector("[onclick='toggleMenu()']").remove();
            clone.querySelector(".menu.hidden").remove();
        } else {
            clone.querySelector("[onclick='toggleMenu()']").setAttribute("data-menu", `tweet-menu-${tweet.tweet_id}`);
            clone.querySelector(".menu.hidden").setAttribute("id", `tweet-menu-${tweet.tweet_id}`);

            let follow_index = -1;
            if (follows.length > 0) {
                follow_index = follows.findIndex(item => item === tweet.tweet_user_id);
            }

            if (tweet.tweet_user_id !== user_id && follow_index === -1 && user_id !== userId) {
                clone.querySelector("[onclick='toggleUpdateModal()']").remove();
                clone.querySelector(`[onclick="toggleModal('#tweet-delete-modal')"]`).remove();
                const followBtn = document.createElement("a");
                followBtn.setAttribute("onclick", "followUser()");
                followBtn.setAttribute("data-user-id", user_id);
                followBtn.setAttribute("data-follow-user-id", tweet.tweet_user_id);
                followBtn.setAttribute("data-follow-user-handle", tweet.user_handle);
                followBtn.classList.add("p-4", "block", "transition", "cursor-pointer", "hover:bg-twitter-grey1-10");
                const icon = document.createElement("i");
                icon.classList.add("fa-solid", "fa-user-plus", "fa-fw", "text-twitter-grey1", "pointer-events-none");
                const span = document.createElement("span");
                span.classList.add("pointer-events-none");
                span.textContent = `Follow @${tweet.user_handle}`
                followBtn.appendChild(icon);
                followBtn.appendChild(span);
                clone.querySelector(".menu.hidden").appendChild(followBtn);
            }
            if (tweet.tweet_user_id !== user_id && follow_index !== -1) {
                clone.querySelector("[onclick='toggleUpdateModal()']").remove();
                clone.querySelector(`[onclick="toggleModal('#tweet-delete-modal')"]`).remove();
                const unfollowBtn = document.createElement("a");
                unfollowBtn.setAttribute("onclick", "unfollowUser()");
                unfollowBtn.setAttribute("data-user-id", user_id);
                unfollowBtn.setAttribute("data-unfollow-user-id", tweet.tweet_user_id);
                unfollowBtn.setAttribute("data-unfollow-user-handle", tweet.user_handle);
                unfollowBtn.classList.add("p-4", "block", "transition", "cursor-pointer", "hover:bg-twitter-grey1-10");
                const icon = document.createElement("i");
                icon.classList.add("fa-solid", "fa-user-xmark", "fa-fw", "text-twitter-grey1", "pointer-events-none");
                const span = document.createElement("span");
                span.classList.add("pointer-events-none");
                span.textContent = `Unfollow @${tweet.user_handle}`;
                unfollowBtn.appendChild(icon);
                unfollowBtn.appendChild(span);
                clone.querySelector(".menu.hidden").appendChild(unfollowBtn);
            }
        }

        const dest = document.querySelector("#tweets");
        dest.appendChild(clone);
    })
}

function displayTweets() {
    const [btn, displayId, hideId] = [event.target, event.target.dataset.displayId, event.target.dataset.hideId];
    document.querySelectorAll(".btn-profile-menu-item").forEach(elem => {
        elem.classList.remove("active");
    });
    btn.classList.add("active");
    document.querySelector(hideId).classList.add("hidden");
    document.querySelector(`[data-tweets-container-id='${hideId}']`).classList.add("hidden");
    document.querySelector(displayId).classList.remove("hidden");
    document.querySelector(`[data-tweets-container-id='${displayId}']`).classList.remove("hidden");    
}

async function loadProfileTweets(isLikedTweets, destId) {
    const [userId, offset, btn] = [event.target.dataset.userId, event.target.dataset.offset, event.target];
    const [idValid, offsetValid] = [validDigit(userId), validDigit(offset)];
    if (!idValid || !offsetValid) {
        return
    }
    
    let connection;
    if (!isLikedTweets) {
        connection = await fetch(`/tweets/${userId}/${offset}`, {
            method: "GET"
        });
    } else {
        connection = await fetch(`/liked/tweets/${userId}/${offset}`, {
            method: "GET"
        })
    }

    if (!connection.ok) {
        return
    }
    if (connection.status === 204) {
        btn.remove();
        return
    }
    const response = await connection.json();
    const tweets = response.tweets;
    const liked_tweets = response.liked_tweets;
    const follows = response.follows;
    const user_id = response.user_id;

    if (tweets.length < 10) {
        btn.remove();
    } else {
        btn.setAttribute("data-offset", parseInt(offset) + 10);
    }

    tweets.forEach(tweet => {
        const temp = document.querySelector("#tweet_temp");
        const clone = temp.cloneNode(true).content;
        clone.querySelector("#tweet-").setAttribute("id", `tweet-${tweet.tweet_id}`);
        clone.querySelectorAll("a[data-tweet-id]").forEach(el => {
            el.setAttribute("data-tweet-id", tweet.tweet_id);
        });
        clone.querySelector(".user_image").src = `/images/${tweet.user_image_src}`;
        clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
        clone.querySelector(".user_name").setAttribute("href", `/profile/${tweet.user_handle}`);
        clone.querySelector(".user_handle").textContent += tweet.user_handle;
        clone.querySelector(".tweet_created_at_date").textContent = tweet.tweet_created_at_date;
        clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
        clone.querySelector(".total_likes").textContent = tweet.tweet_total_likes;
        if (tweet.tweet_image != "") {
            clone.querySelector(".tweet_image").src = `/images/${tweet.tweet_image}`;
        } else {
            clone.querySelector(".tweet_image").remove();
        }
        let tweet_index = -1;
        if (liked_tweets.length > 0) {
            tweet_index = liked_tweets.findIndex(item => item === tweet.tweet_id);
        }
        if (tweet_index !== -1) {
            clone.querySelector(".tweet-btn.pink").setAttribute("onclick", "unlikeTweet()");
            clone.querySelector(".tweet-btn.pink").classList.remove("text-twitter-grey1");
            clone.querySelector(".tweet-btn.pink").classList.add("text-twitter-pink1");
            clone.querySelector(".tweet-btn.pink i").classList.remove("fa-regular");
            clone.querySelector(".tweet-btn.pink i").classList.add("fa-solid");
            clone.querySelector(".total_likes").classList.add("text-twitter-pink1");
        } 
        clone.querySelector(".tweet-btn.pink").setAttribute("data-tweet-id", tweet.tweet_id);
        clone.querySelector(".tweet-btn.pink").setAttribute("data-user-id", user_id);

        if (user_id === "") {
            clone.querySelector("[onclick='toggleMenu()']").remove();
            clone.querySelector(".menu.hidden").remove();
        } else {
            clone.querySelector("[onclick='toggleMenu()']").setAttribute("data-menu", `tweet-menu-${tweet.tweet_id}`);
            clone.querySelector(".menu.hidden").setAttribute("id", `tweet-menu-${tweet.tweet_id}`);

            let follow_index = -1;
            if (follows.length > 0) {
                follow_index = follows.findIndex(item => item === tweet.tweet_user_id);
            }

            if (tweet.tweet_user_id !== user_id && follow_index === -1 && user_id !== userId) {
                clone.querySelector("[onclick='toggleUpdateModal()']").remove();
                clone.querySelector(`[onclick="toggleModal('#tweet-delete-modal')"]`).remove();
                const followBtn = document.createElement("a");
                followBtn.setAttribute("onclick", "followUser()");
                followBtn.setAttribute("data-user-id", user_id);
                followBtn.setAttribute("data-follow-user-id", tweet.tweet_user_id);
                followBtn.setAttribute("data-follow-user-handle", tweet.user_handle);
                followBtn.classList.add("p-4", "block", "transition", "cursor-pointer", "hover:bg-twitter-grey1-10");
                const icon = document.createElement("i");
                icon.classList.add("fa-solid", "fa-user-plus", "fa-fw", "text-twitter-grey1", "pointer-events-none");
                const span = document.createElement("span");
                span.classList.add("pointer-events-none");
                span.textContent = `Follow @${tweet.user_handle}`
                followBtn.appendChild(icon);
                followBtn.appendChild(span);
                clone.querySelector(".menu.hidden").appendChild(followBtn);
            }
            if (tweet.tweet_user_id !== user_id && follow_index !== -1) {
                clone.querySelector("[onclick='toggleUpdateModal()']").remove();
                clone.querySelector(`[onclick="toggleModal('#tweet-delete-modal')"]`).remove();
                const unfollowBtn = document.createElement("a");
                unfollowBtn.setAttribute("onclick", "unfollowUser()");
                unfollowBtn.setAttribute("data-user-id", user_id);
                unfollowBtn.setAttribute("data-unfollow-user-id", tweet.tweet_user_id);
                unfollowBtn.setAttribute("data-unfollow-user-handle", tweet.user_handle);
                unfollowBtn.classList.add("p-4", "block", "transition", "cursor-pointer", "hover:bg-twitter-grey1-10");
                const icon = document.createElement("i");
                icon.classList.add("fa-solid", "fa-user-xmark", "fa-fw", "text-twitter-grey1", "pointer-events-none");
                const span = document.createElement("span");
                span.classList.add("pointer-events-none");
                span.textContent = `Unfollow @${tweet.user_handle}`;
                unfollowBtn.appendChild(icon);
                unfollowBtn.appendChild(span);
                clone.querySelector(".menu.hidden").appendChild(unfollowBtn);
            }
        }

        const dest = document.querySelector(destId);
        dest.appendChild(clone);
    })
}

async function loadAdminTweets() {
    const [offset, btn] = [event.target.dataset.offset, event.target];
    
    const [offsetValid] = [validDigit(offset)];
    
    if (!offsetValid) {
        return
    }

    const connection = await fetch(`/tweets/${offset}`, {
        method: "GET"
    })

    if (!connection.ok) {
        return
    }
    if (connection.status === 204) {
        btn.remove();
        return
    }
    const response = await connection.json();
    const tweets = response.tweets;

    if (tweets.length < 10) {
        btn.remove();
    } else {
        btn.setAttribute("data-offset", parseInt(offset) + 10);
    }

    tweets.forEach(tweet => {
        const temp = document.querySelector("#tweet_temp");
        const clone = temp.cloneNode(true).content;
        clone.querySelector("#tweet-").setAttribute("id", `tweet-${tweet.tweet_id}`);
        clone.querySelector(".user_image").src = `/images/${tweet.user_image_src}`;
        clone.querySelector(".user_name").textContent = `${tweet.user_first_name} ${tweet.user_last_name}`;
        clone.querySelector(".user_handle").textContent += tweet.user_handle;
        clone.querySelector(".tweet_created_at_date").textContent = tweet.tweet_created_at_date;
        clone.querySelector(".tweet_text").textContent = tweet.tweet_text;
        if (tweet.tweet_image != "") {
            clone.querySelector(".tweet_image").src = `/images/${tweet.tweet_image}`;
        } else {
            clone.querySelector(".tweet_image").remove();
        }
        clone.querySelector("a").setAttribute("data-tweet-id", tweet.tweet_id);
        const dest = document.querySelector("#tweets");
        dest.appendChild(clone);
    })
}

async function getFollowing(followsListVisible) {
    const userId = event.target.dataset.userId;

    const idValid = validDigit(userId);
    if (!idValid) {
        return
    }

    if (!followsListVisible) {
        window.scrollTo(0, 0);
        document.querySelector("#profile").classList.add("hidden");
        document.querySelector("#follows").classList.remove("hidden");
        document.querySelector("[data-list='following']").classList.add("active");
    } else {
        document.querySelector("#no-follows").classList.add("hidden");
        document.querySelector("#follows-list").innerHTML = "";
        document.querySelectorAll("#follows .btn-profile-menu-item").forEach(btn => {
            btn.classList.remove("active");
        });
        document.querySelector("[data-list='following']").classList.add("active");
    }
    
    const connection = await fetch(`/${userId}/following`, {
        method: "GET"
    });
    if (!connection.ok) {
        return
    }
    if (connection.status === 204) {
        const noFollows = document.querySelector("#no-follows");
        noFollows.querySelector("h3").textContent = "Looking for followings?";
        noFollows.querySelector("p").textContent = "When this account follows someone, they’ll show up here. Tweeting and interacting with others helps boost followings.";
        noFollows.classList.remove("hidden");
        return
    }
    const users = await connection.json();
    users.forEach(user => {
        const temp = document.querySelector("#follows-temp");
        const clone = temp.cloneNode(true).content;

        clone.querySelector("#user-").setAttribute("id", `user-${user.user_id}`);
        clone.querySelector("div[href='']").setAttribute("href", `/profile/${user.user_handle}`);
        clone.querySelector(".user_image").src = `/images/${user.user_image_src}`;
        clone.querySelector(".user_name").textContent = `${user.user_first_name} ${user.user_last_name}`;
        clone.querySelector(".user_handle").textContent = `@${user.user_handle}`;
        clone.querySelector(".user_description").textContent = user.user_description;

        const dest = document.querySelector("#follows-list");
        dest.appendChild(clone);
    });
}

async function getFollowers(followsListVisible) {
    const userId = event.target.dataset.userId;

    const idValid = validDigit(userId);
    if (!idValid) {
        return
    }

    if (!followsListVisible) {
        window.scrollTo(0, 0);
        document.querySelector("#profile").classList.add("hidden");
        document.querySelector("#follows").classList.remove("hidden");
        document.querySelector("[data-list='followers']").classList.add("active");
    } else {
        document.querySelector("#no-follows").classList.add("hidden");
        document.querySelector("#follows-list").innerHTML = "";
        document.querySelectorAll("#follows .btn-profile-menu-item").forEach(btn => {
            btn.classList.remove("active");
        });
        document.querySelector("[data-list='followers']").classList.add("active");
    }

    const connection = await fetch(`/${userId}/followers`, {
        method: "GET"
    });
    if (!connection.ok) {
        return
    }
    if (connection.status === 204) {
        const noFollows = document.querySelector("#no-follows");
        noFollows.querySelector("h3").textContent = "Looking for followers?";
        noFollows.querySelector("p").textContent = "When someone follows this account, they’ll show up here. Tweeting and interacting with others helps boost followers.";
        noFollows.classList.remove("hidden");
        return
    }
    const users = await connection.json();
    users.forEach(user => {
        const temp = document.querySelector("#follows-temp");
        const clone = temp.cloneNode(true).content;

        clone.querySelector("#user-").setAttribute("id", `user-${user.user_id}`);
        clone.querySelector("div[href='']").setAttribute("href", `/profile/${user.user_handle}`);
        clone.querySelector(".user_image").src = `/images/${user.user_image_src}`;
        clone.querySelector(".user_name").textContent = `${user.user_first_name} ${user.user_last_name}`;
        clone.querySelector(".user_handle").textContent = `@${user.user_handle}`;
        clone.querySelector(".user_description").textContent = user.user_description;

        const dest = document.querySelector("#follows-list");
        dest.appendChild(clone);
    });
}

function hideFollows() {
    document.querySelector("#profile").classList.remove("hidden");
    document.querySelector("#follows").classList.add("hidden");
    document.querySelector("#follows-list").innerHTML = "";
    document.querySelectorAll("#follows .btn-profile-menu-item").forEach(btn => {
        btn.classList.remove("active");
    });
}