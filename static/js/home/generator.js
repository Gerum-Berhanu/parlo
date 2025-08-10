function generateRandomCode() {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    // Get a random length between 6 and 16
    // const length = Math.floor(Math.random() * 11) + 6;
    let result = '';

    for (let i = 0; i < 8; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        result += characters[randomIndex];
    }

    return result;
}

const codeGeneratorKey = document.getElementById("room-code-key")
const codeArea = document.getElementById("code-area")
codeGeneratorKey.addEventListener("click", () => codeArea.value = generateRandomCode());

// ---+---+---+---

function generateRandomName() {
    const names = ["Rick", "Morty", "Summer", "Jerry", "Beth"];
    const randomIndex = Math.floor(Math.random() * names.length);
    return names[randomIndex];
}

const nameGeneratorKey = document.getElementById("name-code-key");
const nameArea = document.getElementById("name-area");
nameGeneratorKey.addEventListener("click", () => nameArea.value = generateRandomName());