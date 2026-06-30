include <BOSL2/std.scad>
include <BOSL2/gears.scad>


circ_pitch = 5;

dist = gear_dist(circ_pitch=circ_pitch, 20,20,30);

tooth_angle=360/20;

left(dist/2) zrot(90 + tooth_angle/2) {
    spur_gear(
        circ_pitch=circ_pitch, 
        teeth=20, 
        thickness=10, 
        helical=30, 
        herringbone=true, 
        slices=5
    );
    up(10) spur_gear(
        circ_pitch=circ_pitch, 
        teeth=15, 
        thickness=10, 
        helical=30, 
        herringbone=true, 
        slices=5
    );
}
right(dist/2) zrot(90) {
    spur_gear(
        circ_pitch=circ_pitch, 
        teeth=20, 
        thickness=10, 
        helical=-30, 
        herringbone=true, 
        slices=5
    );
}

up(10) zrot(94) ring_gear(
    circ_pitch=circ_pitch, 
    teeth=36,
    helical=-30, 
    herringbone=true
);
