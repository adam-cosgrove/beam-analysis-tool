import matplotlib.pyplot as plt

class PointLoad:

    def __init__(self, magnitude, position):
        self.magnitude = magnitude
        self.position = position

    def __repr__(self):
        return f"pl({self.magnitude}, {self.position})"

    def resultant_force(self):
        return self.magnitude

    def resultant_position(self):
        return self.position

    def force_to_left(self, x):

        if self.position <= x:
            return self.magnitude
        
        return 0

    def moment_to_left(self, x):

        if x >= self.position:
            return self.magnitude * (x - self.position)

        return 0

class DistributedLoad:

    def __init__(self, magnitude_a, magnitude_b, position_a, position_b):
        self.magnitude_a = magnitude_a
        self.magnitude_b = magnitude_b
        self.position_a = position_a
        self.position_b = position_b

    def __repr__(self):
        return f"dl({self.magnitude_a}, {self.magnitude_b}, {self.position_a}, {self.position_b})"

    def resultant_force(self):
        return (self.position_b - self.position_a) * (self.magnitude_a + self.magnitude_b) / 2

    def resultant_position(self):
        return self.position_a + ((self.position_b - self.position_a) * (self.magnitude_a + 2 * self.magnitude_b) / (3 * (self.magnitude_a + self.magnitude_b)))

    def force_to_left(self, x):
        if x <= self.position_a:
            return 0

        elif x >= self.position_b:
            return self.resultant_force()

        else:
            wx = (self.magnitude_a + (x - self.position_a) * (self.magnitude_b - self.magnitude_a) / (self.position_b - self.position_a))
            return ((self.magnitude_a + wx) * (x - self.position_a) / 2)
    
    def moment_to_left(self, x):

        if x <= self.position_a:
            return 0

        elif x >= self.position_b:
            return (self.resultant_force() * (x - self.resultant_position()))

        else:
            wx = (self.magnitude_a + (x - self.position_a) * (self.magnitude_b - self.magnitude_a) / (self.position_b - self.position_a))
            force = ((self.magnitude_a + wx) * (x - self.position_a) / 2)
            centroid = self.position_a + ((x - self.position_a) * (self.magnitude_a + 2 * wx) / (3 * (self.magnitude_a + wx)))
            return force * (x - centroid)

class Beam:

    def __init__(self, length):
        self.length = length
        self.loads = []
        self.ra = None
        self.rb = None

    def add_load(self, load):
        self.loads.append(load)

    def calculate_reactions(self):

        total_moment = 0
        total_force = 0

        for load in self.loads:

            total_moment += (load.resultant_force() * load.resultant_position())

            total_force += load.resultant_force()

        rb = total_moment / self.length
        ra = total_force - rb

        self.ra = ra
        self.rb = rb

        return ra, rb

    def calculate_shear(self):

        x_values = []
        sf_values = []

        for i in range(int(self.length * 10) + 1):

            x = i / 10

            sf = self.ra

            for load in self.loads:
                sf -= load.force_to_left(x)

            x_values.append(x)
            sf_values.append(sf)

        return x_values, sf_values

    def calculate_moment(self):

        x_values = []
        moment_values = []

        for i in range(int(self.length * 10) + 1):

            x = i / 10

            moment = self.ra * x

            for load in self.loads:
                moment -= load.moment_to_left(x)

            x_values.append(x)
            moment_values.append(moment)

        return x_values, moment_values

    def plot(self):

        x_sf, sf = self.calculate_shear()
        x_m, moment = self.calculate_moment()

        plt.figure(figsize=(10, 4))

        plt.subplot(1, 2, 1)

        plt.plot(x_sf, sf, color="blue")

        plt.axhline(y=0, color="black", linewidth=1)

        plt.plot([0, 0], [0, sf[0]], color="blue")
        plt.plot([self.length, self.length], [0, sf[-1]], color="blue")

        plt.grid()
        plt.title("Shear Force Diagram")
        plt.xlabel("Position (m)")
        plt.ylabel("Shear Force (kN)")

        plt.subplot(1, 2, 2)

        plt.plot(x_m, moment, color="red")

        plt.axhline(y=0, color="black", linewidth=1)

        plt.grid()
        plt.title("Bending Moment Diagram")
        plt.xlabel("Position (m)")
        plt.ylabel("Bending Moment (kNm)")

        plt.tight_layout()

        plt.show()