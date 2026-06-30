$fn = 72;

// TODO: make herringbone by sandwiching two helical on top of each other? constrain on hex shaft
// TODO: add second stage with interlocked sun gear

include <BOSL2/std.scad>
include <BOSL2/gears.scad>
include <BOSL2/ball_bearings.scad>

inner_diameter = 100; // aka, pitch diameter

modulus = 2.5;

// modulus * teeth_count = circumf
// circumf / PI = diam
max_teeth_count = floor(inner_diameter / 2 * PI / modulus);

echo(max_teeth_count);

n = 4;

bearing_info = ball_bearing_info(trade_size="608ZZ");
gear_data = planetary_gears(
  mod=modulus,
  n=n,
  max_teeth=max_teeth_count,
  sun_ring=2,
  gear_spin=360 / 27 * $t
);

echo(gear_data);
echo("sun teeth", gear_data[0][1]);
echo("sun teeth", gear_data[1][1]);
echo("total", (gear_data[0][1] + gear_data[1][1]));
echo("is uniform?", ( (gear_data[0][1] + gear_data[1][1]) / n) % 2 == 0);

module planetary() {

  ring_gear(
    mod=modulus,
    teeth=gear_data[1][1],
    profile_shift=gear_data[1][2],
    gear_spin=gear_data[1][3],
    backing=4,
    thickness=7
  );

  color("blue") {
    move_copies(
      gear_data[2][4]
    )
      cyl(
        h=12,
        d=4
      );
    down(9)
      linear_extrude(height=3)
        scale(1.2)
          polygon(gear_data[2][4]);
  }

  ball_bearing("608ZZ");
  spur_gear(
    mod=modulus,
    teeth=gear_data[0][1],
    profile_shift=gear_data[0][2],
    gear_spin=gear_data[0][3],
    thickness=5,
    shaft_diam=bearing_info[1]
  );
  //sun

  move_copies(gear_data[2][4]) {
    ball_bearing("608ZZ");
    color("red")
      spur_gear(
        mod=modulus,
        teeth=gear_data[2][1],
        profile_shift=gear_data[2][2],
        gear_spin=gear_data[2][3][$idx],
        thickness=5,
        shaft_diam=bearing_info[1]
      );
  }
}



left(24) bevel_gear(
    circ_pitch=5,
    teeth=35,
    mate_teeth=36,
    shaft_diam=5,
    spiral=1
);
right(24) xrot(180) bevel_gear(
    circ_pitch=5,
    teeth=35,
    mate_teeth=36,
    shaft_diam=5,
    // spiral=0,
    anchor="flattop"
);
