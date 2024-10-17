// "use strict";
let counter = 1

const more = document.getElementById("load-more");


document.body.addEventListener('htmx:beforeRequest', function (evt) {
    console.log(evt)
    const page = document.getElementById("page");
    const eventPath = evt.detail.pathInfo.path
    if (eventPath == "/more/") {
        counter += 1
        page.value = counter
        console.log(page)
    } else {
        counter = 1
    }
});


