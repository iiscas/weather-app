const form = document.getElementById("search-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const city = document.getElementById("city").value;
    const apiUrl = `/api/forecast/${city}/`;

    try {
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            displayResult(data);
        } else {
            resultDiv.innerHTML = `<p style="color: red;">City not found.</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error fetching data. Try again later.</p>`;
    }
});

function displayResult(data) {
    resultDiv.innerHTML = `
        <h3>Weather in ${data.city}</h3>
        <p>Temperature: ${data.temperature}°C</p>
        <p>Description: ${data.description}</p>
    `;
}
