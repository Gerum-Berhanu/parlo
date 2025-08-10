document.addEventListener("DOMContentLoaded", () => {
    // --- exit to home page ---
    const exit = document.getElementById("exit");
    exit.addEventListener("click", () => {
        window.location.href = "/";
    })

    // --- toggle emoji menu ---

    const emojiToggle = document.getElementById("emoji-toggle");
    const emojiMenu = document.getElementById("emoji-menu");

    emojiToggle.addEventListener("click", event => {
        event.stopPropagation();
        if (emojiMenu.classList.contains("hidden")) {
            emojiMenu.classList.remove("hidden")
            emojiMenu.classList.add("block")
        } else {
            emojiMenu.classList.add("hidden")
            emojiMenu.classList.remove("block")
        }
    })

    document.addEventListener("click", (event) => {
        // Check if the click was outside the emojiMenu and emojiToggle elements
        if (!emojiMenu.contains(event.target) && !emojiToggle.contains(event.target)) {
            emojiMenu.classList.add("hidden");
            emojiMenu.classList.remove("block");
        }
    });

    // --- select emojis ---

    const emojis = document.querySelectorAll(".emojis");
    const messageInput = document.getElementById("my-message");

    emojis.forEach(emo => {
        emo.addEventListener("click", event => {
            messageInput.value += emo.textContent;     
        })
    });

    // --- copy to clipboard ---

    function copyToClipboard(text) {
        if (navigator.clipboard) {
            // Use the Clipboard API if available
            navigator.clipboard.writeText(text).then(() => {
                // console.log('Text copied to clipboard');
                alert(`${text} ~ Copied to Clipboard`);
            }).catch(err => {
                alert(`${text} ~ Could not copy text\n${err}`);
                // console.error('Could not copy text: ', err);
            });
        } else {
            // Fallback for older browsers
            let textarea = document.createElement('textarea');
            textarea.value = text;
            // Make the textarea out of viewport
            textarea.style.position = 'fixed';
            textarea.style.left = '-999999px';
            document.body.appendChild(textarea);
            textarea.focus();
            textarea.select();
            try {
                document.execCommand('copy');
                console.log('Text copied to clipboard');
            } catch (err) {
                console.error('Could not copy text: ', err);
            }
            document.body.removeChild(textarea);
        }
    }

    const roomCodeSpan = document.getElementById("room-code-span");
    roomCodeSpan.addEventListener("click", () => {
        copyToClipboard(roomCodeSpan.textContent);
    })
})