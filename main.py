import tkinter as tk
import folium
import webview
import json
from folium.plugins import MeasureControl

def run_script1():
    import json
    import tkinter as tk
    from tkinter import messagebox, ttk
    from PIL import Image, ImageTk

    # تحميل بيانات GeoJSON للحصول على جميع العناوين المتاحة
    def load_geojson_addresses(geojson_file):
        with open(geojson_file, "r", encoding="utf-8") as file:
            geojson_data = json.load(file)
        return list({feature["properties"].get("address", "") for feature in geojson_data.get("features", []) if
                     "properties" in feature})

    # البحث عن البيانات وإظهار التفاصيل وحفظها في ملف جديد
    def filter_geojson_by_address(input_geojson_file, output_geojson_file, target_address):
        with open(input_geojson_file, "r", encoding="utf-8") as file:
            geojson_data = json.load(file)

        matching_features = [
            feature for feature in geojson_data.get("features", [])
            if "properties" in feature and feature["properties"].get("address") == target_address
        ]

        if not matching_features:
            messagebox.showwarning("نتيجة البحث", "لم يتم العثور على أي بيانات مطابقة.")
            details_label.config(text="")
            return

        filtered_geojson = {
            "type": "FeatureCollection",
            "features": matching_features
        }

        with open(output_geojson_file, "w", encoding="utf-8") as file:
            json.dump(filtered_geojson, file, ensure_ascii=False, indent=4)

        # استخراج التفاصيل وعرضها
        properties = matching_features[0]["properties"]
        plot_no = properties.get("plot_no", "غير متوفر")
        block = properties.get("block", "غير متوفر")
        area = properties.get("area", "غير متوفر")
        details_label.config(text=f"رقم القطعة: {plot_no}\nالمربع: {block}\nالمساحة: {area}")

        messagebox.showinfo("تم الحفظ",
                            f"تم العثور على {len(matching_features)} عنصر(عناصر) وحفظها في {output_geojson_file}")

    # تحديث قائمة الإكمال التلقائي
    def update_autocomplete(event):
        input_text = address_entry.get().lower()
        matching_addresses = [addr for addr in addresses if addr.lower().startswith(input_text)]
        address_combobox["values"] = matching_addresses

    # عند اختيار عنصر من القائمة المنسدلة، يتم إدخاله تلقائيًا في مربع النص
    def on_combobox_select(event):
        selected_address = address_combobox.get()
        address_entry.delete(0, tk.END)
        address_entry.insert(0, selected_address)

    # عند الضغط على زر البحث
    def search_and_save():
        selected_address = address_entry.get()
        if not selected_address:
            messagebox.showwarning("تحذير", "الرجاء إدخال عنوان صحيح!")
            return
        filter_geojson_by_address(input_geojson, output_geojson, selected_address)

    # مسارات الملفات
    input_geojson = "bader with address.geojson"
    output_geojson = "select bader.geojson"

    # تحميل جميع العناوين المتاحة
    addresses = load_geojson_addresses(input_geojson)

    # إنشاء واجهة Tkinter
    root = tk.Tk()
    root.title("ارشيف ادارة المساحة ")
    # حساب موضع منتصف الشاشة
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # حساب موقع النافذة لكي تكون في منتصف الشاشة
    x = (screen_width // 2) - (600 // 2)
    y = (screen_height // 2) - (400 // 2)

    # تحديد موقع النافذة
    root.geometry(f"600x400+{x}+{y}")

    # إضافة عنوان
    tk.Label(root, text="أدخل العنوان:", font=("Arial", 12)).pack(pady=10)

    # مربع الإدخال مع خاصية الإكمال التلقائي
    address_entry = tk.Entry(root, font=("Arial", 12))
    address_entry.pack(pady=5)
    address_entry.bind("<KeyRelease>", update_autocomplete)

    # قائمة منسدلة لعرض الاقتراحات
    address_combobox = ttk.Combobox(root, font=("Arial", 12))
    address_combobox.pack(pady=5)
    address_combobox.bind("<<ComboboxSelected>>", on_combobox_select)

    # زر البحث
    search_button = tk.Button(root, text="بحث", font=("Arial", 12), command=search_and_save)
    search_button.pack(pady=10)

    # مساحة عرض تفاصيل الطبقة
    details_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
    details_label.pack(pady=10)

    # تشغيل الواجهة
    root.mainloop()
def run_script2():
    #subprocess.run(["python", "gejeson to map .py"])
    import folium
    import json
    import webbrowser
    from shapely.geometry import Polygon, MultiPolygon
    from folium.plugins import MeasureControl

    def create_map():
        """إنشاء الخريطة بموقع افتراضي مع إضافة أداة قياس."""
        m = folium.Map(location=[19.569941, 37.206855], zoom_start=30, control_scale=True)

        # إضافة طبقات Google
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google Satellite",
            name="Google Satellite",
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google Maps",
            name="Google Maps",
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
            attr="Google Terrain",
            name="Google Terrain",
        ).add_to(m)

        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attr="Google Hybrid",
            name="Google Hybrid",
        ).add_to(m)

        # إضافة أداة القياس
        m.add_child(MeasureControl(primary_length_unit="meters"))

        return m

    def add_gray_geojson1(map_object, file_path, label_field):
        """إضافة طبقة GeoJSON مع طبقة منفصلة لأرقام القطع."""
        with open(file_path, encoding="utf-8") as f:
            geojson_data = json.load(f)

        # إنشاء طبقة للأراضي
        land_layer = folium.FeatureGroup(name="الأراضي").add_to(map_object)

        # إنشاء طبقة منفصلة لأرقام القطع
        label_layer = folium.FeatureGroup(name="أرقام القطع").add_to(map_object)

        def style_function(feature):
            return {
                "fillColor": "#808080",
                "color": "#606060",
                "weight": 1,
                "fillOpacity": 0.3
            }

        folium.GeoJson(
            geojson_data,
            style_function=style_function
        ).add_to(land_layer)  # إضافة الأراضي إلى طبقة الأراضي

        bounds = []  # قائمة لتجميع الإحداثيات

        # إضافة النصوص إلى الطبقة الخاصة بالأرقام
        for feature in geojson_data["features"]:
            properties = feature.get("properties", {})
            label_value = properties.get(label_field, "N/A")  # قيمة النص

            geometry = feature.get("geometry", {})
            if geometry.get("type") == "Polygon":
                coordinates = geometry.get("coordinates", [])
                if coordinates:
                    polygon = Polygon(coordinates[0])  # تحويل إلى مضلع
            elif geometry.get("type") == "MultiPolygon":
                coordinates = geometry.get("coordinates", [])
                if coordinates:
                    polygon = MultiPolygon([Polygon(p[0]) for p in coordinates])  # تحويل إلى مضلعات متعددة
            else:
                print(f"⚠️ نوع غير مدعوم: {geometry.get('type')}")
                continue

            if polygon.is_valid and not polygon.is_empty:
                centroid = polygon.centroid  # حساب مركز المضلع

                folium.Marker(
                    [centroid.y, centroid.x],
                    icon=folium.DivIcon(
                        html=f'<div style="font-size: 14px; color: gold; fgont-weight: bold;">{label_value}</div>'
                    )
                ).add_to(label_layer)  # إضافة الرقم إلى طبقة الأرقام

                bounds.append([centroid.y, centroid.x])  # إضافة الإحداثيات إلى القائمة

        # تحديث الخريطة لعرض جميع العناصر
        if bounds:
            map_object.fit_bounds(bounds)  # ضبط الخريطة لتشمل جميع النقاط

    def add_secondary_geojson(map_object, file_path):
        """إضافة ملف GeoJSON إضافي وعمل زوم له."""
        with open(file_path, encoding="utf-8") as f:
            geojson_data = json.load(f)

        secondary_layer = folium.FeatureGroup(name="الحدود المحددة").add_to(map_object)

        folium.GeoJson(
            geojson_data,
            style_function=lambda feature: {
                "fillColor": "#00ff00",
                "color": "#FF0000",
                "weight": 4,
                "fillOpacity": 0.4
            }
        ).add_to(secondary_layer)

        # استخراج الحدود وضبط الخريطة
        bounds = []
        for feature in geojson_data["features"]:
            geometry = feature.get("geometry", {})
            if geometry.get("type") == "Polygon":
                coordinates = geometry.get("coordinates", [])
                if coordinates:
                    polygon = Polygon(coordinates[0])
            elif geometry.get("type") == "MultiPolygon":
                coordinates = geometry.get("coordinates", [])
                if coordinates:
                    polygon = MultiPolygon([Polygon(p[0]) for p in coordinates])
            else:
                continue

            if polygon.is_valid and not polygon.is_empty:
                bounds.append([polygon.centroid.y, polygon.centroid.x])

        if bounds:
            map_object.fit_bounds(bounds)  # ضبط الخريطة لتحتوي على جميع البيانات

    # إنشاء الخريطة وإضافة البيانات
    map0 = create_map()
    add_gray_geojson1(map0, "bader with address.geojson", "plot_no")  # الحقل الصحيح
    add_secondary_geojson(map0, "select bader.geojson")  # إضافة ملف إضافي

    # إضافة التحكم في الطبقات
    folium.LayerControl().add_to(map0)

    # حفظ وعرض الخريطة
    map0.save("map.html")
    webbrowser.open("map.html")
