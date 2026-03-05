from datetime import datetime
import math
class Car():

    def __init__(self, model, year):
        self.model = model 
        self.year = year
        self.color = None

    def printModel(self):
        print(f"Model of the car is {self.model}.")

    def printAge(self):
        current_year = datetime.now().year
        age = current_year - self.year
        print(f"The car is {age} years old.")

    def setColor(self, color):
        self.color = color 

    def printColor(self):
        if self.color: 
            print(f"The car has {self.color} color.")
        else:
            print(f"Car color not set.")

class Truck(Car):
        
        def __init__(self, model, year, capacity):
            super().__init__( model,year)
            self.capacity = capacity

        def evaluateCargo(self, weight):
            numTrucks = math.ceil(weight / self.capacity)
            print(f"To transfer {weight} tons, you would need {numTrucks} {self.model} trucks.")

        