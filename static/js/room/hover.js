const exit = document.getElementById("exit");

exit.addEventListener("mouseover", () => {
    if (exit.getAttribute("src") == "/static/imgs/exit.png") exit.setAttribute("src", "/static/imgs/exit-red.png");
})

exit.addEventListener("mouseout", () => {
    exit.setAttribute("src", "/static/imgs/exit.png");
})