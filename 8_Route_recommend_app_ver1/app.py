import streamlit as st
from park_data import PARKS
from streamlit_js_eval import get_grolocation

st.title("Route recommend")

#location getting
location = get_geolocation

if location is None:
    st.waring("getting geo location...")
    
else:
    lat_now = location["coords"]["latitude"]
    lon_now = location["coords"]["longitude"]
    st.success(f"現在位置取得: {lat_now}, {lon_now}")
    
    # 各公園へのルート取得と情報収集
    park_routes = []
    for park in PARKS:
        route_json = get_walking_route(lat_now, lon_now, park["lat"], park["lon"])
        route_info = get_route_info(route_json)
        route_info["name"] = park["name"]
        park_routes.append(route_info)

    # 所要時間が短い順にソート
    best_routes = sorted(park_routes, key=lambda x: x["duration"])[:3]

    for route in best_routes:
        st.subheader(f"{route['name']}までの徒歩ルート")
        st.write(f"所要時間: {route['duration']:.1f} 分 / 距離: {route['distance']:.2f} km")
        draw_route(route["geometry"])