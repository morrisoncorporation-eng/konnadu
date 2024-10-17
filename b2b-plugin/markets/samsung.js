window.addEventListener("load", getCart)


function getCart() {
    const cartItem = document.querySelectorAll(".ec-cart-items-row-holder");
    const SamsungCart = []
    cartItem.forEach(item => {
        const items = {
            name: "Samsung",
            image: item.querySelector("img").src,
            title: item.querySelector(".ec-cart-prd-name").children[0].textContent,
            price: item.querySelector(".ec-cart-prd-display-price").textContent,
            quantity: item.querySelector(".label").textContent,
        }
        SamsungCart.push(items)
        chrome.storage.local.set({ SamsungCart: SamsungCart });
    })
}