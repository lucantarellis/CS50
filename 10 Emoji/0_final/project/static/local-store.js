function updateTotalPrice() {
    var totalPrice = 0;
    var productCards = document.querySelectorAll('.card-prod');
    productCards.forEach(function(card) {
        var input = card.querySelector('input[name="qty"]');
        var price = parseFloat(card.querySelector('input[name="price"]').value);
        var quantity = parseInt(input.value, 10);
        if (isNaN(quantity)) {
            totalPrice = 0;
        } else {
            totalPrice += quantity * price;
        }
    });
    var totalPriceElement = document.getElementById('total-price');
    totalPriceElement.textContent = 'Total: $' + totalPrice.toFixed(2);
}

function increaseCount(event, button) {
    var input = button.previousElementSibling;
    var value = parseInt(input.value, 10);
    if (isNaN(value)) {
        value = 0;
    }
    value++;
    input.value = value;
    updateTotalPrice();
    updateButtonStatus(input);
}

function decreaseCount(event, button) {
    var input = button.nextElementSibling;
    var value = parseInt(input.value, 10);
    if (isNaN(value)) {
        value = 0;
    } else if (value > 0) {
        value--;
    }
    input.value = value;
    updateTotalPrice();
    updateButtonStatus(input);
}

function updateButtonStatus(input) {
    var card = input.closest('.card-prod');
    var minusButton = card.querySelector('.counter a:first-child');

    if (input.value === '0') {
        minusButton.classList.add('disabled');
    } else {
        minusButton.classList.remove('disabled');
    }
}