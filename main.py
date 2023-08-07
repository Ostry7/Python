# [************************] @Marek Ostrowski [************************]

#1. Napisz program, który oblicza pole trójkąta na podstawie długości dwóch boków i kąta między nimi.
#2. Stwórz program, który zamienia temperaturę w stopniach Celsiusza na stopnie Fahrenheita.
#3. Napisz skrypt, który odczytuje plik tekstowy i podaje liczbę słów, liczbę linii oraz liczbę znaków w tym pliku.
#4. Stwórz funkcję, która znajduje wszystkie liczby pierwsze w danym przedziale liczb.
#5. Napisz program, który odwraca kolejność znaków w podanym przez użytkownika zdaniu.
#6. Stwórz prostą grę w kółko i krzyżyk dla dwóch graczy.
#7. Napisz program, który generuje losowe hasło o określonej długości składające się z liter, cyfr i znaków specjalnych.
#8. Stwórz funkcję, która oblicza silnię dla danej liczby całkowitej.
#9. Napisz skrypt, który pobiera dane od użytkownika dotyczące jego imienia, wieku i ulubionego koloru, a następnie zapisuje je do pliku.
#10. Stwórz prostą aplikację do notowania zadań. Użytkownik powinien móc dodawać, usuwać i przeglądać zadania.




#1.

#import math
#
#print ("Select A: ")
#a = int(input())
#print ("Select B: ")
#b = int(input())
#print ("Select ANGLE: ")
#angle = int(input())
##wynik = triangle_area(a,b,angle)
#angle_rad = math.radians(angle)
#triangleArea = (a * b * 0.5 * math.sin(angle_rad))
#
#print(f"Pole trojkata wynosi: {triangleArea}")


#2

#def Fahr_calc():
#    print(f"Select temperature in Celsious: ")
#    Celc = float(input())
#    calculate = (Celc * (9/5) + 32)
#    print(f"{Celc} Celsious = {calculate} Fahrenheita")
#Fahr_calc()

#3
#
#def input_calc():
#    with open(r"test.txt", 'r') as file:
#        count = 0
#        for line in file:
#            if line != "\n":
#                count += 1
#    num_lines = count
#    file = open("test.txt", "r")
#    data = file.read()
#    num_of_characters = len(data)
#    num_of_words = data.split()
#    print(f"Number of characters: {num_of_characters}; number of lines: {num_lines}; number of words: {len(num_of_words)}")
#input_calc()
#
#4
def is_prime_numbers(num): 
    if num < 2:
        return False
    for i in range (2, int (num**0.5) + 1):
        if num % i == 0:
            return False
    return True
def prime_numbers(start,end):
    prime_num = []
    for num in range(start,end + 1):
        if is_prime_numbers(num):
            prime_num.append(num)
    return prime_num

print("Select start number: ")
start = int(input())
print("Select start number: ")
end = int(input())

prime_num = prime_numbers(start,end)
print(f"Prime numbers in {start} to {end}: {prime_num}")