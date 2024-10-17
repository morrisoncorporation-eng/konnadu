window.addEventListener("load", getCart)


function getCart() {
    const cartItem = document.querySelectorAll(".css-1fdkffg");
    let NikeCart = []
    cartItem.forEach(item => {
        const items = {
            name: "Nike",
            image: item.querySelector("img").src,
            size: item.querySelector("[data-automation='size-select']").value,
            title: item.querySelector("[data-automation='cart-item-product-name']").textContent,
            price: item.querySelector(".price").textContent,
            original_price: item.querySelector('.original-price').textContent,
            sales_price: item.querySelector('.sale-price').textContent,
            quantity: item.querySelector("[data-automation='quantity-select']").value,
        }
        NikeCart.push(items)

        const cart = []
        
        for (const key in NikeCart) {
             if (Object.hasOwnProperty.call(NikeCart, key)) {
                 let element = NikeCart[key];
                 if(element.sales_price.length > 0){
                    element.price = element.sales_price
                    console.log("Sales price is available.")
                 }
                 cart.push(element)
             }
         }
        console.log(cart)
        // // NikeCart = cart
        // console.log(cart)
        chrome.storage.local.set({ NikeCart: cart });
    })
}

