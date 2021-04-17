import numpy as np

def simulasyon (baslangic_stok,donem,yeniden_siparis_noktasi,hedef):

        # Kaç dönem simülasyon yapılacaksa o kadar random sayı ataması yapılıyor
        talepler = np.random.normal(100, 20, donem)
        maliyetler = np.zeros([2,donem])
        # maliyetler [0][0] -> Elde bulundurma maliyeti
        # maliyetler [0][1] -> Yoksatma maliyeti

        b = 0
        karsilanmayan_talep = 0
        kacinciDonem = 0
        for i in talepler:
            i = i + karsilanmayan_talep
            if baslangic_stok <= yeniden_siparis_noktasi:
                x = hedef - baslangic_stok
                baslangic_stok = x + baslangic_stok
                if i <= baslangic_stok:
                    kalan_stok = baslangic_stok - i
                    if kalan_stok >= 0:
                        maliyetler[0][kacinciDonem] = kalan_stok * 2
                        maliyetler[1][kacinciDonem] = 0

                elif i > baslangic_stok:
                    karsilanmayan_talep = abs(baslangic_stok - i)
                    kalan_stok = 0
                    if karsilanmayan_talep > 0:
                        maliyetler[1][kacinciDonem] = karsilanmayan_talep * 3
                        maliyetler[0][kacinciDonem] = 0

            elif baslangic_stok > yeniden_siparis_noktasi:
                if i <= baslangic_stok:
                    kalan_stok = baslangic_stok - i
                    if kalan_stok >= 0:
                        maliyetler[1][kacinciDonem] = 0
                        maliyetler[0][kacinciDonem] = kalan_stok * 2

                elif i > baslangic_stok:
                    karsilanmayan_talep = abs(baslangic_stok - i)
                    kalan_stok = 0
                    if karsilanmayan_talep > 0:
                        maliyetler[1][kacinciDonem] = karsilanmayan_talep * 3
                        maliyetler[0][kacinciDonem] = 0
            # Bir sonraki döneme geçiş yapılıyor
            kacinciDonem += 1
            baslangic_stok = kalan_stok


            # Burada nasıl bir hesap yapılıyor anlamadım??

            # elde_bulundurma_ortalamasi = hesapArrayi[0]
            # yoksatma_maliyeti_ortalamasi = hesapArrayi[1]
            hesapArrayi = np.sum(maliyetler, axis=0)
            Toplam = (hesapArrayi[0] + hesapArrayi[1])
            b = b + Toplam

        return [yeniden_siparis_noktasi,hedef,b]

baslangic_stok = 100
donem = 100
simSuresi = 5

# Kaç dönem simülasyon yapılacağı kararlaştırılıyor
for i in range(simSuresi):
    # Her simülasyonda yeni bir hedef ve yeniden sipariş noktası belirle
    yeniden_siparis_noktasi = np.random.randint(0, 150)
    hedef = np.random.randint(yeniden_siparis_noktasi, 150)

    #sonucArrayi[0] = yeniden sipariş noktası
    #sonucArrayi[1] = hedef
    #sonucArrayi[2] = b
    # "{:.2f}".format(sonucArrayi[2]) => b değerini virgülden sonraki 2 sayıyı göstererek yazdır
    sonucArrayi = simulasyon(baslangic_stok,donem,yeniden_siparis_noktasi,hedef)
    print("(",sonucArrayi[0],",",sonucArrayi[1],") => Toplam Maliyet = ","{:.2f}".format(sonucArrayi[2]))