import pygame as pg
from math import *
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from collections.abc import Callable
from operator import attrgetter
import model as m
import world as w



# class Gear:
#     radius: float
#     transform: Transform

#     def __init__(self, size: float, t: Transform | None):
#         self.radius = size
#         self.transform = t if t is not None else Transform(pg.Vector2,0)

#     def drive(self, rads: float):
#         self.rotation += rads
#         for other, link in self.links:
#             ratio = self.radius / other.radius
#             match link:
#                 case GearLink.COAXIAL:
#                     other.drive(rads)
#                 case GearLink.DIRECT:
#                     other.drive(rads * ratio)
#                 case GearLink.INVERSE:
#                     other.drive(-rads * ratio)


class GearSystem:
    """
    represents a gear system defined as a network of nodes guided by links and constraints
    """

    relations: set[tuple[int, int, m.GearRelation]]

    def __init__(self):
        self.relations = set()

    def make_relation(self, gear_1_id: int, gear_2_id: int, link_type: m.GearRelation):
        if gear_1_id == gear_2_id:
            raise AssertionError(f"cant have a relation with the same gear (id: {gear_1_id})")
        # order ids to ensure link stays unique
        minid, maxid = min(gear_1_id, gear_2_id), max(gear_1_id, gear_2_id)
        self.relations.add((minid, maxid, link_type))

    def get_relations(self, id: int):
        return [
            (g1, g2, relation)
            for g1, g2, relation in self.relations
            if g1 == id or g2 == id
        ]

    # def drive(self, gear_id: int, rads: float, traversed =[]):
    #     if not self.__gear_exists(gear_id):
    #         return

    #     for g1, g2, l in self.links:
    #         if not (g1 == gear_id or g2 == gear_id):
    #             continue
    #         in_g, out_g = (g1, g2) if g1 == gear_id else (g2, g1)

    #     pass

    # def __gear_exists(self, gear_id: int):
    #     return gear_id in range(len(self.gears))
