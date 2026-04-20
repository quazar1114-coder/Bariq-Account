import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import flet as ft
from datetime import datetime, timedelta
from ummalqura.hijri_date import HijriDate

def main(page: ft.Page):
    # إعدادات الصفحة الأساسية للتطبيق
    page.title = "حساب بلاد بارق - الأستاذ محمد عامر البارقي"
    page.rtl = True
    page.horizontal_alignment = "center"
    page.scroll = "auto"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # التاريخ الحالي عند فتح التطبيق
    current_date = datetime.now()

    # --- مصفوفة البيانات (حساب بلاد بارق) بناءً على جدولك الزراعي ---
    seasons_data = {
        "الصيف": [
            {"n": "الشرطين", "a": "بداية جمعة الصيف"}, 
            {"n": "البطين", "a": ""}, 
            {"n": "الثريا", "a": ""},
            {"n": "التابع", "a": "بداية الفيحا - الاستعداد للموسم الزراعي"},
            {"n": "الهقعة", "a": "مناسبة لزراعة جميع الحبوب و الدخن التهامي"},
            {"n": "الهنعة", "a": "مناسبة لزراعة جميع الحبوب و الدخن التهامي"},
            {"n": "الذراع (المرزم)", "a": "أفضل أوقات الزراعة قبل وقوف الشمس\nزراعة البجيدة و الدخن و الجلجلان"}
        ],
        "الخريف": [
            {"n": "الناب", "a": "زراعة البجيدة و الدخن و الجلجلان"},
            {"n": "الطرف", "a": "بداية علان (فياح) - مناسب لزراعة جميع أنواع الحبوب"},
            {"n": "الجباه", "a": "مناسب لزراعة جميع أنواع الحبوب"},
            {"n": "الزبر", "a": "مناسب لزراعة جميع أنواع الحبوب"},
            {"n": "الصرفة", "a": "بداية أبو شتية - مناسب لزراعة جميع أنواع الحبوب"},
            {"n": "العواء", "a": "الدخن العفيطي و الزعر و البجيدة و الجلجلان"},
            {"n": "السماك", "a": "الدخن العفيطي و الزعر و البجيدة و الجلجلان"}
        ],
        "الشتاء": [
            {"n": "الغفر", "a": ""}, {"n": "الزبانا", "a": ""},
            {"n": "الإكليل", "a": "مناسب لزراعة الذرة البيضاء و الزعر و الجلجلان (قصير) و الدخن العفيطي"},
            {"n": "القلب", "a": "مناسب لزراعة الذرة البيضاء و الزعر و الجلجلان (قصير) و الدخن العفيطي"},
            {"n": "الشولة", "a": "مناسب لزراعة الذرة البيضاء و الزعر و الجلجلان (قصير) و الدخن العفيطي"},
            {"n": "النعائم", "a": ""}, {"n": "البلدة", "a": ""}
        ],
        "الربيع": [
            {"n": "سعد الذابح", "a": ""}, {"n": "سعد بلع", "a": ""}, {"n": "سعد السعود", "a": ""},
            {"n": "سعد الأخبية", "a": ""}, {"n": "الفرع المقدم", "a": ""}, {"n": "الفرع المؤخر", "a": ""},
            {"n": "الحوت ( الرشا)", "a": ""}
        ]
    }

    def get_local(name):
        fayha = ["التابع", "الهقعة", "الهنعة", "الذراع (المرزم)", "الناب"]
        alan = ["الطرف", "الجباه", "الزبر"]
        abu_shatya = ["الصرفة", "العواء", "السماك"]
        if name in fayha: return "الفيحا"
        if name in alan: return "علان"
        if name in abu_shatya: return "أبو شتية"
        return ""

    def get_rain(name):
        ghasaq = ["الفرع المقدم", "الفرع المؤخر", "الحوت ( الرشا)", "الشرطين", "البطين", "الثريا"]
        fayha = ["الهقعة", "الهنعة", "الذراع (المرزم)", "الناب"]
        raddad = ["الطرف", "الجباه", "الزبر"]
        akhir = ["الصرفة", "العواء", "السماك"]
        shita = ["الغفر", "الزبانا", "الإكليل", "القلب", "الشولة", "النعائم", "البلدة"]
        rabia = ["سعد الذابح", "سعد بلع", "سعد السعود", "سعد الأخبية"]
        if name in ghasaq: return "أمطار الغسق"
        if name in fayha: return "أمطار الفيحا"
        if name in raddad: return "أمطار رداد الخريف"
        if name in akhir: return "أمطار آخر الخريف"
        if name in shita: return "أمطار الشتاء"
        if name in rabia: return "أمطار الربيع"
        return ""

    def update_ui():
        year = current_date.year
        starts = {}
        # حساب الفصول وتصحيح الجمعة (جمعة الصيف)
        for n in ["الصيف", "الخريف", "الشتاء", "الربيع"]:
            base = {"الصيف": (3, 20), "الخريف": (6, 19), "الشتاء": (9, 18), "الربيع": (12, 18)}
            y_check = year if n != "الربيع" or current_date.month > 3 else year - 1
            dt = datetime(y_check, base[n][0], base[n][1])
            off = (4 - dt.weekday()) % 7
            if off > 3: off -= 7
            orig_f = dt + timedelta(days=off)
            
            start_dt, is_leap = orig_f, False
            if n == "الصيف" and orig_f.month == 3 and orig_f.day == 17:
                start_dt, is_leap = orig_f + timedelta(days=7), True
            starts[n] = {"start": start_dt, "is_leap": is_leap, "orig_f": orig_f}

        active_n = "الربيع"
        for n, data in sorted(starts.items(), key=lambda x: x[1]["start"]):
            if current_date >= data["start"]: active_n = n

        cur_data = starts[active_n]
        diff = (current_date - cur_data["start"]).days
        
        h = HijriDate(current_date.year, current_date.month, current_date.day, gr=True)
        txt_dates.value = f"ميلادي: {current_date.strftime('%Y/%m/%d')} م | هجري: {int(h.day)} {h.month_name} {int(h.year)}"
        txt_day.value = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"][current_date.weekday()]

        summer = starts["الصيف"]
        if summer["is_leap"] and summer["orig_f"] <= current_date < summer["start"]:
            txt_skip.value = "⚠️ الأسبوع الساقط (تصحيح الحساب)"
            txt_star.value = "نجم: --"
            txt_local.value = ""; txt_rain.value = ""; txt_agri.value = "فترة انتقالية"
        else:
            txt_skip.value = ""
            idx = min(max(0, diff // 13), 6)
            star = seasons_data[active_n][idx]
            txt_star.value = f"نجم: {(diff % 13) + 1:02d}/13 - {star['n']}"
            txt_local.value = f"التسمية: {get_local(star['n'])}"
            txt_rain.value = f"الحالة: {get_rain(star['n'])}"
            txt_agri.value = f"الزراعة: {star['a']}" if star['a'] else ""

        txt_season_info.value = f"الموسم: {active_n} (اليوم {diff+1})"
        page.update()

    def adjust(v, u):
        nonlocal current_date
        d = {"d": 1, "w": 7, "m": 30, "y": 365}
        current_date += timedelta(days=v * d[u])
        update_ui()

    # --- التصميم ---
    header = ft.Container(
        content=ft.Text("حساب بلاد بارق الزراعي", size=22, color="white", weight="bold"),
        bgcolor="#2e7d32", padding=15, border_radius=10, alignment=ft.alignment.center, width=400
    )

    card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                txt_day := ft.Text("", size=40, weight="bold", color="#1b5e20"),
                txt_dates := ft.Text("", size=16, color="grey"),
                txt_skip := ft.Text("", size=14, color="red"),
                ft.Divider(height=10),
                txt_star := ft.Text("", size=22, weight="bold"),
                txt_local := ft.Text("", size=20, color="#d84315", weight="bold"),
                txt_rain := ft.Text("", size=18, color="#0277bd"),
                txt_agri := ft.Text("", size=16, text_align="center", color="#388e3c"),
                ft.Divider(),
                txt_season_info := ft.Text("", size=14, italic=True),
            ], horizontal_alignment="center"),
            padding=20
        ), width=400
    )

    def btn_col(l, u):
        return ft.Column([
            ft.ElevatedButton("+", on_click=lambda _: adjust(1, u), width=60),
            ft.Text(l, size=12),
            ft.ElevatedButton("-", on_click=lambda _: adjust(-1, u), width=60),
        ], horizontal_alignment="center", spacing=5)

    page.add(
        header, card,
        ft.Row([btn_col("يوم", "d"), btn_col("أسبوع", "w"), btn_col("شهر", "m"), btn_col("سنة", "y")], 
               alignment="center"),
        ft.Text("تصميم وبرمجة الأستاذ محمد عامر البارقي", size=10, color="grey")
    )
    update_ui()

if __name__ == "__main__":
    ft.app(target=main)
