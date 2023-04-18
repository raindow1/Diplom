indexes = []
a = 0
b = 100
file_number = 1
with open("patents.txt", "r") as file:
    for line in file:
        patent = line.split("/")
        if len(patent[4]) == 11 and 'C' in patent[4]:
            indexes.append(line)
#print(indexes)

while True:
    with open(f"/home/raindow/Diplom/Files/{file_number}.txt", "w+") as file1:
        for i in range(a,b):
            file1.write(indexes[i])
    a +=100
    b +=100
    file_number += 1
