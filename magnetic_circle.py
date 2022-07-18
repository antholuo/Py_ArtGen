"""
magnetic_circle.py
Anthony Luo (antholuo@gmail.com)
July 17, 2022
================================================
Generates random art based on magnets around a circle.
"""

### Imports
import cairo
import math
import random

### Global Variables
FILE_FORMAT = "PNG"

HEIGHT = "1000"
WIDTH = "1000"
GRID_SIZE = "100"
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
        if self.drawStroke is not False:
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