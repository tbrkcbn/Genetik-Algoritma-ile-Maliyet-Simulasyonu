import numpy as np
from ypstruct import structure


def run(problem,params):
    temp = 0
    # Problem Bilgisinin alınması
    costfunc = problem.costfunc
    nvar = problem.nvar
    varmin = problem.varmin
    varmax = problem.varmax

    # Parametreler
    maxit = params.maxit
    npop = params.npop
    pc = params.pc
    nc = np.round(pc*npop/2)*2                                          # Üretilecek olan çocuk sayısı
    gamma = params.gamma
    mu = params.mu
    sigma = params.sigma


    # Boş birey şablonu
    empty_individual = structure()
    empty_individual.hedef = None
    empty_individual.yenidenSiparis = None
    empty_individual.cost = None


    # En iyi birey şablonu
    bestsol = empty_individual.deepcopy()                               # Eğer deepcopy() kullanılmazsa bestsol değiştiğinde empty_ind değeri de değişir
    bestsol.cost = np.inf                                               # Önceden en iyi çözümün maliyetini sonsuz bir değere eşitliyoruz


    # Popülasyonun (Boş bireylerden oluşan bir array) oluşturulması, bu kısım ilk iterasyon için hazırlandı, sonrasında 2,3,4.... n iterasyona kadar alttaki döngü çalışacak
    pop = empty_individual.repeat(npop)                                         # önceden belirlenmiş büyüklükte bir popülasyon oluşturulması
    for i in range(0,npop):
        pop[i].yenidenSiparis = np.random.uniform(varmin, varmax, nvar)         # önceden belirlenmiş sınırlar içerisinde, önceden belirlenmiş büyüklüğe göre
        pop[i].hedef = np.random.uniform(pop[i].yenidenSiparis[0], varmax, nvar)
        pop[i].cost = costfunc(pop[i].yenidenSiparis[0], pop[i].hedef[0])       #rastgele pozisyonların oluşturulması
        if pop[i].cost < bestsol.cost:                                          # eğer popülasyondaki i. bireyin (kromozomun) maliyet değeri
            bestsol = pop[i].deepcopy()                                         #en iyi bireyin maliyetinden küçükse en iyi değer değiştirilir


    # En iyi yineleme maliyeti
    bestcost = np.empty(maxit)                                          # Her iterasyonun sonunda en iyi maliyeti tutan içi boş array


    # Ana döngü
    for it in range(maxit):                                             # Bu döngü içerisinde her iterasyon için mutasyon, crossover, vb. gibi işlemler uygulanacak

        popc = []                                                       # Üretilecek çocukların listesi (ilk başta boş)
        for k in range (int(nc//2)):                                    # Yeni çocukların üretilmesi için for döngüsü

            # Ebeveynlerin seçimi
            q = np.random.permutation(npop)                             # 0'dan npop değerine kadar bütün sayıları rastgele bir sırayla içeren (her birinden 1 tane) array
            p1 = pop[q[0]]
            p2 = pop[q[1]]

            # Çocukların seçimi
            c1, c2 = crossover(p1,p2, gamma)                            # Rastgele oluşuturulan 2 ebeveynden crossover ile 2 çocuk üretiliyor

            # Mutasyon
            c1 = mutate(c1, mu, sigma)
            c2 = mutate(c2, mu, sigma)

            # Sınırların eklenmesi
            # apply_bound(c1, varmin, varmax)
            # apply_bound(c2, varmin, varmax)

            # Sonuçların değerlendirilmesi

            # Birinci çocuğun değerlendirilmesi
            c1.yenidenSiparis.sort()
            c1.hedef.sort()
            c1.cost = costfunc(c1.yenidenSiparis[0], c1.hedef[0])
            if c1.cost < bestsol.cost:
                bestsol = c1.deepcopy()

            # İkinci çocuğun değerlendirilmesi
            c2.yenidenSiparis.sort()
            c2.hedef.sort()
            c2.cost = costfunc(c2.yenidenSiparis[0], c2.hedef[0])
            if c2.cost < bestsol.cost:
                bestsol = c2.deepcopy()

            # Üretilen çocukların popülasyona dahil edilmesi
            popc.append(c1)
            popc.append(c2)

        # yeni popülasyonun eski popülasyona eklenmesi
        pop += popc
        # en iyi sonuçların bulunması için sıralama
        sorted(pop, key = lambda  x: x.cost)
        # popülasyon büyüklüğüne kadar olan (öreneğin ilk 50) kromozomun seçilip yeni iterasyon için popülasyon haline getirilmesi
        pop = pop[0:npop]


        # En iyi maliyetin hafızaya aktarılması

        bestcost[it] = bestsol.cost

        # Iterasyon bilgisinin print edilmesi, sadece iyileştirme olduğunda ve son iterasyonun sonucunu print eder
        if bestsol.yenidenSiparis[0] != temp:
            print("{}. İterasyondaki yeniden sipariş noktası = {}, hedef = {},en iyi maliyet = {}".format(it + 1,bestsol.yenidenSiparis[0],bestsol.hedef[0],bestcost[it]))
            temp = bestsol.yenidenSiparis[0]
        if it == (maxit-1):
            print("\n---------------------------------------------------\n\n{} dönem uygulanan optimizasyon sonucunda bulunan minimum maliyet = {}\nYeniden Sipariş Noktası = {}\nHedef = {}".format(maxit,bestcost[it],bestsol.yenidenSiparis[0],bestsol.hedef[0]))

# iki farklı ebeveynden 2 farklı çocuk üretimi
def crossover(p1, p2, gamma = 0.1):

    c1 = p1.deepcopy()
    c2 = p2.deepcopy()

    # Alpha değeri tanımlanıyor
    yenidenSiparisAlpha = np.random.uniform(-gamma,1+gamma, *c1.yenidenSiparis.shape)

    # Crossover (Yeniden sipariş noktası için)
    c1.yenidenSiparis =     yenidenSiparisAlpha*p1.yenidenSiparis + (1-yenidenSiparisAlpha)*p2.yenidenSiparis
    c2.yenidenSiparis = (1-yenidenSiparisAlpha)*p1.yenidenSiparis +     yenidenSiparisAlpha*p2.yenidenSiparis

    hedefAlpha = np.random.uniform(-gamma, 1 + gamma, *c1.hedef.shape)
    # Crossover (Hedef için)
    c1.hedef =     hedefAlpha*p1.hedef + (1-hedefAlpha)*p2.hedef
    c2.hedef = (1-hedefAlpha)*p1.hedef +     hedefAlpha*p2.hedef

    return c1,c2

# x => mutasyona uğrayacak olan çözüm, mu => mutasyon oranı, sigma => adım sayısı?
def mutate(x, mu, sigma):

    # Mutasyona uğrayacak değer için x'den bilgiler kopyalanıyor
    y = x.deepcopy()

    yenidenSiparisFlag = np.random.rand(*x.yenidenSiparis.shape) <= mu
    ind = np.argwhere(yenidenSiparisFlag)

    y.yenidenSiparis[ind] = x.yenidenSiparis[ind] + sigma*np.random.randn(*ind.shape)

    hedefFlag = np.random.rand(*x.hedef.shape) <= mu
    ind = np.argwhere(hedefFlag)

    y.hedef[ind] = x.hedef[ind] + sigma*np.random.randn(*ind.shape)

    return y

def apply_bound(x, varmin, varmax):
    x.yenidenSiparis = np.maximum(x.yenidenSiparis,varmin)
    x.yenidenSiparis = np.minimum(x.yenidenSiparis,varmax)

    x.hedef = np.maximum(x.hedef,x.yenidenSiparis)
    x.hedef = np.minimum(x.hedef,varmax)