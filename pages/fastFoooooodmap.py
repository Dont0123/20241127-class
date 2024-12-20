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
    
    # 計算周圍 500 公尺的所有點
    nearby_points = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            point = feature['geometry']['coordinates']
            point_coords = (point[1], point[0])  # (lat, lon)
            
            # 計算距離
            distance = geodesic((lat, lon), point_coords).meters
            if distance <= 500:
                # 將符合條件的點加入 nearby_points 列表
                nearby_points.append({
                    "名稱": feature.get('properties', {}).get('name', '無名稱'),
                    "經度": point[0],
                    "緯度": point[1],
                    "距離(公尺)": round(distance, 2)
                })
    
    # 顯示周圍 500 公尺的所有點
    if nearby_points:
        st.write(f"找到 {len(nearby_points)} 個點在500公尺範圍內。")
        # 使用 Pandas 顯示表格
        df = pd.DataFrame(nearby_points)
        st.dataframe(df)
    else:
        st.write("周圍 500 公尺內沒有找到任何點。")

# 設置 Folium 的點擊事件監聽
m.add_child(folium.ClickForMarker(popup="Clicked here!").add_to(m))

# 顯示地圖
output = st_folium(m, width=725)

# 顯示更新後的地圖
st_folium(m, width=725)

