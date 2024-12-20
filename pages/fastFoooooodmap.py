import streamlit as st
import leafmap.foliumap as leafmap
import requests
from geopy.distance import geodesic

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

# 創建 Leafmap 地圖
m = leafmap.Map(center=(23.8, 121), zoom=7)

# 加載 GeoJSON 資料
try:
    response = requests.get(geojson_url)
    geojson_data = response.json()
    m.add_geojson(geojson_data, layer_name="GeoJSON Data")
    st.success("GeoJSON 檔案加載成功！")
except Exception as e:
    st.error(f"無法加載 GeoJSON 檔案：{e}")

# 用戶點擊地圖
click_location = None

# 點擊地圖並返回經緯度
with st.expander("點擊地圖查看周圍 500 公尺的點"):
    click_location = m.get_click_coordinates()

# 如果用戶點擊了地圖
if click_location:
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
        m.add_geojson({'type': 'FeatureCollection', 'features': nearby_points}, layer_name="Nearby Points")
    else:
        st.write("周圍 500 公尺內沒有找到任何點。")

# 顯示地圖
m.to_streamlit(height=600)

