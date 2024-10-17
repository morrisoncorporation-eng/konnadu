cartBtn = document.querySelector(".CartCount");

cartBtn.addEventListener("click", getCart)



function getCart() {
    const delay = 2;
    const limit = 5;
    let i = 1;

    console.log('START!');
    const limitedInterval = setInterval(() => {
        console.log(`message ${i}, appeared after ${delay * i++} seconds`);
        const FootlockerCart = []
        const selector = document.querySelectorAll('.c-product--list')
        console.log(selector)

        if (selector.length > 0) {
            selector.forEach(item => {
                const items = {
                    name: 'Footlocker',
                    image: item.querySelector('img').src,
                    size: item.querySelectorAll('tr')[0].querySelector('td').textContent,
                    title: item.querySelector('.Heading-main.font-heading-5').children[0].textContent,
                    price: item.querySelector('.ProductPrice').children[0].textContent,
                    quantity: item.querySelectorAll('tr')[1].querySelector('td').textContent,
                }
                FootlockerCart.push(items)
            });
            chrome.storage.local.set({ FootlockerCart: FootlockerCart });
            console.log(FootlockerCart)
        }
        if (i > limit) {
            clearInterval(limitedInterval);
            console.log('interval cleared!');
        }
    }, delay * 1000);
}



