const weatherApi = "https://api.open-meteo.com/v1/forecast";
const cityApi = "https://geocoding-api.open-meteo.com/v1/search";

const cityInput = document.getElementById("cityInput");
const searchButton = document.getElementById("searchButton");
const message = document.getElementById("message");

searchButton.addEventListener("click", getWeather);

cityInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        getWeather();
    }
});

async function getWeather() {
    const city = cityInput.value.trim();

    if (city === "") {
        showMessage("Please enter a city name.");
        return;
    }

    showMessage("Searching for weather...");

    try {
        const cityResponse = await fetch(
            `${cityApi}?name=${encodeURIComponent(city)}&count=1&language=en&format=json`
        );

        if (!cityResponse.ok) {
            throw new Error("Could not search for the city.");
        }

        const cityData = await cityResponse.json();

        if (!cityData.results || cityData.results.length === 0) {
            throw new Error("City not found. Try another city.");
        }

        const location = cityData.results[0];

        const weatherUrl =
            `${weatherApi}?latitude=${location.latitude}` +
            `&longitude=${location.longitude}` +
            `&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m` +
            `&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max` +
            `&timezone=auto&forecast_days=7`;

        const weatherResponse = await fetch(weatherUrl);

        if (!weatherResponse.ok) {
            throw new Error("Weather information could not be loaded.");
        }

        const weatherData = await weatherResponse.json();

        displayCurrentWeather(location, weatherData);
        createForecast(weatherData.daily);
        showMessage("");

    } catch (error) {
        console.error(error);
        showMessage(error.message);
    }
}

function displayCurrentWeather(location, data) {
    const current = data.current;

    document.getElementById("cityName").textContent =
        `${location.name}, ${location.country_code || location.country}`;

    document.getElementById("temperature").textContent =
        Math.round(current.temperature_2m);

    document.getElementById("humidity").textContent =
        `${current.relative_humidity_2m}%`;

    document.getElementById("wind").textContent =
        `${Math.round(current.wind_speed_10m)} km/h`;

    document.getElementById("feelsLike").textContent =
        `${Math.round(current.apparent_temperature)}°C`;

    document.getElementById("rainChance").textContent =
        `${data.daily.precipitation_probability_max[0] ?? 0}%`;

    const weather = getWeatherInfo(current.weather_code);

    document.getElementById("condition").textContent = weather.name;
    document.getElementById("weatherIcon").textContent = weather.icon;

    const date = new Date(current.time);

    document.getElementById("weatherDate").textContent =
        date.toLocaleString("en-IN", {
            weekday: "long",
            day: "numeric",
            month: "long",
            hour: "2-digit",
            minute: "2-digit"
        });
}

function createForecast(daily) {
    const forecast = document.getElementById("forecast");

    forecast.innerHTML = "";

    for (let i = 0; i < daily.time.length; i++) {
        const weather = getWeatherInfo(daily.weather_code[i]);

        const date = new Date(daily.time[i] + "T12:00:00");

        const day = date.toLocaleDateString("en-IN", {
            weekday: "short"
        });

        const card = document.createElement("div");
        card.className = "forecast-card";

        card.innerHTML = `
            <div class="day">${i === 0 ? "Today" : day}</div>
            <div class="icon">${weather.icon}</div>
            <div class="weather-name">${weather.name}</div>

            <div class="temperatures">
                <span class="max">
                    ${Math.round(daily.temperature_2m_max[i])}°
                </span>
                <span class="min">
                    ${Math.round(daily.temperature_2m_min[i])}°
                </span>
            </div>

            <small>
                Rain ${daily.precipitation_probability_max[i] ?? 0}%
            </small>
        `;

        forecast.appendChild(card);
    }
}

function getWeatherInfo(code) {
    const weatherTypes = {
        0: ["Clear Sky", "☀️"],
        1: ["Mainly Clear", "🌤️"],
        2: ["Partly Cloudy", "⛅"],
        3: ["Cloudy", "☁️"],
        45: ["Fog", "🌫️"],
        48: ["Fog", "🌫️"],
        51: ["Light Drizzle", "🌦️"],
        53: ["Drizzle", "🌦️"],
        55: ["Heavy Drizzle", "🌧️"],
        61: ["Light Rain", "🌦️"],
        63: ["Rain", "🌧️"],
        65: ["Heavy Rain", "🌧️"],
        71: ["Light Snow", "🌨️"],
        73: ["Snow", "❄️"],
        75: ["Heavy Snow", "❄️"],
        80: ["Rain Showers", "🌦️"],
        81: ["Rain Showers", "🌧️"],
        82: ["Heavy Rain", "⛈️"],
        95: ["Thunderstorm", "⛈️"],
        96: ["Thunderstorm", "⛈️"],
        99: ["Thunderstorm", "⛈️"]
    };

    const result = weatherTypes[code];

    return result
        ? { name: result[0], icon: result[1] }
        : { name: "Unknown", icon: "🌤️" };
}

function showMessage(text) {
    message.textContent = text;
}
