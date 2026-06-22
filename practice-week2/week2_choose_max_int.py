import random

int_lst = [random.randint(10, 100) for i in range(9)]
max_int = float('-inf')

for num in int_lst:
    if num > max_int:
        max_int = num

print(max_int)