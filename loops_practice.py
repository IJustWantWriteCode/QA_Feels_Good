import random
import time

class LoopsPractice:

    COUNT_ITER_IN_INT_CYCLE = 8
    MAX_INT_IN_CYCLE = 5

    COUNT_ITER_IN_STR_CYCLE = 10

    COUNT_ITER_ROSTICS = 10
    HIGH_LOAD_ROSTICS = 85
    MIN_LOAD_ROSTICS = 0
    MAX_LOAD_ROSTICS = 100
    TIME_SLEEP_ROSTICS = 0.2

    def list_int_cycle(self):
        numbers = list(range(1, self.COUNT_ITER_IN_INT_CYCLE))
        for n in numbers:
            print(n)
            if n == self.MAX_INT_IN_CYCLE:
                break

    def list_str_cycle(self):
        words = [f"str{i}" for i in range(self.COUNT_ITER_IN_STR_CYCLE)]
        for word in words:
            print(word)

    def imitation_load_rostics(self):
        iteration = 0
        while iteration < self.COUNT_ITER_ROSTICS:
            iteration += 1
            load = random.randint(self.MIN_LOAD_ROSTICS, self.MAX_LOAD_ROSTICS)
            print(f'Нагрузка : {load}%')
            if load <= self.HIGH_LOAD_ROSTICS:
                print("Нагрузка в пределах нормы")
            else:
                print("Высокая нагрузка!")
            time.sleep(self.TIME_SLEEP_ROSTICS)

practice = LoopsPractice()

practice.list_int_cycle()
practice.list_str_cycle()
practice.imitation_load_rostics()