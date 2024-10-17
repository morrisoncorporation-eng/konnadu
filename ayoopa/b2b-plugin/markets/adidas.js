var myVar = setInterval(getCart, 3000);

function getCart() {
    const cartItem = document.querySelectorAll(".item___3ciCh")
    const AddidasCart = []
    cartItem.forEach(item => {
        const items = {
            name: 'Addidas',
            image: item.querySelector("[data-auto-id='glass-cart-line-item-image']").src,
            title: item.querySelector('.line-item__title___31Byz').textContent,
            attr: item.querySelector('span[cart-line-item-attribute-color]'),
            size: '',
            price: item.querySelector('.gl-price-item').textContent,
            quantity: item.querySelector('.gl-dropdown-custom__select-label-text').textContent
        }
        AddidasCart.push(items)
        console.log(AddidasCart)
    }) 
    chrome.storage.local.set({AddidasCart: AddidasCart});
}
