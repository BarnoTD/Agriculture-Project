document.addEventListener('DOMContentLoaded', function () {
    const card = document.querySelector(".card-visible");
    const form = document.querySelector("form");
    const plantInput = document.querySelector(".form-select.w-100");
    const dateInput = document.querySelector(".form-control.w-100");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        try {
            // Replace 'http://localhost:8000' with the actual URL of your FastAPI server
            const response = await fetch(`http://localhost:8000/available_suggestions/?crop_name=${plantInput.value}&date=${dateInput.value}`);
            const result = await response.json();

            if (response.ok) {
                const sugg = result[0]
                displayInfo(card, plantInput.value, dateInput.value, result[0].proposal, result[0].periodname);
            } else if (response.status === 404) {
                // Display a custom message for 404 (Not Found)
                displayError(card, "عذرا، ليس لدينا اقتراحات للمحصول بتلك الفترة");
            } else {
                // Display a generic error message
                displayError(card, "حصل خطأ، الرجاء الإعادة لاحقا");
            }

            // Display the response in the console or update the UI as needed
            console.log(result[0].proposal);
            console.log(dateInput.value);

        } catch (error) {
            console.error('Error:', error);
            displayError(card, "حصل خطأ، الرجاء الإعادة لاحقا");
        }
    });
});
function displayError(card, errorMessage) {
    card.textContent = '';
    card.classList.add("d-none");

    const errorDisplay = document.createElement('p');
    errorDisplay.textContent = errorMessage;

    // Add text-align style to center the text
    errorDisplay.style.textAlign = 'center';

    card.appendChild(errorDisplay);
    card.classList.remove("d-none");
}

function displayInfo(card, plantInput, dateInput, suggestions, period_name) {
    card.textContent = '';
    // Explicitly add the 'd-none' class to ensure the card is hidden
    card.classList.add("d-none");

    const messageDisplay = document.createElement('p');

    messageDisplay.textContent = ` لقد قمتم بطلب اقتراح نشاط فلاحي يخص ${plantInput} بتاريخ ${dateInput}`;

    messageDisplay.style.textAlign = 'center';
    card.appendChild(messageDisplay);
    void card.offsetWidth;

    const suggestionDisplay = document.createElement('p');
    suggestionDisplay.textContent = `التاريخ المذكور يقع بفترة ${period_name} ومن المستحسن في تلك الفترة  ${suggestions}`;
    // Add text-align style to center the text
    suggestionDisplay.style.textAlign = 'center';
    card.appendChild(suggestionDisplay);

    // Remove the 'd-none' class after setting the content
    card.classList.remove("d-none");
}