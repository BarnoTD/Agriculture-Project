document.addEventListener('DOMContentLoaded', function () {
    const card = document.querySelector(".card-visible");
    const form = document.querySelector("form");
    const plantInput = document.querySelector(".form-select.w-100");
    const dateInput = document.querySelector(".form-control.w-100");

    form.addEventListener("submit", function (event) {
        event.preventDefault();
        displayInfo(card, plantInput.value, dateInput.value);
    });
});

function displayInfo(card, plantInput, dateInput) {
    card.textContent = '';
    // Explicitly add the 'd-none' class to ensure the card is hidden
    card.classList.add("d-none");

    let plantInputArabic = '';

    switch (plantInput) {
        case "olive":
            plantInputArabic = 'أشجار الزيتون';
            break;
        case "tomatoes":
            plantInputArabic = 'الطماطم';
            break;
        case "potatoes":
            plantInputArabic = 'البطاطا';
            break;
        case "peppers":
            plantInputArabic = 'الفلفل';
            break;

        default:
            break;
    }

    const messageDisplay = document.createElement('p');

    messageDisplay.textContent = ` لقد قمتم بطلب اقتراح نشاط فلاحي يخص ${plantInputArabic} بتاريخ ${dateInput}`;

    card.appendChild(messageDisplay);
    // Remove the 'd-none' class after setting the content
    card.classList.remove("d-none");
}
