window.addEventListener("load", getCart)

function getCart() {
    const cartItem = document.querySelectorAll(".fluid-item");
    const BestBuyCart = []
    cartItem.forEach(item => {
        const items = {
            name: 'BestBuy',
            image: item.querySelector(".cart-item__image").src,
            title: item.querySelector(".cart-item__title").textContent,
            price: item.querySelector(".price-block__primary-price").textContent,
            quantity: item.querySelector(".tb-select").value
        }
        BestBuyCart.push(items)
        chrome.storage.local.set({ BestBuyCart: BestBuyCart });
    });
}