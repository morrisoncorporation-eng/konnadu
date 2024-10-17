// window.addEventListener("load", getCart);
const cartBtn = document.querySelector(".bn.bg-transparent.br2.db.flex.flex-column.items-center.pa0.pointer.relative.sans-serif.white")

const checkElement = async selector => {
    while (document.querySelector(selector) === null) {
        await new Promise(resolve => requestAnimationFrame(resolve))
    }
    return document.querySelector(selector);
};

cartBtn.addEventListener("click", function () {
    const WalmartCart = []
    checkElement("#ItemDetailsFCGroup").then((selector) => {
        selector.click();
        
        const liContainer = document.querySelectorAll(".list.dark-gray");
        console.log(liContainer)
        liContainer.forEach(item => {
            const items = {
                name: 'Walmart',
                image: item.querySelector('.pointer').src,
                title: item.querySelector('.sans-serif.f5-l.lh-copy-l.lh-title.overflow-hidden.dark-gray').textContent,
                price: item.querySelector('.f5.lh-copy.h2-l.f4-l.lh-title-l.b.tr').firstElementChild.textContent,
                quantity: 1,
            }
            WalmartCart.push(items)
        });
        chrome.storage.local.set({ WalmartCart: WalmartCart });

        console.log(WalmartCart)
    });
})
// function getCart() {
//     console.log("Running...")
//     // const cartItem = document.querySelectorAll(".rs-iteminfo.row")
//     // const WalmartCart = []
//     // cartItem.forEach(item => {
//     //     const items = {
//     //         name: 'Walmart',
//     //         image: item.querySelector('.rs-iteminfo-image').children[0].src,
//     //         title: item.querySelector('.rs-iteminfo-title').children[0].textContent,
//     //         price: item.querySelector('.rs-iteminfo-price').children[0].textContent,
//     //         quantity: item.querySelector('.rs-quantity-dropdown').value
//     //     }
//     //     WalmartCart.push(items)

//     // })
//     // chrome.storage.local.set({ WalmartCart: WalmartCart });
// }
