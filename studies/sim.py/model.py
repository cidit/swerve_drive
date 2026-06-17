from vec import Vector2
from math import *
from dataclasses import dataclass
from enum import Enum
from arcade.types import Color

EntityId = int

@dataclass
class JoystickData:
    xy: Vector2
    angle: float  # last coherent angle. needs to exist in case the vector is of (0, 0).


class GearRelation(Enum):
    AXIAL = -1  # transform is relative to an axis
    RELATIVE = 0  # rotation is relative to it's parent
    DIRECT = 1  # turns in the same direction
    INVERSE = 2  # turns in the oposite direction


@dataclass
class Transform:
    """component"""

    translation: Vector2
    rotation: float  # rads
    
    def with_offset(self, offset: Vector2):
        return Transform(self.translation + offset, self.rotation)


@dataclass
class Parent:
    """component"""

    id: EntityId


@dataclass
class Gear:
    """component"""

    radius: float
    color: Color = "black"


@dataclass
class Gizmo:
    """component"""

    label: str
