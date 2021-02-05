from math import sqrt, cos
import json


def read_json(path: str):
    with open(path) as fp:
        data = json.load(fp)
    return data


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Distance calculation for close locations. Using only Pythagoras theorem.
    :param lat1:
    :param lon1:
    :param lat2:
    :param lon2:
    :return:
    """
    DEG2RAD = 0.0174532925199432958  # PI / 180
    radius = 6378.
    latrad1 = lat1 * DEG2RAD
    lonrad1 = lon1 * DEG2RAD
    latrad2 = lat2 * DEG2RAD
    lonrad2 = lon2 * DEG2RAD
    dx = radius * diff(lonrad1, lonrad2) * cos(latrad1)
    dy = radius * diff(latrad1, latrad2)
    return sqrt(dx * dx + dy * dy)


def diff(deg1: float, deg2: float) -> float:
    DEGREE = 600000
    result = deg2 - deg1
    if result > 180 * DEGREE:
        return result - 360 * DEGREE
    elif result < -180 * DEGREE:
        return result + 360 * DEGREE
    else:
        return result
