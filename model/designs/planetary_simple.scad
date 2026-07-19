$fn = 24;
$slop = 0.1;

// TODO: make herringbone by sandwiching two helical on top of each other? constrain on hex shaft
// TODO: add second stage with interlocked sun gear

include <BOSL2/std.scad>
include <BOSL2/gears.scad>
include <BOSL2/ball_bearings.scad>

bearing_type = "608ZZ";
max_ring_pitch_diameter = 120;
modulus = 2;
helical = 30;
height = 15;

%cuboid([180, 180, 180]);

// modulus = pitch_diam / teeth -> teeth = pitch_diam / modulus
max_teeth_count = floor(max_ring_pitch_diameter / modulus);
num_planets = 4;

bearing_info = ball_bearing_info(trade_size="608ZZ");
bearing_info_id = bearing_info[0];
bearing_info_od = bearing_info[1];
bearing_info_w = bearing_info[2];

// ["sun", teeth, profile_shift, spin]
// ["ring", teeth, profile_shift, spin]
// ["planets", teeth, profile_shift, spins, positions, angles]
// ["ratio", realized_ratio]
gear_data = planetary_gears(
  mod=modulus,
  n=num_planets,
  max_teeth=max_teeth_count,
  helical=helical,
  sun_ring=2.2,
  gear_spin=360 / 27 * $t
);

echo(gear_data);
assert(
  ( (gear_data[0][1] + gear_data[1][1]) / num_planets) % 2 == 0,
  "the planets are not uniformly spaced."
);

ring_root_radius = outer_radius(mod=modulus, teeth=gear_data[1][1], helical=helical);
planetary_gear_drive_radius = ceil(ring_root_radius / 10) * 10; // round to the cm up

module stage(
  thickness = bearing_info_w,
  backlash = .1,
  shaft_idx,
  anchor = CENTER,
  spin = 0,
  orient = UP
) {
  attachable(h=thickness, r=planetary_gear_drive_radius, anchor=anchor, spin=spin, orient=orient) {
    ring_gear(
      mod=modulus,
      teeth=gear_data[1][1],
      profile_shift=gear_data[1][2],
      gear_spin=gear_data[1][3],
      helical=helical,
      herringbone=true,
      // backing=4, 
      or=planetary_gear_drive_radius,
      backlash=backlash,
      thickness=bearing_info_w,
          $gear_steps=2,
    ) {

      diff()
        spur_gear(
          mod=modulus,
          teeth=gear_data[0][1],
          profile_shift=gear_data[0][2],
          gear_spin=gear_data[0][3],
          helical=helical,
          herringbone=true,
          thickness=bearing_info_w,
          shaft_diam=0,
          backlash=backlash,
          $gear_steps=2,
        ) tag("remove") rex_shaft(h=bearing_info_w + 1, $slop=0.01);

      
      move_copies(gear_data[2][4])
        diff()
          spur_gear(
            mod=modulus,
            teeth=gear_data[2][1],
            profile_shift=gear_data[2][2],
            helical=-helical,
            gear_spin=gear_data[2][3][$idx],
            herringbone=true,
            thickness=bearing_info_w,
            shaft_diam=$idx != shaft_idx ? bearing_info_od : 0,
            backlash=backlash,
          $gear_steps=2,
          ) if ($idx == shaft_idx) {
            tag("remove") rex_shaft(h=bearing_info_w + 1, $slop=0.01);
          } else if ($preview) {
            // ball_bearing("608ZZ");
          }
    }
    children();
  }
}

module rex_shaft(h, $slop = 0) {
  flat2flat = ( (7 / 2) / cos(30)) * 2;
  intersection() { cyl(h=h, d=8 + $slop); cyl(h=h, d=flat2flat + $slop, $fn=6); };
}

module washer(anchor = CENTER, spin = 0, orient = UP) {
  attachable(anchor=anchor, spin=spin, orient=orient, d=19, h=1.2) {
    diff()
      cyl(h=1.2, d=19)
        tag("remove") cyl(h=2, d=8.9);
    children();
  }
}

module chassis_plate(anchor = CENTER, spin = 0, orient = UP, thickness = 5) {
  attachable(anchor, spin, orient, h=thickness, r=planetary_gear_drive_radius) {
    diff()
      cyl(h=thickness, r=planetary_gear_drive_radius) tag("remove") cyl(h=thickness + 1, d=bearing_info_od) move_copies(gear_data[2][4]) cyl(h=thickness + 1, d=bearing_info_od);
    children();
  }
}

// module stack_children() {
//   for (c_idx = [0:$children]) {
//     children(c_idx);
//   }
// }

// chassis_plate();
// up(20) washer() move_copies(gear_data[2][4]) washer();
// up (40) stage();
// up(60) washer() move_copies(gear_data[2][4]) washer();
// up(80) stage();
// up(100) chassis_plate();

chassis_plate()
  attach(TOP, BOT) washer()
    let (save_pt = parent()) move_copies(gear_data[2][4]) washer() restore(save_pt)
          attach(TOP, BOT)
            stage()
              attach(TOP, BOT) washer()
              let (save_pt = parent()) move_copies(gear_data[2][4]) washer() restore(save_pt)
                      attach(TOP, BOT) stage()
                          attach(TOP, BOT) washer()
                          let (save_pt = parent()) move_copies(gear_data[2][4]) washer();
// move_copies(gear_data[2][4]) rex_shaft(h=bearing_info_w * 5);
