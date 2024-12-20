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

# 點擊地圖後顯示經緯度
st.write("點擊地圖選擇位置")

# 用 st_folium 顯示地圖
output = st_folium(m, width=725)

# 確認是否有返回點擊的經緯度
if output and 'lat' in output and 'lon' in output:
    click_lat = output['lat']
    click_lon = output['lon']
    st.write(f"您點擊的位置：經度 {click_lon}, 緯度 {click_lat}")

    # 計算周圍500公尺的所有點
    nearby_points = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            point = feature['geometry']['coordinates']
            point_coords = (point[1], point[0])  # (lat, lon)

            # 計算距離
            distance = geodesic((click_lat, click_lon), point_coords).meters
            if distance <= 500:
                nearby_points.append({
                    "名稱": feature.get('properties', {}).get('name', '無名稱'),
                    "經度": point[0],
                    "緯度": point[1],
                    "距離(公尺)": round(distance, 2)
                })

    # 顯示周圍500公尺的所有點
    if nearby_points:
        st.write(f"找到 {len(nearby_points)} 個點在500公尺範圍內。")
        df = pd.DataFrame(nearby_points)
        st.dataframe(df)
    else:
        st.write("周圍500公尺內沒有找到任何點。")
else:
    st.write("請點擊地圖選擇位置。")
