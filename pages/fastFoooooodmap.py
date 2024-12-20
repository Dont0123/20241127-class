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
    st.success("GeoJSON 文件加载成功！")
except Exception as e:
    st.error(f"无法加载 GeoJSON 文件：{e}")

# 通过 st_folium 显示地图并等待用户点击
output = st_folium(m, width=725)

# 判断用户是否点击了地图
if output:
    if 'lat' in output and 'lon' in output:
        click_lat = output['lat']
        click_lon = output['lon']
        st.write(f"您点击的位置：经度 {click_lon}, 纬度 {click_lat}")

        # 计算周围500米的所有点
        nearby_points = []
        for feature in geojson_data['features']:
            if feature['geometry']['type'] == 'Point':
                point = feature['geometry']['coordinates']
                point_coords = (point[1], point[0])  # (lat, lon)

                # 计算距离
                distance = geodesic((click_lat, click_lon), point_coords).meters
                if distance <= 500:
                    nearby_points.append({
                        "名称": feature.get('properties', {}).get('name', '无名称'),
                        "经度": point[0],
                        "纬度": point[1],
                        "距离(米)": round(distance, 2)
                    })

        # 显示周围500米的所有点
        if nearby_points:
            st.write(f"找到 {len(nearby_points)} 个点在500米范围内。")
            df = pd.DataFrame(nearby_points)
            st.dataframe(df)
        else:
            st.write("周围500米内没有找到任何点。")
    else:
        st.write("请点击地图选择位置。")
