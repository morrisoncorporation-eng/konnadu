window.addEventListener("load", getCart)


function getCart() {
    AliexpressCart = []
    
    const productContainer = document.querySelectorAll('.product-container');
    productContainer.forEach(product => {
      const productItems = {
            name: "Aliexpress",
            image: product.querySelector("img").src,
            title: product.querySelector(".product-name-link").textContent,
            price: product.querySelector(".main-cost-price").textContent,
            quantity: product.querySelector(".next-input").firstChild.value,
            // description: product.querySelector("dl").innerHTML
        }
        AliexpressCart.push(productItems);
    })

    chrome.storage.local.set({ AliexpressCart: AliexpressCart });
}

