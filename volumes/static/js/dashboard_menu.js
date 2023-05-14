const new_order = document.getElementsByClassName('new_order');
const state_dashboard = document.getElementsByClassName('state_dashboard');
const profile_dashboard = document.getElementsByClassName('profile_dashboard');
const wallet_dashboard = document.getElementsByClassName('wallet_dashboard');
const orders_list_dashboard = document.getElementsByClassName('orders_list_dashboard');
const transactions_dashboard = document.getElementsByClassName('transactions_dashboard');
const support_dashboard = document.getElementsByClassName('support_dashboard');


if (window.location.pathname === '/dashboard/new-order/') {
    for (let i = 0; i < new_order.length; i++) {
        new_order[i].classList.add("bg-warning");
        new_order[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/') {
    for (let i = 0; i < state_dashboard.length; i++) {
        state_dashboard[i].classList.add("bg-warning");
        state_dashboard[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/profile/') {
    for (let i = 0; i < profile_dashboard.length; i++) {
        profile_dashboard[i].classList.add("bg-warning");
        profile_dashboard[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/wallet/') {
    for (let i = 0; i < wallet_dashboard.length; i++) {
        wallet_dashboard[i].classList.add("bg-warning");
        wallet_dashboard[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/orders/') {
    for (let i = 0; i < orders_list_dashboard.length; i++) {
        orders_list_dashboard[i].classList.add("bg-warning");
        orders_list_dashboard[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/transactions/') {
    for (let i = 0; i < transactions_dashboard.length; i++) {
        transactions_dashboard[i].classList.add("bg-warning");
        transactions_dashboard[i].classList.remove("bg-transparent");
    }
} else if (window.location.pathname === '/dashboard/support/' || window.location.pathname.includes('/dashboard/ticket/') || window.location.pathname.includes('/dashboard/submit-ticket/')) {
    for (let i = 0; i < support_dashboard.length; i++) {
        support_dashboard[i].classList.add("bg-warning");
        support_dashboard[i].classList.remove("bg-transparent");
    }
}