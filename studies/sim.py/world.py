import model as m
import pygame as pg


class World:
    INITIAL_SIZE = 100
    world_id: m.EntityId = 0
    last_id = 0

    # ECS style
    parents: list[m.Parent | None] = [None] * INITIAL_SIZE
    transforms: list[m.Transform | None] = [None] * INITIAL_SIZE
    gears: list[m.Gear | None] = [None] * INITIAL_SIZE
    gizmos: list[m.Gizmo | None] = [None] * INITIAL_SIZE

    def __init__(self):
        """this base constructor initializes the first entity as being the world itself. its a special entity because it has no parent"""
        self.parents[self.world_id] = None
        self.transforms[self.world_id] = m.Transform(pg.Vector2(), 0)

    def spawn(self, *components: list) -> m.EntityId:
        self.last_id += 1

        print(f"spawning entity id:{self.last_id} with components \n\t[{components}]")
        for component in components:
            match type(component):
                case m.Parent:
                    self.parents[self.last_id] = component
                case m.Transform:
                    self.transforms[self.last_id] = component
                case m.Gear:
                    self.gears[self.last_id] = component
                case m.Gizmo:
                    self.gizmos[self.last_id] = component
        return self.last_id

    def get_parents(self, id: m.EntityId) -> list[m.Parent]:
        parents: list[m.Parent] = []
        current_id = id
        while True:
            parent = self.parents[current_id]
            if parent is not None:
                parents.append(parent)
                current_id = parent.id
            else:
                break
        return parents

    def abs_transform(self, id: m.EntityId) -> m.Transform:

        parents = reversed(self.get_parents(id))
        parent_ids = [p.id for p in parents]

        transforms = map(lambda id: self.transforms[id], parent_ids + [id])

        total_rotation = 0.0
        total_translation = pg.Vector2()

        for t in transforms:
            assert t != None
            total_translation += t.translation.rotate_rad(total_rotation)
            total_rotation += t.rotation

        return m.Transform(total_translation, total_rotation)
