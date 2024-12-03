import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("AQI 地圖")

aqi_data = [
    {"city": "台北", "latitude": 25.0330, "longitude": 121.5654, "AQI": 85},
    {"city": "台中", "latitude": 24.1477, "longitude": 120.6736, "AQI": 120},
    {"city": "高雄", "latitude": 22.6273, "longitude": 120.3014, "AQI": 140},
    {"city": "新竹", "latitude": 24.8066, "longitude": 120.9686, "AQI": 70},
    {"city": "花蓮", "latitude": 23.9872, "longitude": 121.6016, "AQI": 50},
]

m = leafmap.Map(center=(23.8, 121), zoom=7)

for data in aqi_data:
    color = "green" if data["AQI"] <= 50 else "orange" if data["AQI"] <= 100 else "red"
    m.add_circle_marker(
        location=(data["latitude"], data["longitude"]),
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{data['city']} AQI: {data['AQI']}",
    )

m.to_streamlit(height=600)

st.header("AQI 數據表")
st.table(aqi_data)

