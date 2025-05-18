import tkinter as tk
from tkinter import messagebox, ttk
import uuid

# --- Sınıflar ---

class Urun:
    def __init__(self, ad, fiyat, stok, hazirlama_suresi=0):
        self.ad = ad
        self.fiyat = fiyat
        self.stok = stok
        self.hazirlama_suresi = hazirlama_suresi  # dakika cinsinden

    def stok_guncelle(self, miktar):
        self.stok += miktar

    def siparis_al(self, miktar):
        if miktar <= self.stok:
            self.stok -= miktar
            return True
        return False

class Siparis:
    def __init__(self, musteri_ad, urun, miktar):
        self.siparis_id = str(uuid.uuid4())[:8]
        self.musteri_ad = musteri_ad
        self.urun = urun
        self.miktar = miktar
        self.tutar = urun.fiyat * miktar
        self.durum = "Hazırlanıyor"

class Restoran:
    def __init__(self):
        self.urunler = []
        self.siparisler = []

    def urun_ekle(self, ad, fiyat, stok, hazirlama_suresi=0):
        for u in self.urunler:
            if u.ad == ad:
                u.stok_guncelle(stok)
                u.hazirlama_suresi = hazirlama_suresi
                return "Stok ve hazırlanma süresi güncellendi."
        yeni_urun = Urun(ad, fiyat, stok, hazirlama_suresi)
        self.urunler.append(yeni_urun)
        return "Yeni ürün eklendi."

    def urun_listele(self):
        return self.urunler

    def siparis_olustur(self, musteri_ad, urun_ad, miktar):
        for urun in self.urunler:
            if urun.ad == urun_ad:
                if urun.siparis_al(miktar):
                    yeni_siparis = Siparis(musteri_ad, urun, miktar)
                    self.siparisler.append(yeni_siparis)
                    return yeni_siparis
                else:
                    return None
        return None

    def siparis_listele(self):
        return self.siparisler

# --- GUI ---

