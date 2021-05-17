import numpy as np
from ypstruct import structure
import GenetikAlgoritma as ga

# Burada verilen değerler test amaçlıdır, bir değer girilmeden fonksiyon çağırılırsa kullanılır
def simulasyon (yeniden_siparis_noktasi= 50,hedef = 150):
    baslangic_stok = 100
    donem = 100
    # Kaç dönem simülasyon yapılacaksa o kadar random sayı ataması yapılıyor
    talepler = np.random.normal(100, 20, donem)
    maliyetler = np.zeros([3,donem])
    # maliyetler [0][0] -> Elde bulundurma maliyeti
    # maliyetler [0][1] -> Yoksatma maliyeti
    # maliyetler [0][2] -> Sipariş maliyeti

    elde_bulundurma_maliyeti = 1
    yoksatma_maliyeti = 2
    siparis_maliyeti = 10

    b = 0
    karsilanmayan_talep = 0
    kacinciDonem = 0
    for i in talepler:
        i = i + karsilanmayan_talep
        if baslangic_stok <= yeniden_siparis_noktasi:
            x = hedef - baslangic_stok
            y = np.random.uniform(0.8, 1)
            baslangic_stok = (x * y) + baslangic_stok
            maliyetler[2][kacinciDonem] = x * siparis_maliyeti
            maliyetler[1][kacinciDonem] = 0
            maliyetler[0][kacinciDonem] = 0
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


        # elde_bulundurma_ortalamasi = hesapArrayi[0]
        # yoksatma_maliyeti_ortalamasi = hesapArrayi[1]
        hesapArrayi = np.sum(maliyetler, axis=0)

    Toplam = np.sum(hesapArrayi)
    b = Toplam / donem

    # Ortalama maliyeti döndürüyoruz
    return b

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
out = ga.run(problem,params)
