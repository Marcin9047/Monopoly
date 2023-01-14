# Monopoly

Uproszczona wersja monopoly zawierająca kluczowe elementy gry.
***
> ### Uruchomienie następuje z pliku main podając nicki graczy uczestniczących w rozgrywce
***
Gra opiera sie na podstawowych klasach takich jak **Player**, **Property**, **Area**, **Dices** oraz **Special_Square**

## Klasa Player
***
***Zawiera podstawowe parametry każdego gracza***

* W konstruktorz przyjmuje informacje o imieniu gracza oraz ilości pieniedzy.

* Pozostałe wartości takie jak informacje o posiadanych działkach, pozycji i pauzie gracz nabywa w trakcie gry. Pozycja gracza podczas tworzenia ustawiana jest na 0 (Start).

* Posiada możliwość ustawienia również pionka gracza za pomocą metody **set_pon**.

* W zależnośći od wymagań programu możliwe jest dodawanie, odejmowanie card, działek oraz ilości pieniędzy.
#
> W przypadku odejmowania za dużej ilości pieniędzy program zwróci **NotEnoughtMoneyError**
#
* Metoda **value_of_proerties** pozwala uzyskać informacje odnośnie całkowitej wartości posiadanych przez gracza posiadłości razem z domkami.

* Gracz może poruszać się po planszy za pomocą metod **move_forward/move_backward*. Program operuje na 40-polowej planszy a więc przesunięcie na 41 pole wiąże się z ustawieniem pozycji na 1

* Metoda **isactive** -> True/False | Informuje czy gracz dalej uczestniczy w rozgrywce

    Możliwe jest również jej ustawienie za pomocom metody **set_inactive**

## Klasa Square
***
***Iniciowana przez klasy podległe. Zawiera informacje o typie i położeniu danego pola.***

## Klasa Property >> Square 
***Klasa pozwalająca na wykonywanie podstawowych operacji na nieruchomościach***

* Konstruktor:
    * Przyjmuje takie informacje jak: nazwa, pozycja, cena, czynsz, obszar do którego należy oraz informacje o domkach i jej właścicielu jeśli taki istnieje
    * do klasy **Square** przekazuje typ : "property" oraz pozycje

* Za pomocą metod **increase_rent/decrease_rent** można wpływać na wielkość renty co zostanie wykorzystane przy ustawianiu domków

* Posiada metodę **pay_rent** ,która od określonego gracza pobiera ilość pieniędzy równą aktualnej wartości czynszu. W przypadku gdy posesja jest zastawiona właściciel nie otrzymuje pieniędzy

***
> Zwraca **NotEnoughtMoneyError** gdy gracz nie jest w stanie opłacić czynszu
***
* Metoda **set_pladge** pozwala na zastawienie posesji i otrzymanie wartości równej połowie wartości czynszu

***
> Zwraca **WrongInputError** gdy wartość jaką gracz chce ustawić jest taka sama jak aktualna
***

* Metoda **set_home_cost** określa cenę zakupu domku w zależności od strony planszy

* Metoda **buy_house** pozwala na zakup domu po spełnieniu odpowiednich wymagań. Zakup zwiększa procentowo wartość czynszu posiadłości

***
> Zwraca **NotOwnerOfEveryError** gdy gracz nie jest właścicielem każdej posiadłości w danum obszarze

> Zwraca **HousesFullError** gdy na określonej posiadłości zakupiona została juz maksumalna liczba domków

> Zwraca **NotEnoughtMoneyError** gdy gracz nie posiada wystarczających funduszy

> Zwraca **HousesNotEquallyError** gdy gracz nie kupuje domków równomiernie
***

* Metoda **sell_house** posiada na sprzedaż domu na posiadłości, której jesteśmy właścicielem

***
> Zwraca **ZeroHousesError** gdy gracz próbuje sprzedać dom na pustej działce
***

* Posiada również metody **sell** i **buy**
które odpowiednio sprzedają posiadłość i ustawiają właściciela na None oraz kupują pusta posiadłość.

***
> Metoda **buy** zwraca **NotEnoughtMoneyError**
***

## Klasa Special >> Square
***Klasa dla posesji specjalnych takich jak Start lub Lotnisko***

* Konstruktor określa parametry dla klassy Square oraz ustawia wartość gdy karta ma dawać lub zabierać pieniądze.

* Posiada metode **do_action**, która dla konkretnych nazw określa wykonywaną przez program operacje

## Klasa Area
***
***Klasa informująca o składzie danego obszaru***

* W konstruktorze przyjmuje nazwę oraz listę działek wchodzącą w skład.

* Umożliwia ustawienie koloru w celu rozróżnienie obszarów na planszy

* Pozwala na dodanie posiadłości do listy za pomocą metody **add_property**

* Metoda **check_if_fully_occupied** sprawdza czy gracz posiada wszystkie posiadłości z danego obszaru

## Klasa Dices << Player
***Klasa służąca do zarządania kośćmi graczy i decydowaniu o wykonaniu rzutu***

* W konstruktorze nie przyjmuje żadnych wartości

* Metoda **dice_throw**
zwraca dwie  losowe cyfry z zakresu 1-6

* Metoda **dublets** informuej czy wartości na obu kościach były takie same

* Metoda **ready_to_play** określa czy liczba rzutów gracza jest większa niz zero oraz nie jest on aktualnie w trakcie pauzy

* Metoda **throw_dices** wykonuje rzut i przesuwa gracza o określoną ilośc pól. Liczy równiez dublety i w przypadku wyrzucenia 3 pod rząd przenosi gracza do więzienia

***
> Zwraca **ZeroThrowsError** gdy gracz nie może wykonać rzutu
***

## Interface
***Gra korzysta z biblioteki Pygame***

* Uruchamiając gre tworzymy planszę oraz dwie tablice z wynikami i akcjami do wykonania

* Gracz może wpływać na przebieg gry za pomocą przycisków generowanych na tablicy akcji

* Tablica wyników informuje o ilości posiadanych pieniędzy przez każdego gracza oraz pauzie jeśli taka występuje

* Nad planszą wyswietlany jest dodatkowo aktualny gracz

* Plansza podzielona jest na część centralną oraz zewnętrzna gdzie znajdują sie posiadłości i pola specjalne

* Przy posiadłościach wyświetlana jest ich nazwa oraz kolor obszaru do którego należą

* Możliwa jest zmiana koloru podstawowych części planszy oraz zmiana wielkości napisu środkowego