class GirisEkrani:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Girişi")
        self.root.geometry("300x150")
        self.root.configure(bg="#0a2342")

        tk.Label(root, text="Kullanıcı Adı:", bg="#0a2342", fg="white").pack(pady=5)
        self.kullanici_entry = tk.Entry(root)
        self.kullanici_entry.pack()

        tk.Label(root, text="Şifre:", bg="#0a2342", fg="white").pack(pady=5)
        self.sifre_entry = tk.Entry(root, show="*")
        self.sifre_entry.pack()

        tk.Button(root, text="Giriş Yap", bg="#1e90ff", fg="white", command=self.giris_yap).pack(pady=10)

    def giris_yap(self):
        kullanici = self.kullanici_entry.get().strip()
        sifre = self.sifre_entry.get().strip()

        if kullanici == "admin" and sifre == "1234":
            self.root.destroy()
            main_root = tk.Tk()
            app = RestoranGUI(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre yanlış!")

class RestoranGUI:
    def __init__(self, root):
        self.restoran = Restoran()
        # Örnek ürünler, hazırlama süresi eklendi (dakika cinsinden)
        self.restoran.urun_ekle("Pizza", 120, 10, 15)
        self.restoran.urun_ekle("Hamburger", 75, 8, 7)
        self.restoran.urun_ekle("Lahmacun", 40, 20, 5)

        self.root = root
        self.root.title("Restoran Sipariş ve Yönetim Sistemi")
        self.root.geometry("800x700")
        self.root.configure(bg="#0a2342")

        self.create_widgets()
        self.guncelle_urun_listesi()
        self.guncelle_siparis_listesi()

    def create_widgets(self):
        # Ürün Listesi
        urun_label = tk.Label(self.root, text="Ürün Listesi", bg="#0a2342", fg="white", font=("Arial", 14, "bold"))
        urun_label.pack(pady=5)

        self.urun_listbox = tk.Listbox(self.root, width=60, height=8, font=("Arial", 12))
        self.urun_listbox.pack(pady=5)

        # Ürün Ekleme Frame
        frame_urun_ekle = tk.Frame(self.root, bg="#0a2342")
        frame_urun_ekle.pack(pady=10)

        tk.Label(frame_urun_ekle, text="Ürün Adı:", bg="#0a2342", fg="white").grid(row=0, column=0, padx=5)
        self.urun_adi_entry = tk.Entry(frame_urun_ekle)
        self.urun_adi_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_urun_ekle, text="Fiyat:", bg="#0a2342", fg="white").grid(row=0, column=2, padx=5)
        self.fiyat_entry = tk.Entry(frame_urun_ekle)
        self.fiyat_entry.grid(row=0, column=3, padx=5)

        tk.Label(frame_urun_ekle, text="Stok:", bg="#0a2342", fg="white").grid(row=0, column=4, padx=5)
        self.stok_entry = tk.Entry(frame_urun_ekle)
        self.stok_entry.grid(row=0, column=5, padx=5)

        tk.Label(frame_urun_ekle, text="Hazırlama Süresi (dk):", bg="#0a2342", fg="white").grid(row=0, column=6, padx=5)
        self.hazirlama_entry = tk.Entry(frame_urun_ekle, width=5)
        self.hazirlama_entry.grid(row=0, column=7, padx=5)

        urun_ekle_btn = tk.Button(frame_urun_ekle, text="Ürün Ekle", bg="#1e90ff", fg="white",
                                  command=self.urun_ekle_button_click)
        urun_ekle_btn.grid(row=0, column=8, padx=5)

        # Sipariş Verme Frame
        frame_siparis = tk.Frame(self.root, bg="#0a2342")
        frame_siparis.pack(pady=20)

        tk.Label(frame_siparis, text="Müşteri Adı:", bg="#0a2342", fg="white").grid(row=0, column=0, padx=5)
        self.musteri_entry = tk.Entry(frame_siparis)
        self.musteri_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame_siparis, text="Miktar:", bg="#0a2342", fg="white").grid(row=0, column=2, padx=5)
        self.miktar_entry = tk.Entry(frame_siparis)
        self.miktar_entry.grid(row=0, column=3, padx=5)

        siparis_ver_btn = tk.Button(frame_siparis, text="Sipariş Ver", bg="#1e90ff", fg="white",
                                   command=self.siparis_ver_button_click)
        siparis_ver_btn.grid(row=0, column=4, padx=5)

        # Sipariş Geçmişi Label
        siparis_label = tk.Label(self.root, text="Sipariş Geçmişi", bg="#0a2342", fg="white", font=("Arial", 14, "bold"))
        siparis_label.pack(pady=5)

        # Sipariş geçmişi için Treeview (tablo)
        self.siparis_tree = ttk.Treeview(self.root, columns=("ID", "Müşteri", "Ürün", "Miktar", "Tutar", "Durum", "Hazırlama Süresi"),
                                        show="headings", height=8)
        self.siparis_tree.pack(pady=5)

        for col in ("ID", "Müşteri", "Ürün", "Miktar", "Tutar", "Durum", "Hazırlama Süresi"):
            self.siparis_tree.heading(col, text=col)
            self.siparis_tree.column(col, width=110)

        # Sipariş Durum Güncelleme Butonu
        durum_guncelle_btn = tk.Button(self.root, text="Sipariş Durumunu Güncelle", bg="#1e90ff", fg="white",
                                       command=self.siparis_durum_guncelle)
        durum_guncelle_btn.pack(pady=5)

    def urun_ekle_button_click(self):
        ad = self.urun_adi_entry.get().strip()
        fiyat = self.fiyat_entry.get().strip()
        stok = self.stok_entry.get().strip()
        hazirlama = self.hazirlama_entry.get().strip()

        if not ad or not fiyat.isdigit() or not stok.isdigit() or (hazirlama and not hazirlama.isdigit()):
            messagebox.showerror("Hata", "Lütfen geçerli ürün bilgileri girin.")
            return

        fiyat = int(fiyat)
        stok = int(stok)
        hazirlama = int(hazirlama) if hazirlama else 0

        mesaj = self.restoran.urun_ekle(ad, fiyat, stok, hazirlama)
        messagebox.showinfo("Bilgi", mesaj)
        self.guncelle_urun_listesi()

        self.urun_adi_entry.delete(0, tk.END)
        self.fiyat_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)
        self.hazirlama_entry.delete(0, tk.END)

    def siparis_ver_button_click(self):
        secili = self.urun_listbox.curselection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen bir ürün seçin.")
            return

        musteri_ad = self.musteri_entry.get().strip()
        miktar = self.miktar_entry.get().strip()

        if not musteri_ad or not miktar.isdigit() or int(miktar) <= 0:
            messagebox.showerror("Hata", "Lütfen geçerli müşteri adı ve miktar girin.")
            return

        urun = self.restoran.urun_listele()[secili[0]]
        miktar = int(miktar)

        siparis = self.restoran.siparis_olustur(musteri_ad, urun.ad, miktar)

        if siparis:
            messagebox.showinfo("Başarılı", f"{musteri_ad} için {miktar} adet {urun.ad} siparişi oluşturuldu.")
            self.guncelle_urun_listesi()
            self.guncelle_siparis_listesi()

            self.musteri_entry.delete(0, tk.END)
            self.miktar_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Hata", "Yeterli stok yok veya ürün bulunamadı.")

    def siparis_durum_guncelle(self):
        secili = self.siparis_tree.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen güncellemek istediğiniz siparişi seçin.")
            return
        siparis_id = self.siparis_tree.item(secili[0])['values'][0]

        for siparis in self.restoran.siparisler:
            if siparis.siparis_id == siparis_id:
                if siparis.durum == "Hazırlanıyor":
                    siparis.durum = "Hazırlandı"
                elif siparis.durum == "Hazırlandı":
                    siparis.durum = "Teslim Edildi"
                else:
                    siparis.durum = "Hazırlanıyor"
                break

        self.guncelle_siparis_listesi()

    def guncelle_urun_listesi(self):
        self.urun_listbox.delete(0, tk.END)
        for urun in self.restoran.urun_listele():
            self.urun_listbox.insert(tk.END, f"{urun.ad} - {urun.fiyat} TL - Stok: {urun.stok} - Hazırlama Süresi: {urun.hazirlama_suresi} dk")

    def guncelle_siparis_listesi(self):
        for i in self.siparis_tree.get_children():
            self.siparis_tree.delete(i)

        for siparis in self.restoran.siparis_listele():
            self.siparis_tree.insert("", tk.END, values=(
                siparis.siparis_id,
                siparis.musteri_ad,
                siparis.urun.ad,
                siparis.miktar,
                f"{siparis.tutar} TL",
                siparis.durum,
                f"{siparis.urun.hazirlama_suresi} dk"
            ))


if __name__ == "__main__":
    root = tk.Tk()
    giris = GirisEkrani(root)
    root.mainloop()
