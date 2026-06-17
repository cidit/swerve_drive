use bevy::color::palettes::css::*;
use bevy::color::palettes::tailwind::RED_100;
use bevy::prelude::*;
use bevy::reflect::DynamicTypePath;
use bevy_prototype_lyon::prelude::*;

const MAUVE: u32 = 0xff00ffff;

#[derive(Component)]
struct Gear {
    radius: f32,
    color: u32,
}

// #[derive(Component)]
// struct Gizmo(String);

fn spawn_gear_sys(mut cmd: Commands) {
    cmd.spawn((
        Gear {
            radius: 10.,
            color: MAUVE,
        },
        // Gizmo("gear a".to_owned()),
        Transform::from_xyz(0., 0., 0.),
        ShapeBundle {
            path: ShapePath::new().add(&shapes::Circle {
                radius: 50.,
                center: Vec2::ZERO,
            })
            .build(),
            ..Default::default()
        },
        Fill::color(RED),
        Stroke::new(RED_100, 5.)
    ));
}

fn main() {
    App::new()
        .add_plugins((DefaultPlugins, ShapePlugin))
        .add_systems(Startup, spawn_gear_sys)
        .run();
}
