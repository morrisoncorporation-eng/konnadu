const loginForm = document.getElementById("login");
const checkoutBtn = document.getElementById("checkout");
const clearCartBtn = document.getElementById("clear-cart");
const notification = document.getElementById("notification");
const cart = []

AppleCart = "AppleCart"
BestBuyCart = "BestBuyCart"
EbayCart = "EbayCart"
AliexpressCart = "AliexpressCart"
SamsungCart = "SamsungCart"
NikeCart = "NikeCart"
AmazonCart = "AmazonCart"
AddidasCart = "AddidasCart"
WalmartCart = "WalmartCart"
FootlockerCart = "FootlockerCart"

cartArr = [
    AppleCart, BestBuyCart,
    EbayCart, AliexpressCart,
    SamsungCart, NikeCart,
    AmazonCart, AddidasCart,
    WalmartCart, FootlockerCart
]


function isLoggedIn() {
    chrome.storage.local.get("user", function (user_info) {

        const user = user_info['user']
        if (user.username.length > 0 && user.password.length > 0) {
            const loginForm = document.getElementById("nav-profile")
            loginForm.innerHTML = `<div>
                <h3 class="text-center">Hello ${user.username}.</h3> 
            <p class="text-center">You already logged in</p>
            </div>`
        }
    });
}

isLoggedIn()

chrome.storage.local.get(null, function (items) {
    Object.entries(items).map(item => {
        if ((item[1].length > 0) && (item[0] != "username") && (item[0] != "password")) {
            // console.log(item)
            cart.push(item[1])
        }
    })
    data = cart.flat();
    const html = document.getElementById("cart");
    if (data.length > 0) {
        html.innerHTML = data.map(item => `
                <tr>
                    <td><img class="img-fluid" width="50" height="50" src=${item.image}>
                    <td class="title">${item.title}</td>
                    <td>${item.quantity}</td>
                    <td>${item.price}</td>
                    <td><button class="btn btn-sm btn-danger remove">remove</button></td>
                </tr>
            
            `).join('\n');
    }
    else {
        document.querySelector(".table-cart").innerHTML = `<div><h3 class="text-center p-4">No item in cart</h3></div>`
        clearCartBtn.classList.add("d-none");
        checkoutBtn.classList.add("d-none");
    }
});

window.onclick = function (event) {
    var target = event.target;
    if (target.matches('.remove')) {
        var parent = event.target.parentElement.parentElement;
        removeItem(parent.querySelector('.title'))
        parent.remove();
        const Kart = document.getElementById("cart")
        if (Kart.children.length === 0) {
            document.querySelector(".table-cart").innerHTML = `<div><h3 class="text-center p-4">No item in cart</h3></div>`
            clearCartBtn.classList.add("d-none");
            checkoutBtn.classList.add("d-none");
        }
    }
}



function removeItem(name) {
    const title = name.textContent;
    chrome.storage.local.get(null, function (items) {
        Object.entries(items).map(item => {
            console.log(item)
            isArr = Object.prototype.toString.call(item[1]) == '[object Array]';
            if (isArr) {
                let cart = item[1].filter(function (obj) {
                    return obj.title != title;
                });

                CartName = item[0]
                kontainer = {}
                kontainer[CartName] = cart

                // console.log(CartName, cart)
                chrome.storage.local.set(kontainer);
            }
        })
    })
}


clearCartBtn.addEventListener("click", function (e) {
    const clearCart = document.querySelector("#clear-cart");
    const clearCartLoading = document.querySelector("#clear-cart-loading");

    clearCart.classList.add("d-none");
    clearCartLoading.classList.remove("d-none");
    chrome.storage.local.remove(cartArr, function () {
        document.querySelector(".table-cart").innerHTML = `<h3 class="text-center bg-info p-4"> Cart cleared...</h3>`
        clearCartLoading.classList.add("d-none");
        checkoutBtn.classList.add("d-none");
        var error = chrome.runtime.lastError;
        if (error) {
            console.error(error);
        }
    })

})

checkoutBtn.addEventListener("click", checkOut)

function checkOut() {
    checkoutBtn.classList.add("d-none");
    document.querySelector("#checkout-loading").classList.remove("d-none");
    newCart = cart.flat();
    chrome.storage.local.get(['user'], function (result) {
        if ((result.user['username'].length == 0 || result.user['username'].length === "undefined") && (result.user['password'].length == 0 || result.user['password'].length === "undefined")) {
            console.log("Console.log no username found")
            document.getElementById("nav-profile-tab").click()
        }
        else {
            document.getElementById("nav-profile-tab").classList.add("d-none")
            fetch('http://localhost:8000/cart/create/', {
                method: 'POST', // or 'PUT'
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user: result.user,
                    cart: newCart
                })
            }).then(response => {
                return response.json()
            })
                .then(data => {
                    clearCartBtn.addEventListener("click", function (e) {
                        chrome.storage.local.remove(cartArr, function () {
                            var error = chrome.runtime.lastError;
                            if (error) {
                                console.error(error);
                            }
                        })
                    })
                    const body = document.getElementById("body").innerHTML = `<div class="" style="width:500px;">
                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                        <strong>Success!</strong> Item(s) added to your cart login to see them.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                    </div>`
                    document.body.style.minWidth = "850px";
                    Swal.fire({
                        title: '<strong class="text-success"><u>Items added to cart</u></strong>',
                        icon: 'info',
                        html:
                            'You can login and view your Cart',
                        showCloseButton: true,
                        focusConfirm: false,
                        confirmButtonText:
                            'Great!',
                    })
                    document.getElementById("link").classList.remove("d-none");
                })
                .catch((error) => {
                    console.error('Error:', error);
                    document.getElementById("nav-info-tab").click();
                    const info = document.getElementById("nav-info");
                    info.innerHTML = `<div class="text-center fs-3">Something went wrong, we will notify you if it's from our end.</div>`
                    user = {
                        username: "",
                        password: ""
                    }
                    checkoutBtn.classList.remove("d-none");
                    document.querySelector("#checkout-loading").classList.add("d-none");
                    chrome.storage.local.set({ user: user })
                    document.getElementById("nav-profile-tab").click();
                });
        }
    })
}


loginForm.addEventListener("submit", function (evt) {
    evt.preventDefault();
    const formData = new FormData(loginForm);
    let user = {};
    formData.forEach(function (value, key) {
        user[key] = value;
    });
    // chrome.storage.local.set({ user: user })
    fetch('http://localhost:8000/cart/user-auth-check/', {
        method: 'POST', // or 'PUT'
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            user: user,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            chrome.storage.local.set({ user: user })
            checkOut()
            loginForm.reset();
            document.getElementById("nav-home-tab").click();
        })
        .catch((error) => {
            console.error('Error:', error);
            document.getElementById("nav-info-tab").click();
            const info = document.getElementById("nav-info");
            info.innerHTML = `<div class="text-center fs-3">Something went wrong</div>`
            checkoutBtn.classList.remove("d-none");
            document.querySelector("#checkout-loading").classList.add("d-none");
            user = {
                username: "",
                password: ""
            }
            chrome.storage.local.set({ user: user })
        });
})