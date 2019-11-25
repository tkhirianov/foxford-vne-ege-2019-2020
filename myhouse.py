from graph import *


def paint_house(x, y, width, height):
    foundation_height = int(height * 0.1)
    walls_height = int(height * 0.5)
    roof_height = height - foundation_height - walls_height

    paint_foundation(x, y + walls_height, width, foundation_height)
    paint_walls(x, y, width, walls_height)
    paint_roof(x, y, width, roof_height)


def paint_foundation(x, y, width, height):
    print(1)
    pass


def paint_walls(x, y, width, height):
    print(2)
    pass


def paint_roof(x, y, widht, height):
    print(3)
    pass




def main():
    paint_house(150, 150, 120, 100)
    run()



main()
