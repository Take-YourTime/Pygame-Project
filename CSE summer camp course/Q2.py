print("請輸入n的值：", end = "")
n = int(input())

list = [ [1, 1] ]

for index in range(0, 21):
    list[index].insert(0, 0)
    list[index].append(0)

    arr = []

    for i in range(0, len(list[index]) - 1):
        arr.append(list[index][i] + list[index][i + 1])
    
    list.append(arr)

for index in range(0, n):
    for i in range(1, len(list[index]) - 1):
        print(list[index][i], "\t", end = "")
    print()