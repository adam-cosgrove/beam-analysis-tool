from solver import Beam
from solver import PointLoad
from solver import DistributedLoad


def main():

    print("\n----- Beam Analysis Tool -----\n")

    length = float(input("Enter beam length (m): "))
    print("\n")

    beam = Beam(length)

    while True:

        print("Select option")
        print("1. Add point load")
        print("2. Add distributed load")
        print("3. Analyse beam")
        print("4. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":

            magnitude = float(input("Magnitude (kN): "))
            position = float(input("Position (m): "))
            print("\n")

            beam.add_load(PointLoad(magnitude, position))

            print("Point load added.\n")

        elif choice == "2":

            magnitude_a = float(input("Start magnitude (kN/m): "))
            magnitude_b = float(input("End magnitude (kN/m): "))
            position_a = float(input("Start position (m): "))
            position_b = float(input("End position (m): "))
            print("\n")

            beam.add_load(DistributedLoad(magnitude_a, magnitude_b, position_a, position_b))

            print("Distributed load added.\n")

        elif choice == "3":

            ra, rb = beam.calculate_reactions()

            print("\nResults")
            print(f"RA = {ra:.2f} kN")
            print(f"RB = {rb:.2f} kN")

            beam.plot()

        elif choice == "4":

            print("Closing program.")
            break

        else:

            print("Invalid selection.")


if __name__ == "__main__":
    main()