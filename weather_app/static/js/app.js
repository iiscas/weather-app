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
/* 
const canvas = document.getElementById("temperatureChart");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const city = document.getElementById("city").value;
    const apiUrl = `/api/forecast/${city}/`;

    try {
        const response = await fetch(apiUrl);
        if (response.ok) {
            const data = await response.json();
            displayGraph(data.hourly_temperatures);
        } else {
            const errorData = await response.json();
            resultDiv.innerHTML = `<p style="color: red;">${errorData.error}</p>`;  // Exibe a mensagem de erro
        }
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error fetching data: ${error}</p>`;
    }
});
 */

function displayGraph(hourlyTemperatures) {
    const hours = hourlyTemperatures.map(item => item.hour);
    const temperatures = hourlyTemperatures.map(item => item.temperature);

    const ctx = canvas.getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: hours,  // Horas do dia
            datasets: [{
                label: "Temperature (°C)",
                data: temperatures,  // Temperaturas
                borderColor: "rgba(75, 192, 192, 1)",
                backgroundColor: "rgba(75, 192, 192, 0.2)",
                borderWidth: 2,
                tension: 0.4  // Curvatura da linha
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top"
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Hours"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Temperature (°C)"
                    },
                    beginAtZero: true
                }
            }
        }
    });
}
