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

st.title("GeoJSON Viewer with Streamlit")
st.markdown(
    """
    此應用程式使用 [Streamlit](https://streamlit.io) 和 [Leafmap](https://leafmap.org) 加載並顯示 GeoJSON 檔案。  
    你現在加載的是來自 GitHub 的 GeoJSON 檔案。
    """
)

# GeoJSON 檔案連結
geojson_url = "https://raw.githubusercontent.com/Dont0123/Dont123/refs/heads/main/MCDdata.geojson"

m = leafmap.Map(center=(23.8, 121), zoom=7)

for data in aqi_data:
    color = "green" if data["AQI"] <= 50 else "orange" if data["AQI"] <= 100 else "red"
    m.add_marker(
        location=(data["latitude"], data["longitude"]),
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        popup=f"{data['city']} AQI: {data['AQI']}",
    )

m.to_streamlit(height=600)

st.header("AQI data")
st.table(aqi_data)

