# Example file showing a circle moving on screen
# import pygame as pg
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

SPEED = 1  # rad/s
JOYSTICK_SIZE = 50
AB_GEAR_SIZE = 50


GearId = int

# returns the resulting motion gear 2 must do relative to gear 1
# GearRelations = Callable[[GearId, GearId], m.Transform]


# def make_swerve_module():
#     """the assembly
#     should comport multiple gears in some sort of parent-child hierarchy(?) or at least in which gears are relative to one another and can lock.
#     propagation type system?
#     """

#     motor_gear_a = Gear(20)  # axially fixed
#     ring_gear_a = Gear(50)  # axially fixed
#     small_gear_a = Gear(ring_gear_a.radius / 2)  # relative to ring_gear_a

#     motor_gear_b = Gear(20)
#     ring_gear_b = Gear(50)
#     small_gear_b = Gear(ring_gear_b.radius / 2)

#     # these have an analog relationship because they are linked via a belt
#     motor_gear_a.link(ring_gear_a, GearLink.DIRECT)
#     motor_gear_b.link(ring_gear_b, GearLink.DIRECT)

#     ring_gear_a.link(small_gear_a, GearLink.DIRECT)
#     ring_gear_b.link(small_gear_b, GearLink.DIRECT)

#     small_gear_a.link(small_gear_b, GearLink.INVERSE)

#     # motor_gear_a.drive(some_rads)
#     # motor_gear_b.drive(some_rads)
#     # for g in gears():
#     #   g.get_transform()
#     pass


# gs = GearSystem()
# gear1_handle = gs.add_gear(Gear(50))
# gear2_handle = gs.add_gear(Gear(50))
# gs.link(gear_1_id=gear1_handle, gear_2_id=gear2_handle, link_type=GearLink.INVERSE)


class MyAppArgParser(tap.Tap):
    debug: bool = False


parser = MyAppArgParser()
args = parser.parse_args()

pg.init()
screen = pg.display.set_mode((500, 500))
world = w.World()
gs = gear_system.GearSystem()
clock = pg.time.Clock()

running = True
dt = 0


origin_offset = pg.Vector2(screen.get_width() / 2, screen.get_height() / 2)


gear_a_id = world.spawn(
    m.Parent(world.world_id),
    m.Transform(pg.Vector2(-75, 0), 0),
    m.Gear(25, "red"),
    m.Gizmo("Gear 1"),
)
gear_A_id = world.spawn(
    m.Parent(world.world_id),
    m.Transform(pg.Vector2(0, 0), 0),
    m.Gear(50, "red"),
    m.Gizmo("Gear 2"),
)

gear_b_id = world.spawn(
    m.Parent(world.world_id),
    m.Transform(pg.Vector2(75, 0), 0),
    m.Gear(25, "blue"),
    m.Gizmo("Gear 1"),
)
gear_B_id = world.spawn(
    m.Parent(world.world_id),
    m.Transform(pg.Vector2(0, 0), 0),
    m.Gear(50, "blue"),
    m.Gizmo("Gear 2"),
)


origin_gizmo = world.spawn(
    m.Parent(world.world_id), m.Transform(pg.Vector2(0, 0), 0), m.Gizmo("origin")
)

gs.make_relation(gear_a_id, gear_A_id, m.GearRelation.INVERSE)
gs.make_relation(gear_b_id, gear_B_id, m.GearRelation.INVERSE)



while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    for event in pg.event.get():
        # stop loop if quitting with x button or on focus loss
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.WINDOWFOCUSLOST:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE] or keys[pg.K_q]:
        running = False
    if keys[pg.K_a] or keys[pg.K_LEFT]:
        # gs.drive(gear1_handle, SPEED * pi * dt)
        pass
    if keys[pg.K_d] or keys[pg.K_RIGHT]:
        # gs.drive(gear1_handle, -SPEED * pi * dt)
        pass

    drive_by = 1 * dt  # 1 rad per second
    relations = gs.get_relations(gear_a_id)

    for g1, g2, relation in relations:
        # FIXME: DRIVING MANUALLY FOR NOW....
        match relation:
            case m.GearRelation.INVERSE:
                ratio = world.gears[g1].radius / world.gears[g2].radius
                world.transforms[g1].rotation += dt  # drived gear
                world.transforms[g2].rotation -= dt * ratio
            case _:
                print(f"relation unimplemented: {relation.name}")

    uit.draw_world_entities(screen, world, origin_offset, debug=args.debug)

    # flip() the display to put your work on screen
    pg.display.flip()

    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    FPS = 30
    dt = clock.tick(FPS) / 1000

pg.quit()
