import folium
import webview
import json
import tkinter as tk
from tkinter import filedialog
from folium.plugins import MeasureControl  # ✅ إضافة أداة القياس


class MapViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("تحميل ملف GeoJSON وعرضه على Google Maps")
        self.root.geometry("400x200")

        self.upload_button = tk.Button(root, text="اختر ملف GeoJSON", command=self.upload_geojson)
        self.upload_button.pack(pady=20)

        self.map_html = "map.html"

    def upload_geojson(self):
        file_path = filedialog.askopenfilename(filetypes=[("GeoJSON files", "*.geojson")])
        if file_path:
            self.create_map(file_path)
            self.show_map()

    def create_map(self, geojson_path):
        # إنشاء الخريطة باستخدام Google Maps
        m = folium.Map(location=[19.569941, 37.206855], zoom_start=18, max_zoom=23, min_zoom=5, tiles=None)

        # ✅ إضافة Google Maps بأنواعها المختلفة
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google Maps Streets",
            name="Google Streets",
            max_zoom=23
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Google Satellite",
            max_zoom=23
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attr="Google Hybrid",
            name="Google Hybrid",
            max_zoom=23
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
            attr="Google Terrain",
            name="Google Terrain",
            max_zoom=23
        ).add_to(m)

        # ✅ إضافة أداة قياس المسافات
        m.add_child(MeasureControl(primary_length_unit="meters", secondary_length_unit="kilometers"))

        # تحميل ملف GeoJSON وإضافته للخريطة
        with open(geojson_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)
            folium.GeoJson(geojson_data, name="GeoJSON Data").add_to(m)

            # استخراج الحدود وضبط التكبير التلقائي
            bounds = self.get_geojson_bounds(geojson_data)
            if bounds:
                m.fit_bounds(bounds, padding=(10, 10))

        # إضافة زر اختيار نوع الخريطة
        folium.LayerControl().add_to(m)

        # حفظ الخريطة كملف HTML
        m.save(self.map_html)

    def get_geojson_bounds(self, geojson_data):
        """ استخراج الحدود الجغرافية من ملف GeoJSON """
        bounds = []
        if "features" in geojson_data:
            for feature in geojson_data["features"]:
                geometry = feature.get("geometry", {})
                coordinates = geometry.get("coordinates", [])

                if geometry["type"] == "Point":
                    bounds.append(coordinates)
                elif geometry["type"] in ["LineString", "MultiPoint"]:
                    bounds.extend(coordinates)
                elif geometry["type"] in ["Polygon", "MultiLineString"]:
                    for coord in coordinates:
                        bounds.extend(coord)
                elif geometry["type"] == "MultiPolygon":
                    for poly in coordinates:
                        for coord in poly:
                            bounds.extend(coord)

        if bounds:
            min_lat = min(coord[1] for coord in bounds)
            max_lat = max(coord[1] for coord in bounds)
            min_lon = min(coord[0] for coord in bounds)
            max_lon = max(coord[0] for coord in bounds)
            return [[min_lat, min_lon], [max_lat, max_lon]]
        return None

    def show_map(self):
        # ✅ جعل النافذة قابلة للتكبير والتصغير مع أبعاد ابتدائية 900x900
        webview.create_window("الخريطة", self.map_html, width=900, height=900, resizable=True)
        webview.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapViewer(root)
    root.mainloop()
