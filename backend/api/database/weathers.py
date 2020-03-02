"""
Weather condidtion types as python enums
"""

from enum import Enum, auto


class WeatherTypes(Enum):

    Rainy = auto()
    Windy = auto()
    Sunny = auto()
    Snowing = auto()
