const submitNameArea = document.getElementById("name-area");
const submitCodeArea = document.getElementById("code-area");
const statusMsg = document.getElementById("status-message");

function messenger(text, node = statusMsg) {
    node.style.display = "block";
    node.textContent = text;
}

function processor() {
    let isValid = true;
    if (!submitNameArea.value || !submitCodeArea.value) {
        messenger("Invalid nickname or room code");
        isValid = false;
    }
    return isValid;
}

// ---+---+---+---

const joinBtn = document.getElementById("join-btn");
const createBtn = document.getElementById("create-btn");
const roomForm = document.getElementById("room-form");

async function submitter(event) {
    event.preventDefault();
    if (!processor()) return;

    statusMsg.style.display = "none";
    const formData = new FormData();
    formData.append("nick", submitNameArea.value);
    formData.append("room", submitCodeArea.value);
    formData.append("mode", event.target.getAttribute("name"));

    try {
        const response = await fetch("/", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        if (data.code != 200 && data.code != 302) messenger(data.text);
        if (data.code == 302) window.location.href = data.text;
        console.log(data)
    }
    catch (error) {
        
    }
}

joinBtn.addEventListener("click", submitter);
createBtn.addEventListener("click", submitter);