def run_script3():

    class MapViewer:
        def __init__(self):
            self.map_html = "map.html"
            self.upload_geojson("select bader.geojson")

        def upload_geojson(self, file_path):
            self.create_map(file_path)
            self.show_map()

        def create_map(self, geojson_path):
            m = folium.Map(location=[19.569941, 37.206855], zoom_start=18, max_zoom=23, min_zoom=5, tiles=None)

            # إضافة أنواع Google Maps
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

            m.add_child(MeasureControl(primary_length_unit="meters", secondary_length_unit="kilometers"))

            with open(geojson_path, 'r', encoding='utf-8') as f:
                geojson_data = json.load(f)
                folium.GeoJson(geojson_data, name="GeoJSON Data").add_to(m)

                bounds = self.get_geojson_bounds(geojson_data)
                if bounds:
                    m.fit_bounds(bounds, padding=(10, 10))

            folium.LayerControl().add_to(m)
            m.save(self.map_html)

        def get_geojson_bounds(self, geojson_data):
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
            webview.create_window("الخريطة", self.map_html, width=900, height=900, resizable=True)
            webview.start()

    if __name__ == "__main__":
        app = MapViewer()


# إنشاء النافذة الرئيسية
root = tk.Tk()
root.title("الادارة العامة للمساحة")
# حساب موضع منتصف الشاشة
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# حساب موقع النافذة لكي تكون في منتصف الشاشة
x = (screen_width // 2) - (600 // 2)
y = (screen_height // 2) - (400 // 2)

# تحديد موقع النافذة
root.geometry(f"600x400+{x}+{y}")

# إعداد الأزرار بنفس الهوية البصرية
button1 = tk.Button(
    root,
    text="📁 اختيار القطة",
    command=run_script1,
    font=("Arial", 12),
    bg="#f7941d",   # اللون البرتقالي من الشعار
    fg="white",
    padx=10,
    pady=8,
    bd=0,
    relief="flat",
    cursor="hand2"
)
button1.pack(pady=10)

button2 = tk.Button(
    root,
    text="🗺️ الكروكي",
    command=run_script2,
    font=("Arial", 12),
    bg="#0f1f47",   # أزرق غامق من الشعار
    fg="white",
    padx=10,
    pady=8,
    bd=0,
    relief="flat",
    cursor="hand2"
)
button2.pack(pady=10)

button3 = tk.Button(
    root,
    text="🌍 العرض على الطبيعة",
    command=run_script3,
    font=("Arial", 12),
    bg="#1d8348",   # أخضر هادئ مناسب للطبيعة
    fg="white",
    padx=10,
    pady=8,
    bd=0,
    relief="flat",
    cursor="hand2"
)
button3.pack(pady=10)

# تشغيل النافذة
root.mainloop()
