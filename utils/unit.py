from lux.game_objects import Unit


def has_enough_resource(unit: Unit) -> bool:
    if unit.is_cart():
        return False

    return unit.cargo.wood >= 100 or unit.cargo.coal >= 100 or unit.cargo.uranium >= 100
