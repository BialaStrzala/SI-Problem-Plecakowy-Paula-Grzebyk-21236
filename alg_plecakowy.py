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
NI = 100
# Dane zadania
limit_wagi = 100*1000           #[kg->g]
limit_liczby = 10               #[paczki]

# Losowo wybiera pierwotny zbior paczek
def init_random_hms(csv_file):
    global HM
    HM = []
    paczki = []

    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            waga = float(row['weight'])
            priorytet = float(row['priority'])
            paczki.append((waga, priorytet))
            #print(f"{waga}, {priorytet}")

    
    # n-zestawow (HMS)
    for _ in range(HMS):
        zestaw = []
        suma_wagi = 0
        while len(zestaw) < limit_liczby and suma_wagi < limit_wagi:
            paczka = random.choice(paczki)
            #print('wybrana paczka (waga): ' + f"{paczka[0]}")
            if suma_wagi + paczka[0] <= limit_wagi:
                zestaw.append(paczka)
                suma_wagi += paczka[0]
                #print('dodaje paczke do zestawu')
            else:
                #print('odrzucam paczke')
                break
        HM.append(zestaw)
        #HMwartosc.append(fitness(zestaw))
        print('=== Kolejne startowe zestawy ===')
        print('Liczba paczek = ' + f"{len(zestaw)}" + ', suma_wagi = ' + f"{suma_wagi:.2f}")


# Funkcja przystosowania
def fitness(HM):
    suma_priorytetu = [sum(paczka[1] for paczka in sublist) for sublist in HM]
    print(suma_priorytetu)
    

#def punish():
    #...

def main():
    init_random_hms('Paczki_dane.csv')
    print(HM)
    print('=== HM ===')
    print('Liczba zestawow = ' + f"{len(HM)}")
    print('Dziala')
    fitness(HM)

main()