import folium

latitude = 37.7749
longitude = -122.4194
map = folium.Map(location=[latitude, longitude], zoom_start=14)
folium.Marker([latitude, longitude], popup='Current Location').add_to(map)
map.save("map.html")
