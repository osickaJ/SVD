from carClass import Car, Truck

def main():
    print("OOP")

    carOne = Car("Fiat Ka", 2005)
    carOne.printModel()
    carOne.printAge()
    carOne.printColor()
    carOne.setColor("blue")
    carOne.printColor()

    monster = Truck("Liaz", 1999, 150)
    monster.evaluateCargo(480)

if __name__ == "__main__":
        main()