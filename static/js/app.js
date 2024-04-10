
let orders = []
const myOrders = document.getElementById("orders")

const makeOrder=()=>{
    orders.push(event.target.id)
    updateOrder()
}

window.addEventListener("load", ()=>{
   updateOrder()
})

const updateOrder=()=>{
    myOrders.innerText = orders.length
}
