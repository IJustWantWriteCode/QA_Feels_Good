class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def print_car_info(self):
        print(self.brand, self.model, self.year)


car1 = Car('BMW', '5 series', 2020)
car2 = Car('Mercedes', 'E classe', 2023)
car3 = Car('Audi', 'A6', 2021)

car1.print_car_info()
car2.print_car_info()
car3.print_car_info()