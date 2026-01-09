import streamlit as st
import requests
from datetime import datetime

# ----------------- Config -----------------
api_key = '30d4741c779ba94c470ca1f63045390a'

# Weather emojis
weather_emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Dust": "🌪️",
    "Fog": "🌫️",
    "Sand": "🏜️",
    "Ash": "🌋",
    "Squall": "💨",
    "Tornado": "🌪️"
}

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️")
st.title("🌤️ Weather Dashboard")
st.write("Get current weather information for any city!")

# Temperature unit selection
unit = st.radio("Select temperature unit:", ("Fahrenheit", "Celsius"))

# Input city
city = st.text_input("Enter city:")

# Session state for recent searches
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------- Fetch Weather -----------------
if city:
    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": city.strip(),
                "units": "imperial",  # Start with Fahrenheit
                "appid": api_key
            }
        )
        data = response.json()

        if response.status_code == 404:
            st.error(f"No city found with the name '{city}'.")
        elif response.status_code != 200:
            st.error(f"Error fetching data: {data.get('message', 'Unknown error')}")
        else:
            # Save to search history
            if city.title() not in st.session_state.history:
                st.session_state.history.append(city.title())

            weather = data['weather'][0]['main']
            description = data['weather'][0]['description'].capitalize()
            temp_f = round(data['main']['temp'])
            temp_c = round((temp_f - 32) * 5/9)
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            emoji = weather_emojis.get(weather, "")
            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            dt = datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')

            # Layout
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(icon_url, width=100)
                st.markdown(f"<h1 style='font-size:50px'>{emoji}</h1>", unsafe_allow_html=True)
            with col2:
                st.subheader(f"{city.title()} Weather")
                st.write(f"**Condition:** {weather} - {description}")
                temp_display = f"{temp_f}°F" if unit == "Fahrenheit" else f"{temp_c}°C"
                st.metric(label="Temperature", value=temp_display)
                st.write(f"**Humidity:** {humidity}%")
                st.write(f"**Wind Speed:** {wind_speed} mph")
                st.write(f"**Last Updated:** {dt}")

            st.markdown("---")
            st.write("**Recent Searches:**", ", ".join(st.session_state.history))

    except requests.exceptions.RequestException as e:
        st.error(f"Network error occurred: {e}")
