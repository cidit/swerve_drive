// intended to press fit a bearing in the middle of printing

include <BOSL2/std.scad>
include <BOSL2/gears.scad>
include <BOSL2/ball_bearings.scad>

module encrusted_bearing(name = "608ZZ") {
  bi = ball_bearing_info(name);
  difference() {
    children();
    cyl(d=bi[1], h=bi[2]);
  }
}

module encrusted_nut(){
  flat2flat = 12.8;
  a = flat2flat/2;
  r = a/cos(30);
  difference() {
    children();
    cyl(r=r, h=7, $fn=6);
  }
}

