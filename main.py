import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# giriş değişkenleri
sicaklik = ctrl.Antecedent(np.arange(0, 101, 1), 'sıcaklık')
basinc = ctrl.Antecedent(np.arange(0, 101, 1), 'basınç')
nem = ctrl.Antecedent(np.arange(0, 101, 1), 'nem')
karisim = ctrl.Antecedent(np.arange(0, 101, 1), 'karışım')
kukurt = ctrl.Antecedent(np.arange(0, 101, 1), 'kükürt')
viskozite = ctrl.Antecedent(np.arange(0, 101, 1), 'viskozite')
yogunluk = ctrl.Antecedent(np.arange(0, 101, 1), 'yoğunluk')
partikul = ctrl.Antecedent(np.arange(0, 101, 1), 'partikül')
akis_hizi = ctrl.Antecedent(np.arange(0, 101, 1), 'akış_hızı')

# giriş değişkenleri için üyelik fonksiyonu
#yakıt sıcaklığı
sicaklik['düşük'] = fuzz.trimf(sicaklik.universe, [0, 0, 50])
sicaklik['orta'] = fuzz.trimf(sicaklik.universe, [25, 50, 75])
sicaklik['yüksek'] = fuzz.trimf(sicaklik.universe, [50, 100, 100])
#yakıt basıncı
basinc['düşük'] = fuzz.trimf(basinc.universe, [0, 0, 50])
basinc['orta'] = fuzz.trimf(basinc.universe, [25, 50, 75])
basinc['yüksek'] = fuzz.trimf(basinc.universe, [50, 100, 100])
#yakıt nem oranı
nem['düşük'] = fuzz.trimf(nem.universe, [0, 0, 50])
nem['orta'] = fuzz.trimf(nem.universe, [25, 50, 75])
nem['yüksek'] = fuzz.trimf(nem.universe, [50, 100, 100])
#yakıt karışım oranı
karisim['düşük'] = fuzz.trimf(karisim.universe, [0, 0, 50])
karisim['orta'] = fuzz.trimf(karisim.universe, [25, 50, 75])
karisim['yüksek'] = fuzz.trimf(karisim.universe, [50, 100, 100])
#yakıt kükürt içeriği
kukurt['düşük'] = fuzz.trimf(kukurt.universe, [0, 0, 50])
kukurt['orta'] = fuzz.trimf(kukurt.universe, [25, 50, 75])
kukurt['yüksek'] = fuzz.trimf(kukurt.universe, [50, 100, 100])
#yakıt viskozitesi
viskozite['düşük'] = fuzz.trimf(viskozite.universe, [0, 0, 50])
viskozite['orta'] = fuzz.trimf(viskozite.universe, [25, 50, 75])
viskozite['yüksek'] = fuzz.trimf(viskozite.universe, [50, 100, 100])
#yakıt yoğunluğu
yogunluk['düşük'] = fuzz.trimf(yogunluk.universe, [0, 0, 50])
yogunluk['orta'] = fuzz.trimf(yogunluk.universe, [25, 50, 75])
yogunluk['yüksek'] = fuzz.trimf(yogunluk.universe, [50, 100, 100])
#yakıt partikül boyutu
partikul['küçük'] = fuzz.trimf(partikul.universe, [0, 0, 50])
partikul['orta'] = fuzz.trimf(partikul.universe, [25, 50, 75])
partikul['büyük'] = fuzz.trimf(partikul.universe, [50, 100, 100])
#yakıt akış hızı
akis_hizi['düşük'] = fuzz.trimf(akis_hizi.universe, [0, 0, 50])
akis_hizi['orta'] = fuzz.trimf(akis_hizi.universe, [25, 50, 75])
akis_hizi['yüksek'] = fuzz.trimf(akis_hizi.universe, [50, 100, 100])

# çıktı değişkeninin tanımlanması
kalite = ctrl.Consequent(np.arange(0, 101, 1), 'kalite')

#kalite üyelik fonksiyonları tanımlanması
kalite['düşük'] = fuzz.trimf(kalite.universe, [0, 0, 50])
kalite['orta'] = fuzz.trimf(kalite.universe, [25, 50, 75])
kalite['yüksek'] = fuzz.trimf(kalite.universe, [50, 100, 100])

