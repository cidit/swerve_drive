
from vec import Vector2
from math import *
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from collections.abc import Callable
from operator import attrgetter
import model as m
import ui_tools as uit
import world as w
import gear_system
import tap
import arcade


class GearSimulatorView(arcade.View):
    debug: bool = False
    world: w.World
    gsys: gear_system.GearSystem
    
    def __init__(self, window = None, background_color = None):
        super().__init__(window, background_color)
    
    def on_update(self, delta_time):
        return super().on_update(delta_time)