window.addEventListener("load", getCart)


function getCart() {
    AmazonCart = []
    
    const productContainer = document.querySelectorAll('.sc-list-item-content');
    productContainer.forEach(product => {
      const productItems = {
            name: "Amazon",
            image: product.querySelector("img").src,
            title: product.querySelector(".a-truncate-full").textContent,
            price: product.querySelector(".sc-product-price").textContent,
            quantity: product.querySelector(".a-dropdown-prompt").textContent,
        }
        AmazonCart.push(productItems);
    })

    chrome.storage.local.set({ AmazonCart: AmazonCart });
}
