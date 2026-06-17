import pygame as pg
from math import *
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from collections.abc import Callable
from operator import attrgetter
import model as m
import world as w


def pgcoords(screen: pg.Surface, coords: tuple[int, int]):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], screen.get_height() - coords[1])


def in_screen(screen: pg.Surface, x: float, y: float) -> bool:
    x, y = pgcoords((x, y))
    return x >= 0 and y >= 0 and x <= screen.get_width() and y <= screen.get_height()


def draw_joystick(
    screen: pg.Surface,
    origin: pg.Vector2,
    t: m.Transform,
    j: m.JoystickData,
    size: float,
):
    radius = size / 2
    pg.draw.circle(
        screen, "black", pgcoords(screen, t.translation), radius, ceil(size / 25)
    )
    pg.draw.circle(
        screen,
        "black",
        pgcoords(screen, t.translation),
        ceil(size / 25),
        ceil(size / 25),
    )

    if not pg.mouse.get_focused():
        return

    centered = j.xy - origin
    max_norm = (screen.get_width() / 2 + screen.get_height() / 2) / 2
    if centered.length() > max_norm:
        centered.scale_to_length(max_norm)

    as_unit_vec = centered / max_norm

    end_pos = t.translation + (as_unit_vec * radius)
    pg.draw.line(
        screen,
        "black",
        pgcoords(screen, t.translation),
        pgcoords(screen, end_pos),
    )

    # https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    font = pg.font.Font("freesansbold.ttf", 10)
    blit_text(
        screen,
        f"X{as_unit_vec.x:.2}\nY{as_unit_vec.y:.2f}",
        pgcoords(screen, t.translation + pg.Vector2(-size / 5, -size / 2)),
        font,
    )


def lighter_color(color: pg.Color, howmuch: float):
    # r, g, b =
    if type(color) is not pg.Color:
        color = pg.Color(color)
    r, g, b, a = color
    r += (255 - color.r) * howmuch
    g += (255 - color.g) * howmuch
    b += (255 - color.b) * howmuch
    return pg.Color(int(r), int(g), int(b), a)


def draw_gear(
    screen: pg.Surface, transform: m.Transform, radius: float, color: pg.Color
):
    color_with_transparency = pg.Color(color)
    color_with_transparency.a = 20
    pg.draw.circle(
        screen,
        # lighter_color(color, 0.85),
        color_with_transparency,
        pgcoords(screen, transform.translation),
        radius,
    )
    pg.draw.circle(
        screen,
        color,
        pgcoords(screen, transform.translation),
        radius,
        ceil(radius / 25),
    )

    tickpos = pg.Vector2.from_polar((radius, degrees(transform.rotation)))
    tickpos = tickpos if tickpos is not None else pg.Vector2(0)

    pg.draw.line(
        screen,
        color,
        pgcoords(screen, transform.translation),
        pgcoords(screen, transform.translation + tickpos),
        ceil(radius / 25),
    )


def blit_text(surface, text, pos, font, color=pg.Color("black")):
    # https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    # 2D array where each row is a list of words.
    words = [word.split(" ") for word in text.splitlines()]
    space, word_height = font.size(" ")
    max_width, _max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, _ = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def draw_gizmo(
    surface: pg.Surface,
    gizmo: m.Gizmo,
    transform: m.Transform,
    size=30,
    show_label=True,
):
    x, y = transform.translation
    pgc = lambda x, y: pgcoords(surface, (x, y))
    width = size // 10

    endx = transform.translation + pg.Vector2(size, 0).rotate_rad(transform.rotation)
    pg.draw.line(
        surface,
        "blue",
        pgc(x, y),
        pgc(*endx),
        width,
    )
    endy = transform.translation + pg.Vector2(0, size).rotate_rad(transform.rotation)
    pg.draw.line(
        surface,
        "red",
        pgc(x, y),
        pgc(*endy),
        width,
    )
    
    pg.draw.circle(surface, "black", pgc(x, y), width)
    
    if show_label:
        blit_text(
            surface,
            gizmo.label,
            pgc(x, y - width),
            pg.font.SysFont("Comic Sans MS", (size // 4) * 3),
        )


def draw_world_entities(surface, world: w.World, origin_offset: pg.Vector2, debug):
    for eid in range(world.last_id + 1):
        transform = world.abs_transform(eid).with_offset(origin_offset)
        if transform is None:
            continue  # not a drawable entity anyways.
        if (gear := world.gears[eid]) is not None:
            # pg.draw.circle(surface, color="black", center=transform.translation, radius=50)
            draw_gear(surface, transform=transform, radius=gear.radius, color=gear.color)
        if debug and (gizmo := world.gizmos[eid]) is not None:
            draw_gizmo(surface, gizmo=gizmo, transform=transform)
