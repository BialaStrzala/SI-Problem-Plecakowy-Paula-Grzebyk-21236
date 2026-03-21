# Problem optymalizacji ładunku paczek - każdy list/paczka ma przypisaną wagę [g] oraz priorytet [1-10], z jakim musi zostać dostarczona.
# Furgonetka ma limit przewozu 100kg oraz 10 różnych paczek na raz.

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
NI = 1000
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
        HM.append(zestaw)
        HMwartosc.append(fitness(zestaw))
        #print('Liczba paczek = ' + f"{len(zestaw)}" + ', suma_wagi = ' + f"{suma_wagi:.2f}")


# Funkcja przystosowania
def fitness(zestaw):
    suma_priorytetow = sum(paczka[1] for paczka in zestaw)
    suma_wag = sum(paczka[0] for paczka in zestaw)
    if suma_wag > limit_wagi:
        suma_priorytetow = suma_priorytetow/10
    return suma_priorytetow


# Iteracje
def run():
    i = 0
    while i<NI:
        i = i+1
        #print(f"====== ITERACJA {i}/{NI}")
        nowy_zestaw = []
        for j in range(limit_liczby):
            j = j+1
            r = random.randint(0, 100)
            if r < 70:
                k = random.randint(0, len(HM)-1)
                nowy_zestaw.append(HM[k][j-1]) # n-ta paczka z losowego zestawu
            else:
                nowy_zestaw.append(random.choice(wszystkie_paczki)) # losowa paczka ze wszystkich
        
        if fitness(nowy_zestaw) > min(HMwartosc): # zamiana zestawu z min fitness na nowy zestaw
            index = HMwartosc.index(min(HMwartosc))
            HM.pop(index)
            HM.append(nowy_zestaw)
            HMwartosc.pop(index)
            HMwartosc.append(fitness(nowy_zestaw))
    
    # Wyniki
    print("\n====== WYNIKI ======")
    print(f"Suma priorytetow najlepszego zestawu: {max(HMwartosc)} (max = {limit_liczby*10})")
    w = sum(paczka[0] for paczka in HM[HMwartosc.index(max(HMwartosc))])
    print(f"Suma wagi najlepszego zestawu: {w:.2f}")
    print("Najlepszy zestaw paczek:")
    print(HM[HMwartosc.index(max(HMwartosc))])
    if w>limit_wagi:
        print("Zestaw przekracza limit wagi")


def main():
    print("\n====== ALGORYTM PLECAKOWY ======")
    init_random_hm('Paczki_dane.csv')
    print("=== Poczatkowe HMwartosc ===")
    print(HMwartosc)
    print("\n=== Najlepsze rozwiazanie dla poczatkowego HM ===")
    print(f"Suma priorytetow zestawu: {max(HMwartosc)}")
    w = sum(paczka[0] for paczka in HM[HMwartosc.index(max(HMwartosc))])
    print(f"Suma wagi zestawu: {w:.2f}")
    run()

main()