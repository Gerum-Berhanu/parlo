document.addEventListener("DOMContentLoaded", () => {
    const socket = io();

    const chatCont = document.getElementById("chat-container")
    const sendBtn = document.getElementById("chat-send-btn");
    const totalMembers = document.getElementById("total-members");

    function createMessage(name, message, members) {
        let customBg = "";
        if (message == "has entered the room.") customBg = "bg-lime-500/25";
        else if (message == "has left the room.") customBg = "bg-rose-500/25";
        else customBg = "bg-black/25";

        const newElement = document.createElement("div")
        newElement.innerHTML = `
        <div class="mb-5">
            <div class="font-extrabold text-white ${customBg} rounded-t-xl p-3">${name}</div>
            <div class="bg-white/75 p-3 rounded-b-xl">${message}</div>
        </div>
        `;
        if (chatCont.firstElementChild.textContent == "No messages yet...") chatCont.removeChild(chatCont.firstElementChild)
        chatCont.insertBefore(newElement, chatCont.firstElementChild);
        totalMembers.textContent = members;
    }

    socket.on("message", data => createMessage(data.name, data.message, data.members));

    socket.on('notification', function (data) {
        if (Notification.permission === 'granted') {
            const options = {
                body: data.message,
                icon: "/static/imgs/logo.png"
            }
            const n = new Notification(data.name, options);
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission().then(function (permission) {
                if (permission === 'granted') {
                    const options = {
                        body: data.message,
                        icon: "/static/imgs/logo.png"
                    }
                    const n = new Notification(data.name, options);
                }
            });
        }
    });

    const myMsg = document.getElementById("my-message");
    
    function messenger() {
        if (myMsg.value == "") return;
        socket.emit("message", { data: myMsg.value.trim() });
        myMsg.value = "";
    }

    sendBtn.addEventListener("click", messenger);
    myMsg.addEventListener("keyup", event => {
        if (event.key == "Enter") messenger();
    })
});