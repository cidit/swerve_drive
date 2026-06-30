include <BOSL2/std.scad>

full_diameter = 150;

enclosure_side_thickness = 10;
gearbox_diameter = full_diameter - enclosure_side_thickness;

ring_thickness = 10;
diffy_gear_diameter = gearbox_diameter / 2;
inner_gear_diameter = diffy_gear_diameter - ring_thickness * 2;

shaft_radius = 8/2;

module gear_tree(diffy_gear_diameter, inner_gear_diameter) {
  union() {
    cylinder(h=10, r=diffy_gear_diameter / 2, center=true);
    up(10) cylinder(h=10, r=inner_gear_diameter / 2, center=true);
  }
}

module ring(id, od) {
  difference() {
    cylinder(h=10, r=od / 2, center=true);
    cylinder(h=11, r=id / 2, center=true);
  }
}

module shaft(){}

color("blue") {

  left(gearbox_diameter / 4) {
    gear_tree(diffy_gear_diameter, inner_gear_diameter);
    down(30) cylinder(h=50, r=shaft_radius);
  }

  zrot(120) left(gearbox_diameter/3){
    
    cylinder(h=40, r=shaft_radius, center=true);
  }

  zrot(240) left(gearbox_diameter/3){
    
    cylinder(h=40, r=shaft_radius, center=true);
  }

  up(10) ring(
      id=gearbox_diameter - ring_thickness * 2,
      od=gearbox_diameter + enclosure_side_thickness
    );
}
color("red") {
  right(gearbox_diameter / 4) {
    yrot(180) gear_tree(diffy_gear_diameter, inner_gear_diameter);
    down(10) cylinder(h=60, r=shaft_radius, center=true);
  }

  down(10) ring(
      id=gearbox_diameter - ring_thickness * 2,
      od=gearbox_diameter + enclosure_side_thickness
    );
}
