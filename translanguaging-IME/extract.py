with open("Cangjie5.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

my_list = []

for line in lines:
    parts = line.strip().split()

    if len(parts) == 2:
        key, value = parts
        my_list.append((key, value))

#call method : list[][]
