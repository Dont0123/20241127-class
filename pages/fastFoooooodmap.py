import streamlit as st
import folium
import requests
import geopy
from geopy.distance import geodesic
import streamlit_folium
from streamlit_folium import st_folium

# GeoJSON 檔案連結
geojson_url = "https://raw.githubusercontent.com/Dont0123/Dont123/refs/heads/main/MCDdata.geojson"

# 創建 Leafmap 地圖，使用 folium 库來處理點擊事件
m = folium.Map(location=[23.8, 121], zoom_start=7)

try:
    response = requests.get(geojson_url)
    geojson_data = response.json()
    folium.GeoJson(geojson_data).add_to(m)
    st.success("GeoJSON 檔案加載成功！")
except Exception as e:
    st.error(f"無法加載 GeoJSON 檔案：{e}")

# 創建一個點擊事件處理函數，這樣可以捕捉地圖的點擊位置
def on_map_click(event):
    lat = event.latlng[0]
    lon = event.latlng[1]
    st.write(f"您點擊的位置是：經度 {lon}, 緯度 {lat}")

# 設置 Folium 的點擊事件監聽
m.add_child(folium.ClickForMarker(popup="Clicked here!").add_to(m))

# 顯示地圖
output = st_folium(m, width=725)

# 顯示更新後的地圖
st_folium(m, width=725)
