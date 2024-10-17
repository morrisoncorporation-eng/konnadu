window.addEventListener("load", getCart);

function getCart() {
    const cartItem = document.querySelectorAll(".listsummary-content")
    const EbayCart = []
    cartItem.forEach(item => {
        const items = {
            name: 'Ebay',
            // image: item.querySelector('image-display').firstElementChild.src,
            image: item.querySelector('img').src,
            title: item.querySelector('.BOLD').textContent,
            price: item.querySelector('.item-price').children[0].textContent,
            quantity: item.querySelector('.listbox__control').value
        }
        EbayCart.push(items)
        chrome.storage.local.set({EbayCart: EbayCart});
    }) 
}