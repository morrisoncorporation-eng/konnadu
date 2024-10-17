window.addEventListener("load", getCart);

function getCart() {
    const cartItem = document.querySelectorAll(".rs-iteminfo.row")
    const AppleCart = []
    cartItem.forEach(item => {
        const items = {
            name: 'Apple',
            image: item.querySelector('.rs-iteminfo-image').children[0].src,
            title: item.querySelector('.rs-iteminfo-title').children[0].textContent,
            price: item.querySelector('.rs-iteminfo-price').children[0].textContent,
            quantity: item.querySelector('.rs-quantity-dropdown').value
        }
        AppleCart.push(items)

    })
    chrome.storage.local.set({ AppleCart: AppleCart });
}
