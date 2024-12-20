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

# 加載 GeoJSON 資料
try:
    response = requests.get(geojson_url)
    geojson_data = response.json()
    folium.GeoJson(geojson_data).add_to(m)
    st.success("GeoJSON 檔案加載成功！")
except Exception as e:
    st.error(f"無法加載 GeoJSON 檔案：{e}")

# 顯示地圖
output = st_folium(m, width=725)

# 如果用戶點擊地圖，獲取點擊位置的經緯度
if output:
    click_location = (output['lat'], output['lon'])
    st.write(f"點擊的地點：{click_location}")

    # 計算周圍 500 公尺的所有點
    nearby_points = []
    for feature in geojson_data['features']:
        # 假設每個點都有 "geometry" 屬性，並且為 "Point"
        if feature['geometry']['type'] == 'Point':
            point = feature['geometry']['coordinates']
            point_coords = (point[1], point[0])  # (lat, lon)
            
            # 計算距離
            distance = geodesic(click_location, point_coords).meters
            if distance <= 500:
                nearby_points.append(feature)
    
    # 顯示周圍 500 公尺的所有點
    if nearby_points:
        st.write(f"找到 {len(nearby_points)} 個點在500公尺範圍內。")
        # 將篩選出的點顯示在地圖上
        folium.GeoJson({'type': 'FeatureCollection', 'features': nearby_points}).add_to(m)
    else:
        st.write("周圍 500 公尺內沒有找到任何點。")

    # 顯示更新後的地圖
    st_folium(m, width=725)
