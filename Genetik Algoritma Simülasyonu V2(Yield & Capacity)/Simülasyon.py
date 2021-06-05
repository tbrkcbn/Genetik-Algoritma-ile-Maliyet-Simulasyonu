import matplotlib.pyplot as plt
import numpy as np
from ypstruct import structure
import GenetikAlgoritma as ga

# Burada verilen değerler test amaçlıdır, bir değer girilmeden fonksiyon çağırılırsa kullanılır
def simulasyon (yeniden_siparis_noktasi,hedef):
    baslangic_stok = 100
    donem = 365
    # Kaç dönem simülasyon yapılacaksa o kadar random sayı ataması yapılıyor
    talepler = np.random.normal(100, 30, donem)
    maliyetler = np.zeros([3,donem])
    # maliyetler [0][0] -> Elde bulundurma maliyeti
    # maliyetler [0][1] -> Yoksatma maliyeti
    # maliyetler [0][2] -> Sipariş maliyeti

    elde_bulundurma_maliyeti = 1
    yoksatma_maliyeti = 5
    siparis_maliyeti = 10

    # random yield oluşturulması için alt ve üst sınırların tanımlanması, min = max = 1 = yield kısıtı yok
    yieldMin = 0.8
    yieldMax = 1

    # random Capacity oluşturulması için, np.inf = kapasite kısıtı yok
    randomCapacity = 100

    karsilanmayan_talep = 0
    kacinciDonem = 0
    for i in talepler:
        i = i + karsilanmayan_talep
        if baslangic_stok <= yeniden_siparis_noktasi:
            x = hedef - baslangic_stok
            y = np.random.uniform(yieldMin, yieldMax)
            baslangic_stok = min((x * y) + baslangic_stok, randomCapacity)
            maliyetler[2][kacinciDonem] = x * siparis_maliyeti
            maliyetler[1][kacinciDonem] = 0
            maliyetler[0][kacinciDonem] = 0
            if i <= baslangic_stok:
                kalan_stok = baslangic_stok - i
                if kalan_stok >= 0:
                    maliyetler[2][kacinciDonem] = x * siparis_maliyeti
                    maliyetler[1][kacinciDonem] = 0
                    maliyetler[0][kacinciDonem] = kalan_stok * elde_bulundurma_maliyeti

            elif i > baslangic_stok:
                karsilanmayan_talep = abs(baslangic_stok - i)
                kalan_stok = 0
                if karsilanmayan_talep > 0:
                    maliyetler[2][kacinciDonem] = x * siparis_maliyeti
                    maliyetler[1][kacinciDonem] = karsilanmayan_talep * yoksatma_maliyeti
                    maliyetler[0][kacinciDonem] = 0

        elif baslangic_stok > yeniden_siparis_noktasi:
            if i <= baslangic_stok:
                kalan_stok = baslangic_stok - i
                if kalan_stok >= 0:
                    maliyetler[2][kacinciDonem] = 0
                    maliyetler[1][kacinciDonem] = 0
                    maliyetler[0][kacinciDonem] = kalan_stok * elde_bulundurma_maliyeti

            elif i > baslangic_stok:
                karsilanmayan_talep = abs(baslangic_stok - i)
                kalan_stok = 0
                if karsilanmayan_talep > 0:
                    maliyetler[2][kacinciDonem] = 0
                    maliyetler[1][kacinciDonem] = karsilanmayan_talep * yoksatma_maliyeti
                    maliyetler[0][kacinciDonem] = 0

        # Bir sonraki döneme geçiş yapılıyor
        kacinciDonem += 1
        baslangic_stok = kalan_stok

        hesapArrayi = np.sum(maliyetler, axis=1)
        elde_bulundurma_ortalamasi = hesapArrayi[0]/donem
        yoksatma_maliyeti_ortalamasi = hesapArrayi[1]/donem
        siparis_maliyeti_ortalamasi = hesapArrayi[2]/donem



    ortalama_maliyet = np.sum(hesapArrayi)/donem

    # Ortalama maliyeti döndürüyoruz
    return [(ortalama_maliyet),(elde_bulundurma_ortalamasi),(yoksatma_maliyeti_ortalamasi),(siparis_maliyeti_ortalamasi)]

# Problem Tanımı
problem = structure()           # Problem değişkeni içerisinde 1den fazla veri gönderebilmek için
problem.costfunc = simulasyon   # Maliyet fonksiyonunun tanımlanması
problem.nvar = 1                # Değişken sayısı (popülasyonun her elemanı 5 değişkene sahip bir array olacak)
problem.varmin = 0              # Değişkeşerin alt sınırı
problem.varmax = 150            # Değişkenin üst sınırı

# GA parametreleri
params = structure()
params.maxit = 1000             # Maksimum iterasyon sayısı
params.npop = 50                # Popülasyon büyüklüğü (kromozom sayısı)
params.pc = 1                   # Üretilecek olan çocuk sayısının popülasyona oranı
params.gamma = 0.1
params.mu = 0.1
params.sigma = 0.1

# GA çalıştır
ciktilar = ga.run(problem,params)

# Çıktılardan alınan verilerin isimlendirilmesi
ortalamaMaliyetler = np.zeros([params.maxit])
eldeBulundurmaMaliyetleri = np.zeros([params.maxit])
yoksatmaMaliyetleri = np.zeros([params.maxit])
siparisMaliyetleri = np.zeros([params.maxit])
yenidenSiparisDegerleri = np.zeros([params.maxit])
hedefDegerleri = np.zeros([params.maxit])
iterasyonlar = np.zeros([params.maxit])

for i in range(len(ciktilar)):
    ortalamaMaliyetler[i] = ciktilar[i].cost
    eldeBulundurmaMaliyetleri[i] = ciktilar[i].elde_bulundurma_maliyeti
    yoksatmaMaliyetleri[i] = ciktilar[i].yoksatma_maliyeti
    siparisMaliyetleri[i] = ciktilar[i].siparis_maliyeti
    yenidenSiparisDegerleri[i] = ciktilar[i].yenidenSiparis[0]
    hedefDegerleri[i] = ciktilar[i].hedef[0]
    iterasyonlar[i] = i+1

# Çıktıların grafikler ile gösterilmesi
plt.plot(iterasyonlar,eldeBulundurmaMaliyetleri)

plt.plot(iterasyonlar,yoksatmaMaliyetleri)

plt.plot(iterasyonlar,siparisMaliyetleri)

plt.plot(iterasyonlar,ortalamaMaliyetler)

plt.xlabel('İterasyonlar')
plt.ylabel('Maliyetler')
plt.legend(['Elde Bulundurma','Yoksatma','Sipariş','Toplam'])
plt.show()


plt.plot(iterasyonlar,hedefDegerleri)

plt.plot(iterasyonlar,yenidenSiparisDegerleri)

plt.xlabel('İterasyonlar')
plt.ylabel('Değerler')
plt.legend(['Hedef','Yeniden Sipariş'])
plt.show()