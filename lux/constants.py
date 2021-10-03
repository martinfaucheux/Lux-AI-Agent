class Constants:
    class INPUT_CONSTANTS:
        RESEARCH_POINTS = "rp"
        RESOURCES = "r"
        UNITS = "u"
        CITY = "c"
        CITY_TILES = "ct"
        ROADS = "ccd"
        DONE = "D_DONE"

    class DIRECTIONS:
        NORTH = "n"
        WEST = "w"
        SOUTH = "s"
        EAST = "e"
        CENTER = "c"

        @classmethod
        def get_from_coord(cls, x: int, y: int):
            if x == 0:
                if y == -1:
                    return cls.NORTH
                elif y == 1:
                    return cls.SOUTH
            if y == 0:
                if x == -1:
                    return cls.WEST
                elif y == 1:
                    return cls.EAST
            return cls.CENTER

    class UNIT_TYPES:
        WORKER = 0
        CART = 1

    class RESOURCE_TYPES:
        WOOD = "wood"
        URANIUM = "uranium"
        COAL = "coal"
