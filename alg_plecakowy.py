# Problem optymalizacji ładunku paczek - każdy list/paczka ma przypisaną wagę [g] oraz priorytet [1-10], z jakim musi zostać dostarczona.
# Furgonetka ma limit przewozu 100kg oraz 10 różnych paczek na raz.

import csv
import random

# Wszystkie paczki
wszystkie_paczki = []
# Tablica z rozwiazaniami
HM = []
# Tablica z wartosciami rozwiazan
HMwartosc = []
# Ilosc startowych rozwiazan
HMS = 10
# HMCR
HMCR = 70                       #[%]
# Liczba iteracji
NI = 1000
# Dane zadania
limit_wagi = 100*1000           #[kg->g]
limit_liczby = 10               #[paczki]


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

    # n-zestawow (HM)
    for _ in range(HMS):
        zestaw = []
        while len(zestaw) < limit_liczby:
            paczka = random.choice(wszystkie_paczki)
            zestaw.append(paczka)
        HM.append(zestaw)
        HMwartosc.append(fitness(zestaw))


# Funkcja przystosowania
def fitness(zestaw):
    suma_priorytetow = sum(paczka[1] for paczka in zestaw)
    suma_wag = sum(paczka[0] for paczka in zestaw)
    if suma_wag > limit_wagi:
        suma_priorytetow = suma_priorytetow/2
    return suma_priorytetow


# Iteracje
def run():
    i = 0
    while i<NI:
        i = i+1
        #print(f"====== ITERACJA {i}/{NI}")
        nowy_zestaw = []
        r = random.randint(0, 100)

        # 1. Z HM - 70%
        if r < HMCR:
            for j in range(limit_liczby):
                j = j+1
                k = random.randint(0, len(HM)-1)
                nowy_zestaw.append(HM[k][j-1]) # n-ta paczka z losowego zestawu
            # 3. Losowa mutacja - 1%
            if r == 0:
                nowy_zestaw.pop(random.randint(0, len(HM)-1))
                nowy_zestaw.append(random.choice(wszystkie_paczki))
        # 2. Calkowicie losowy zestaw - 30%
        else:
            for j in range(limit_liczby):
                j = j+1
                nowy_zestaw.append(random.choice(wszystkie_paczki))
        
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