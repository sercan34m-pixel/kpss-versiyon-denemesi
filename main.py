import flet as ft
import random
import time
import threading

# =============================================================================
# SORU BANKASI (Kodun İçine Gömülü)
# =============================================================================
TUM_SORULAR = [
    {
        "soru": "Türkiye'nin en doğusu ile en batısı arasında kaç dakikalık zaman farkı vardır?",
        "siklar": ["A) 60", "B) 76", "C) 45", "D) 90", "E) 30"],
        "dogru": "B",
        "konu": "Coğrafi Konum",
        "aciklama": "19 meridyen x 4 dakika = 76 dakika."
    },
    {
        "soru": "Hangisi Türkiye'de dağların kıyıya paralel uzanmasının sonucudur?",
        "siklar": ["A) Koy ve körfez azdır", "B) Ulaşım kolaydır", "C) İklim içlere sokulur", "D) Kıta sahanlığı geniştir", "E) Delta ovası kolay oluşur"],
        "dogru": "A",
        "konu": "Yerşekilleri",
        "aciklama": "Dağlar paralel olunca kıyı düzleşir, girinti çıkıntı (koy) azalır."
    },
    {
        "soru": "En fazla yağış alan ilimiz hangisidir?",
        "siklar": ["A) Trabzon", "B) Antalya", "C) Rize", "D) Muğla", "E) Zonguldak"],
        "dogru": "C",
        "konu": "İklim",
        "aciklama": "Rize, Türkiye'nin yağış şampiyonudur."
    }
]

def main(page: ft.Page):
    # --- AYARLAR ---
    page.title = "KPSS PRO"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F0F4F8"
    page.padding = 20
    page.scroll = "AUTO" # Kaydırma özelliği eklendi

    # --- OYUN DEĞİŞKENLERİ ---
    state = {
        "index": 0,
        "dogru": 0,
        "aktif_sorular": [],
        "cevaplandi": False
    }

    # --- SAYFALAR ---
    
    def oyunu_baslat(e):
        state["aktif_sorular"] = random.sample(TUM_SORULAR, len(TUM_SORULAR))
        state["index"] = 0
        state["dogru"] = 0
        soru_goster()

    def soru_goster():
        page.clean()
        
        # Sorular bitti mi?
        if state["index"] >= len(state["aktif_sorular"]):
            page.add(
                ft.Column([
                    ft.Icon("emoji_events", size=80, color="purple"),
                    ft.Text("TEST BİTTİ", size=30, weight="bold", color="black"),
                    ft.Text(f"Doğru Sayısı: {state['dogru']}", size=20, color="green"),
                    ft.Container(height=20),
                    ft.ElevatedButton("Başa Dön", on_click=lambda e: ana_sayfa())
                ], alignment="center", horizontal_alignment="center")
            )
            page.update()
            return

        soru = state["aktif_sorular"][state["index"]]
        state["cevaplandi"] = False

        # Soru Kartı
        page.add(
            ft.Container(
                content=ft.Text(soru["soru"], size=18, weight="bold", text_align="center", color="black"),
                padding=20, bgcolor="white", border_radius=15
            )
        )

        # Şıklar
        for sik in soru["siklar"]:
            page.add(
                ft.ElevatedButton(
                    text=sik,
                    width=350,
                    bgcolor="white",
                    color="black",
                    on_click=lambda e, s=sik: cevap_kontrol(e, s, soru)
                )
            )
        page.update()

    def cevap_kontrol(e, secilen, soru_data):
        if state["cevaplandi"]: return
        state["cevaplandi"] = True
        
        dogru_mu = soru_data["dogru"] in secilen
        if dogru_mu:
            e.control.bgcolor = "green"
            e.control.color = "white"
            state["dogru"] += 1
        else:
            e.control.bgcolor = "red"
            e.control.color = "white"
        e.control.update()
        
        # Güvenli geçiş (Threading yerine sayfa güncellemesi ile)
        page.update()
        time.sleep(1)
        state["index"] += 1
        soru_goster()

    def ana_sayfa():
        page.clean()
        page.add(
            ft.SafeArea(
                ft.Column([
                    ft.Icon("map", size=80, color="purple"),
                    ft.Text("KPSS 2026", size=30, weight="bold", color="purple"),
                    ft.Text("COĞRAFYA", size=40, weight="heavy", color="black"),
                    ft.Container(height=50),
                    
                    # Sistem Hazır İkonu
                    ft.Row([ft.Icon("check_circle", color="green"), ft.Text("Sistem Hazır (v0.22.1)", color="green")], alignment="center"),
                    
                    ft.Container(height=20),
                    
                    ft.ElevatedButton(
                        "TESTE BAŞLA", 
                        on_click=oyunu_baslat,
                        bgcolor="purple", color="white", width=250, height=60
                    )
                ], alignment="center", horizontal_alignment="center")
            )
        )
        page.update()

    # Uygulamayı başlat
    ana_sayfa()

if __name__ == "__main__":
    ft.app(target=main)