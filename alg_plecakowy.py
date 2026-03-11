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
limit_wagi = 300        #[kg]
limit_liczby = 100      #[paczki]

# Losowo wybiera pierwotny zbior paczek
def init_random_hms(csv_file):
    global HM
    HM = []
    paczki = []

    with open(csv_file, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader) # naglowek
        for row in reader:
            waga = float(row[1])
            priorytet = float(row[2])
            paczki.append((waga, priorytet))

    for _ in range(HMS):
        zestaw = []
        suma_wagi = 0

        while len(zestaw) < limit_liczby and suma_wagi < limit_wagi:
            paczka = random.choice(paczki)
            if suma_wagi + paczka[0] <= limit_wagi:
                zestaw.append(paczka)
                suma_wagi += paczka[0]
        HM.append(zestaw)
        #HMwartosc.append(fitness(zestaw))

# Funkcja przystosowania
#def fitness():
    #...

#def punish():
    #...

def main():
    init_random_hms('Paczki_dane.csv')
    print(HM)