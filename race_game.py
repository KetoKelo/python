import random as R
from time import sleep


class Vehicle:

    def __init__(self, color, fuel_remaining=100, speed=300):
        self.color = color
        self.fuel_remaining = fuel_remaining
        self.speed = speed
        self.laps = 0
        self.lap_times = []

class Car(Vehicle):

    vehicle_type = "Car"

    def __init__(self, *args):
        super().__init__(*args)
        self.fuel_remaining *= 1.2
        self.speed *= 0.9

class Motorbike(Vehicle):

    vehicle_type = "Motorbike"

    def __init__(self, *args):
        super().__init__(*args)
        self.fuel_remaining *= 0.9
        self.speed *= 1.1

class Truck(Vehicle):

    vehicle_type = "Truck"

    def __init__(self, *args):
        super().__init__(*args)
        self.fuel_remaining *= 1.5
        self.speed *= 0.7

class Race:
    
    def __init__(self, racers):
        self.racers = racers
        self.total_times = {}

    def run(self, length):
        for racer in self.racers:
            # Prints color and vehicle type of racer
            print(">", (racer.color + " - " + racer.vehicle_type).upper(), "<")
            while racer.laps < length:
                if racer.vehicle_type == "Car": # If vehicle is a car
                    decreasing_factor = R.randint(11, 20)
                    lap_time = R.randint(10, 20) / 1000

                if racer.vehicle_type == "Motorbike": # If vehicle is a motorbike
                    decreasing_factor = R.randint(13, 23)
                    lap_time = R.randint(7, 17) / 1000

                if racer.vehicle_type == "Truck": # If vehicle is a truck
                    decreasing_factor = R.randint(6, 16)
                    lap_time = R.randint(15, 25) / 1000

                racer.laps += 1
                racer.fuel_remaining -= (length * lap_time * decreasing_factor) # Decreases fuel
                racer.lap_times.append(racer.speed * lap_time) # Generates lap time

                if racer.fuel_remaining < 0: # Turns to 0 any negative fuel values
                    racer.fuel_remaining = 0

                if racer.laps % length == 0: # Prints racer stats by lap
                    print("- LAP", racer.laps, "-")
                    print("Time: {:.3f}".format(racer.lap_times[racer.laps - 1]), "minutes")
                    print("Fuel: {:.3f}".format(racer.fuel_remaining), "litres")
                    print()

                if (racer.fuel_remaining <= 0) and (racer.laps < 30):
                    for index, item in enumerate(racer.lap_times):
                        if item != 0: # Turns to 0 each lap time if racer runs out of fuel
                            racer.lap_times[index] = 0
                    print("{} ran out of gas at lap {} and has been disqualified!".format(racer.color.upper(), racer.laps))
                    break

            if sum(racer.lap_times) > 0: # Prints final stats if racer isn't disqualified
                self.total_times[racer.color] = sum(racer.lap_times)

                print("Race time: {:.3f}".format(sum(racer.lap_times)), "minutes")
                print("Remaining fuel: {:.3f}".format(racer.fuel_remaining), "litres")

            print("="*50)
            print()

        self.is_winner() # Gets winner

    def is_winner(self):
        if len(self.total_times) > 0:
            best_time = min(self.total_times.values())

            for key, value in self.total_times.items():
                if value == best_time:
                    winner = key

            print("CONGRATULATIONS!!!")
            print("The winner is {} with a total time of {:.3f} minutes!!!" \
                  .format(winner.upper(), best_time))
        else:
            print("All racers have been disqualified. Better luck next time!")

class Racer:
    racers = [] # Lists all the racers

    def add_racer(self, *args): # Asks for type of vehicle
                                # Adds racer into racers list
        valid_answers_vehicle = ("C", "M", "T")
        vehicle = ""
        add_racer = is_valid_input("Select a vehicle (C=Car/M=Motorbike/T=Truck): ", str,
                                "Please enter a valid answer", valid_answers_vehicle)
        
        if (add_racer == "C") or (add_racer == "c"):
            vehicle = Car
        elif (add_racer == "M") or (add_racer == "m"):
            vehicle = Motorbike
        elif (add_racer == "T") or (add_racer == "t"):
            vehicle = Truck

        color = input("Choose the color of your {}: ".format((vehicle.__name__).lower()))

        self.racers.append(vehicle(color, fuel, speed))

def is_valid_input(txt_input, data_type, txt_error, *args): # Input validator
    is_valid = False

    while not is_valid:
        value = input(txt_input).upper()

        if any(args): # If input gets special answers
            for item in args:
                if value.upper() in item:
                    return value
        else: # Other types of inputs
            try:
                value = data_type(value)
                is_valid = True
            except ValueError:
                print(txt_error)

    return value

if __name__ == "__main__":
    fuel = is_valid_input("Enter the fuel quantity: ", float, "Please enter a number.")
    speed = is_valid_input("Enter the speed: ", float, "Please enter a number.")
    laps = is_valid_input("Enter the laps: ", int, "Please enter an integer.")

    racer = Racer()
    while len(racer.racers) < 2:
        racer.add_racer(fuel, speed)

    if len(racer.racers) == 2:
        last = False
        valid_answers_yes_no = ("Y", "N")

        while not last:
            add_new_racer = is_valid_input("Do you want to add a new racer? (Y/N): ", str,
                                    "Please enter a valid answer", valid_answers_yes_no)
                                    
            if (add_new_racer == "Y") or (add_new_racer == "y"):
                racer = Racer()
                racer.add_racer(fuel, speed)
            else:
                last = True
                print("READY...")
                sleep(1)
                print("STEADY...")
                sleep(1)
                print("GO!")
                print("="*50)
                sleep(1)

                race = Race(Racer.racers)
                race.run(laps)
