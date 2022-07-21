"""
magnetic_circle.py
Anthony Luo (antholuo@gmail.com)
July 17, 2022
================================================
Generates random art based on magnets around a circle.
"""

### Imports
import math
import os
import random
import time

import cairo

### Global Variables

FILE_FORMAT = "PNG"

HEIGHT = 1000
WIDTH = 1000
GRID_SIZE = 100
BORDER_SIZE = 50
MAG_BORDER = 450
STEP_X, STEP_Y = (WIDTH // GRID_SIZE), (HEIGHT // GRID_SIZE)


### Classes

class Particle:
    """
    Particle class. Each particle will turn into a line.
    """

    def __init__(self, x, y, velocity_x, velocity_y):
        """
        Initialization for our particle.
        :param x:
        :param y:
        :param velocity_x:
        :param velocity_y:
        """
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.force_x = 0
        self.force_y = 0
        self.last_x = x
        self.last_y = y
        self.draw_stroke = True

    def update(self):
        """
        Updates particle position by one unit step
        :return:
        """
        # particle is losing speed?
        self.velocity_x = self.velocity_x * 0.9
        self.velocity_y = self.velocity_y * 0.9

        self.x = self.x + self.velocity_x + self.force_x
        self.y = self.y + self.velocity_y + self.force_y

    def checkInEdges(self):
        """
        Checks that a particle is within the defined borders
        :return:
        """
        if self.x <= BORDER_SIZE or self.x >= WIDTH - BORDER_SIZE or \
                self.x <= BORDER_SIZE or self.y >= HEIGHT - BORDER_SIZE:
            self.draw_stroke = False
        else:
            self.draw_stroke = True

    def resetForce(self):
        """
        Resets the force on the particle
        :return:
        """
        self.force_x = 0
        self.force_y = 0

    def setForce(self, fx, fy):
        """
        Adds forces from magnets to current force (iteratively).
        This is becouse there could be multiple acting magnets w/diff forces.
        :param fx:
        :param fy:
        :return:
        """
        self.force_x = self.force_x + fx
        self.force_y = self.force_y + fy

    def setLastPos(self):
        """
        Sets the last position of the partle to be equal to current position.
        Done before moving particle forward
        :return:
        """
        self.last_x, self.last_y = self.x, self.y

    def calculateForce(self, mx, my, mp) -> [float, float]:
        """
        Calculates a force from magnet
        :param mx:
        :param my:
        :param mp:
        :return:
        """
        dist_y = mx - self.x
        dist_x = my - self.x
        angle = math.atan2(dist_y, dist_x) * mp
        sx = math.sin(angle)
        sy = math.cos(angle)
        return [sx, sy]

    def draw(self, context):
        """
        Draws particle onto image
        :param context:
        :return:
        """
        if self.draw_stroke is not False:
            context.set_line_width(0.9)
            context.set_source_rgba(0, 0, 0, 1)
            context.move_to(self.last_x, self.last_y)
            context.line_to(self.x, self.y)
            context.stroke()


class Magnet:
    """
    Magnet class. Each magnet pulls on all particles.
    """

    def __init__(self, x, y, pole):
        self.x = x
        self.y = y
        self.pole = pole


def generate(context):
    """
    Main function?
    :return:
    """
    context.set_source_rgba(0.95, 0.95, 0.95, 1)
    context.paint()

    magnets = []
    particles = []
    num_magnets = random.randint(2, 15)
    sum_x, sum_y = 0, 0
    sums = 0

    print("number of magnets: " + str(num_magnets))

    for m in range(num_magnets):
        pole = 1
        if random.uniform(0, 1) < 0.5:
            pole = -1
        magnets.append(Magnet(
                random.randint(100, WIDTH - 100),
                random.randint(100, HEIGHT - 100),
                pole
        ))

    start_num = 360
    a = (math.pi * 2) / start_num

    for x in range(100, WIDTH - 100, (WIDTH - 200) // 1):
        for y in range(100, HEIGHT - 100, (HEIGHT - 200) // 1):
            for i in range(start_num):
                # generate x, y position of particles
                xx = x + (math.sin(a * i) * 250) + ((WIDTH - 200) // 2)
                yy = y + (math.cos(a * i) * 250) + ((HEIGHT - 200) // 2)

                # generate velocity in x and y of particles
                vx = random.uniform(-1, 1) * 0.5
                vy = random.uniform(-1, 1) * 0.5

                # add to particle array
                particles.append(Particle(xx, yy, vx, vy))

    for p in particles:
        for t in range(1000):
            for m in magnets:
                # calculate sums for each magnet
                sums = p.calculateForce(m.x, m.y, m.pole * 4)

                # split sums into x and y
                sum_x = sum_x + sums[0]
                sum_y = sum_y + sums[1]

            # normalize
            sum_x = sum_x / len(magnets)
            sum_y = sum_y / len(magnets)

            # apply new forces to the particles and calculate new position \
            # after each time step
            p.resetForce()
            p.setForce(sum_x, sum_y)
            p.update()

            # if meeting timing, draw.
            if t % 8 == 0:
                p.draw(context)
                p.setLastPos()


def main():
    """
    Main function to call the rest
    :return:
    """
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)
    generate(context)
    timestr = time.strftime("%H%M%S")
    date = time.strftime("%Y%m%d")
    directory = "Outputs/magnetic_circle/" + date + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    surface.write_to_png(directory + str(timestr) + '.png')


if __name__ == "__main__":
    i = 0
    while (i < 10):
        main()
        i += 1
