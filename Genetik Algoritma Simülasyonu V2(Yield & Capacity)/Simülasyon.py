import matplotlib.pyplot as plt
import numpy as np
from ypstruct import structure
import GenetikAlgoritma as ga

# Burada verilen değerler test amaçlıdır, bir değer girilmeden fonksiyon çağırılırsa kullanılır
def simulasyon (yeniden_siparis_noktasi,hedef):
    baslangic_stok = 100
    donem = 365
    # Kaç dönem simülasyon yapılacaksa o kadar random sayı ataması yapılıyor
    talepler = np.random.normal(100, 20, donem)
    maliyetler = np.zeros([3,donem])
    # maliyetler [0][0] -> Elde bulundurma maliyeti
    # maliyetler [0][1] -> Yoksatma maliyeti
    # maliyetler [0][2] -> Sipariş maliyeti

    elde_bulundurma_maliyeti = 1
    yoksatma_maliyeti = 2
    siparis_maliyeti = 10

    # random yield oluşturulması için alt ve üst sınırların tanımlanması
    yieldMin = 1
    yieldMax = 1

    # random Capacity oluşturulması için
    randomCapacity = np.inf

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
params.maxit = 100              # Maksimum iterasyon sayısı
params.npop = 50                # Popülasyon büyüklüğü (kromozom sayısı)
params.pc = 1                   # Üretilecek olan çocuk sayısının popülasyona oranı
params.gamma = 0.1
params.mu = 0.1
params.sigma = 0.1

# GA çalıştır
ciktilar = ga.run(problem,params)
ortalamaMaliyetler = np.zeros([params.maxit])
eldeBulundurmaMaliyetleri = np.zeros([params.maxit])
yoksatmaMaliyetleri = np.zeros([params.maxit])
siparisMaliyetleri = np.zeros([params.maxit])
yenidenSiparisDegerleri = np.zeros([params.maxit])
hedefDegerleri = np.zeros([params.maxit])

for i in range(len(ciktilar)):
    ortalamaMaliyetler[i] = ciktilar[i].cost
    eldeBulundurmaMaliyetleri[i] = ciktilar[i].elde_bulundurma_maliyeti
    yoksatmaMaliyetleri[i] = ciktilar[i].yoksatma_maliyeti
    siparisMaliyetleri[i] = ciktilar[i].siparis_maliyeti
    yenidenSiparisDegerleri = ciktilar[i].yenidenSiparis[0]
    hedefDegerleri = ciktilar[i].hedef[0]

fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

twin1 = ax.twinx()
twin2 = ax.twinx()

# Offset the right spine of twin2.  The ticks and label have already been
# placed on the right by twinx above.
twin2.spines.right.set_position(("axes", 1.2))

p1, = ax.plot(eldeBulundurmaMaliyetleri, "b-", label="Elde Bulundurma")
p2, = twin1.plot(yoksatmaMaliyetleri, "r-", label="Yoksatma")
p3, = twin2.plot(siparisMaliyetleri, "g-", label="Sipariş")

ax.set_xlim(0, params.maxit)

ax.set_xlabel("İterasyonlar")
ax.set_ylabel("Elde Bulundurma")
twin1.set_ylabel("Yoksatma")
twin2.set_ylabel("Sipariş")

ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())
twin2.yaxis.label.set_color(p3.get_color())

tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
twin2.tick_params(axis='y', colors=p3.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)

ax.legend(handles=[p1, p2, p3])

plt.show()