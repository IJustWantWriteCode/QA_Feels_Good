import random

students = {
    'Vitaliy': [random.randint(3, 5) for _ in range(10)],
    'Kirill': [random.randint(3, 5) for _ in range(10)],
    'Anton': [random.randint(3, 5) for _ in range(10)],
}

for key, value in students.items():
    if sum(value) / len(value) > 4.1:
        print(key, end=' ')
