document.addEventListener("DOMContentLoaded", function () {

    // Search validation
    const searchForm = document.querySelector(".search-form");

    if (searchForm) {

        searchForm.addEventListener("submit", function (event) {

            const input = searchForm.querySelector(
                'input[name="q"]'
            );

            if (input && input.value.trim() === "") {
                event.preventDefault();

                input.focus();

                input.placeholder =
                    "Please enter a product name...";
            }

        });

    }


    // Button ripple effect
    const buttons = document.querySelectorAll(
        ".cart-btn, .checkout-btn, .view-btn, .register-btn"
    );


    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            button.classList.add("clicked");

            setTimeout(function () {

                button.classList.remove("clicked");

            }, 300);

        });

    });


    // Auto hide messages
    const messages = document.querySelectorAll(
        ".message"
    );

    messages.forEach(function (message) {

        setTimeout(function () {

            message.style.opacity = "0";

            setTimeout(function () {
                message.remove();
            }, 500);

        }, 4000);

    });


    // Scroll reveal
    const cards = document.querySelectorAll(
        ".product-card, .order-card"
    );


    cards.forEach(function (card) {

        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";
        card.style.transition =
            "opacity 0.5s ease, transform 0.5s ease";

    });


    setTimeout(function () {

        cards.forEach(function (card, index) {

            setTimeout(function () {

                card.style.opacity = "1";
                card.style.transform = "translateY(0)";

            }, index * 80);

        });

    }, 100);

});