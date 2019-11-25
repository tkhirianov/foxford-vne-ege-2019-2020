from graph import *


def paint_house(x, y, width, height):
    foundation_height = int(height * 0.1)
    walls_height = int(height * 0.6)
    roof_height = height - foundation_height - walls_height

    paint_foundation(x, y + walls_height, width, foundation_height)
    paint_walls(x, y, width, walls_height)
    paint_roof(x, y, width, roof_height)


def paint_foundation(x, y, width, height):
    brushColor(80, 50, 0)
    penColor("black")
    rectangle(x, y, x + width, y + height)


def paint_walls(x, y, width, height):
    brushColor(180, 40, 0)
    penColor("black")
    rectangle(x, y, x + width, y + height)


def paint_roof(x, y, width, height):
    brushColor(180, 190, 30)
    penColor("black")
    polygon([(x, y), (x + width // 2, y - height), (x + width, y)])




def main():
    paint_house(150, 150, 120, 100)
    run()



main()
