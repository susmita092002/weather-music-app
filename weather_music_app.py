import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
from pytube import Search
import random

# 🌟 Page Configuration
st.set_page_config(page_title="Desi Travel Beats", page_icon="🎵", layout="wide")

# 🎨 Custom CSS
st.markdown("""
    <style>
        body { background-color: #0D0D0D; color: #E6E6FA; font-family: Arial, sans-serif; }
        .stApp { background-color: #0D0D0D; }
        h1, h2 { color: #FF1493; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 🎶 Weather-based song dictionary
weather_songs = {
    "Clear": ["Sunshine Lofi", "Aaj Blue Hai Pani Pani", "Suraj Hua Maddham"],
    "Clouds": ["Megha Re Megha", "Kaise Bhulenge", "Rimjhim Gire Sawan"],
    "Rain": ["Barso Re", "Saawan Aaya Hai", "Tip Tip Barsa Pani"],
    "Thunderstorm": ["Bijli Bijli", "Toofan", "Electric Feel"],
    "Drizzle": ["Aankhon Ke Saagar", "Zara Zara", "Saudagar Saawan"],
    "Snow": ["Ye Haseen Vadiyan", "Chanda Chamke", "Naina Lagiyan Barishan"],
    "Fog": ["Tum Mile", "Ae Ajnabi", "Tera Hone Laga Hoon"]
}

# ☁️ Function to fetch weather data
def get_weather(city):
    api_key = "36827c1692ac6f8f3041af7f869929f5"  # Replace with your OpenWeather API Key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response["cod"] == 200:
        return {
            "temp": response["main"]["temp"],
            "condition": response["weather"][0]["main"],
            "icon": response["weather"][0]["icon"]
        }
    return None

# 🔎 Function to search YouTube for a song
def get_youtube_url(song_name):
    try:
        search = Search(song_name + " song")
        first_result = search.results[0]  # Get first result
        return f"https://www.youtube.com/embed/{first_result.video_id}"
    except Exception:
        return None

# 🚀 Initialize session state
if "weather_condition" not in st.session_state:
    st.session_state.weather_condition = "Clear"

# 🎤 UI Layout
st.title("🎶 Desi Travel Beats 🎶")
st.subheader("Find your weather & get music vibes! 🌍🎵")

# 📍 User Input for City Name
city = st.text_input("Enter the city name:", "Kolkata")

if st.button("Search"):
    weather_data = get_weather(city)
    if weather_data:
        st.session_state.weather_condition = weather_data["condition"]
        st.session_state.weather_data = weather_data
    else:
        st.error("Weather data not found. Please check the city name.")

# Display weather details & suggest song
if "weather_data" in st.session_state:
    weather_data = st.session_state.weather_data
    st.markdown(f"### 🌡️ {weather_data['temp']}°C | {st.session_state.weather_condition}")
    st.image(f"http://openweathermap.org/img/wn/{weather_data['icon']}.png", width=100)

    # Pick a random song based on weather
    suggested_song = random.choice(weather_songs.get(st.session_state.weather_condition, ["No song available"]))
    st.markdown(f"**🎵 Suggested Song: {suggested_song}**")

    # Get YouTube video URL
    youtube_url = get_youtube_url(suggested_song)
    if youtube_url:
        st.markdown(f"""
            <iframe width="100%" height="300" src="{youtube_url}" 
            frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    else:
        st.warning("Could not load the song video.")

# 🎊 Footer
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #FF1493;'>Enjoy Your Journey with Music & Weather Updates! 🚀</h3>", unsafe_allow_html=True)
