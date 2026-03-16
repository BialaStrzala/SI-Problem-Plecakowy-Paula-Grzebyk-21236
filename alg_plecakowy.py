# Problem optymalizacji ładunku paczek - każdy list/paczka ma przypisaną wagę [g] oraz priorytet [1-10], z jakim musi zostać dostarczona.
# Furgonetka ma limit przewozu 300kg oraz 100 różnych paczek na raz.

import csv
import random

# Tablica z rozwiazaniami
HM = []
# Tablica z wartosciami rozwiazan
HMwartosc = []
# Ilosc startowych rozwiazan
HMS = 10
# HMCR
HMCR = 0.7
# Liczba iteracji
NI = 5
# Dane zadania
limit_wagi = 100*1000           #[kg->g]
limit_liczby = 10               #[paczki]
wszystkie_paczki = []

# r = random 0-100, r<70 -> pierwsza paczka z random zestawu 1-10, r>30 - druga paczka random z csv... az do 10 paczek
# fitness(nowy zestaw) > min fitness(HM) -> zamienia HM

# Losowo wybiera pierwotny zbior paczek
def init_random_hm(csv_file):
    global HM
    HM = []
    global wszystkie_paczki
    wszystkie_paczki = []

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            waga = float(row['weight'])
            priorytet = float(row['priority'])
            wszystkie_paczki.append((waga, priorytet))
            #print(f"{waga}, {priorytet}")

    # n-zestawow (HMS)
    for _ in range(HMS):
        zestaw = []
        suma_wagi = 0
        while len(zestaw) < limit_liczby:
            paczka = random.choice(wszystkie_paczki)
            #print('wybrana paczka (waga): ' + f"{paczka[0]}")
            zestaw.append(paczka)
            suma_wagi += paczka[0]
            #print('dodaje paczke do zestawu')
        HM.append(zestaw)
        HMwartosc.append(fitness(zestaw))
        print('=== Kolejne startowe zestawy ===')
        print('Liczba paczek = ' + f"{len(zestaw)}" + ', suma_wagi = ' + f"{suma_wagi:.2f}")


# Funkcja przystosowania
def fitness(zestaw):
    suma_priorytetow = sum(paczka[1] for paczka in zestaw)
    suma_wag = sum(paczka[0] for paczka in zestaw)
    print('=== sum pr zestawu: ')
    print(suma_priorytetow)
    print('=== suma wag zestawu:')
    print(suma_wag)
    if suma_wag > limit_wagi:
        print('za duza waga')
        suma_priorytetow = suma_priorytetow/2
    return suma_priorytetow


def run():
    i = 0
    j = 0
    while i<NI:
        i = i+1
        nowy_zestaw = []
        while j<limit_liczby:
            j = j+1
            r = random.randint(0, 100)
            if r < 70:
                k = random.randint(0,limit_liczby)
                #nowy_zestaw.append(HM[k][0]) # pierwsza paczka z losowego zestawu!!!
                nowy_zestaw.append(random.choice(wszystkie_paczki))
            else:
                nowy_zestaw.append(random.choice(wszystkie_paczki)) # losowa paczka ze wszystkich
            print('======nowy zestaw=========')
            print(nowy_zestaw)
        if fitness(nowy_zestaw) > min(HMwartosc): # zamiana zestawu z min fitness na nowy zestaw
            index = HMwartosc.index(min(HMwartosc))
            HM.pop(index)
            HM.append(nowy_zestaw)
            HMwartosc.pop(index)
            HMwartosc.append(fitness(nowy_zestaw))
    
    # Wyniki
    print(max(HMwartosc))
    print(HM[HMwartosc.index(max(HMwartosc))])


def main():
    init_random_hm('Paczki_dane.csv')
    print(HM)
    print('=== HM ===')
    print('Liczba zestawow = ' + f"{len(HM)}")
    print('Dziala')
    fitness(HM[0])

    print('index min hmwartosc: ')
    print(HMwartosc)
    print(min(HMwartosc))
    print(HMwartosc.index(min(HMwartosc)))

    run()
    #print(HM[0])

main()