# kuralların oluşturulması
rule1 = ctrl.Rule(sicaklik['düşük'] & basinc['düşük'], kalite['düşük'])
rule2 = ctrl.Rule(sicaklik['orta'] & nem['yüksek'], kalite['orta'])
rule3 = ctrl.Rule(karisim['yüksek'] & kukurt['orta'], kalite['yüksek'])
rule4 = ctrl.Rule(viskozite['orta'] & yogunluk['orta'] & partikul['orta'], kalite['yüksek'])
rule5 = ctrl.Rule(nem['yüksek'] & akis_hizi['yüksek'], kalite['orta'])
rule6 = ctrl.Rule(sicaklik['yüksek'] & basinc['yüksek'] & kukurt['yüksek'], kalite['yüksek'])
rule7 = ctrl.Rule(sicaklik['yüksek'] & basinc['orta'] & nem['düşük'] & karisim['düşük'], kalite['orta'])
rule8 = ctrl.Rule(kukurt['yüksek'] & viskozite['orta'] & yogunluk['orta'], kalite['orta'])
rule9 = ctrl.Rule(partikul['büyük'] & akis_hizi['orta'], kalite['düşük'])
rule10 = ctrl.Rule(basinc['orta'] & nem['orta'] & viskozite['yüksek'], kalite['yüksek'])
rule11 = ctrl.Rule(sicaklik['orta'] & karisim['yüksek'] & kukurt['orta'] & yogunluk['orta'], kalite['yüksek'])
rule12 = ctrl.Rule(partikul['küçük'] & akis_hizi['yüksek'], kalite['orta'])

# kontrol sistemi
kalite_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
kalite_sim = ctrl.ControlSystemSimulation(kalite_ctrl)

# kalite seviyesini giriş değerlerini hesaplayan ve gösteren fonksiyon
def calculate_quality():
    try:

        kalite_sim.input['sıcaklık'] = float(sicaklik_entry.get())
        kalite_sim.input['basınç'] = float(basinc_entry.get())
        kalite_sim.input['nem'] = float(nem_entry.get())
        kalite_sim.input['karışım'] = float(karisim_entry.get())
        kalite_sim.input['kükürt'] = float(kukurt_entry.get())
        kalite_sim.input['viskozite'] = float(viskozite_entry.get())
        kalite_sim.input['yoğunluk'] = float(yogunluk_entry.get())
        kalite_sim.input['partikül'] = float(partikul_entry.get())
        kalite_sim.input['akış_hızı'] = float(akis_hizi_entry.get())

        kalite_sim.compute()

        quality_level = kalite_sim.output['kalite']

        result_label.config(text=f"Yakıt Kalite Seviyesi: {quality_level:.2f}")

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {str(e)}")

# arayüz penceresi oluştur
root = tk.Tk()
root.title("Bulanık Mantık Yakıt Kalite Kontrolü")

# giriş widget yazı ve girdi alanlarını oluşturma
tk.Label(root, text="Sıcaklık (0-100 arası)").grid(row=0, column=0)
sicaklik_entry = tk.Entry(root)
sicaklik_entry.grid(row=0, column=1)

tk.Label(root, text="Basınç (0-100 arası)").grid(row=1, column=0)
basinc_entry = tk.Entry(root)
basinc_entry.grid(row=1, column=1)

tk.Label(root, text="Nem (0-100 arası)").grid(row=2, column=0)
nem_entry = tk.Entry(root)
nem_entry.grid(row=2, column=1)

tk.Label(root, text="Karışım (0-100 arası)").grid(row=3, column=0)
karisim_entry = tk.Entry(root)
karisim_entry.grid(row=3, column=1)

tk.Label(root, text="Kükürt (0-100 arası)").grid(row=4, column=0)
kukurt_entry = tk.Entry(root)
kukurt_entry.grid(row=4, column=1)

tk.Label(root, text="Viskozite (0-100 arası)").grid(row=5, column=0)
viskozite_entry = tk.Entry(root)
viskozite_entry.grid(row=5, column=1)

tk.Label(root, text="Yoğunluk (0-100 arası)").grid(row=6, column=0)
yogunluk_entry = tk.Entry(root)
yogunluk_entry.grid(row=6, column=1)

tk.Label(root, text="Partikül (0-100 arası)").grid(row=7, column=0)
partikul_entry = tk.Entry(root)
partikul_entry.grid(row=7, column=1)

tk.Label(root, text="Akış Hızı (0-100 arası)").grid(row=8, column=0)
akis_hizi_entry = tk.Entry(root)
akis_hizi_entry.grid(row=8, column=1)

# hesaplama butonu oluştur
calculate_button = ttk.Button(root, text="Yakıt Kalitesi Hesapla", command=calculate_quality)
calculate_button.grid(row=10, column=0, columnspan=2, pady=10)

# çıktıyı ekranda göster
result_label = ttk.Label(root, text="Yakıt Kalite Seviyesi: ")
result_label.grid(row=11, column=0, columnspan=2)

# Tkinter event döngüsünü başlat
root.mainloop()
