class Student:
   def __init__(self, name, age, grades):
       self.name = name
       self.age = age
       self.grades = grades

   def get_avg_grades(self):
       print(f'{self.name}: {sum(self.grades) / len(self.grades):.2f}')

student1 = Student('Vitaliy', 19, [3, 4, 2, 5, 4])
student2 = Student('Kirill', 21, [5, 4, 5, 4, 3])
student3 = Student('Anton', 23, [3, 4, 3, 4, 2])

student1.get_avg_grades()
student2.get_avg_grades()
student3.get_avg_grades()