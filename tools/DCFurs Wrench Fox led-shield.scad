// Reverse-engineered and parameterized version of oskirby's shades for
// the DC26 DCFURS Wrench Fox badge:
// https://github.com/oskirby/dc26-fur-scripts/blob/master/tools/led-shield.stl


$fn = 64;           // raise for higher detail

$WINDOWSCALE = 1.2; // increase to allow more room for variances in SMD position
$TAPERSCALE = 1;    // taper multiplier for front face, a value of 1 is a
                    // straight-walled hole, a value of 1.5 approximates the
                    // orignal taper (with simpler geometry)
$HASCLIP = true;    // print side clips to hold shades to board
$TYPE = 1;          // cutout type:
                    //   1 = SMD grid holes
                    //   2 = "dive goggles"
                    //   3 = outline
                    //   4 = horizontal slats
                    //   5 = full horizontal slats
                    //   6 = vertical slats


module fillet(r, h) {
    translate([r / 2, r / 2, 0])

        difference() {
            cube([r + 0.01, r + 0.01, h], center = true);

            translate([r / 2, r / 2, 0])
                cylinder(r = r, h = h + 1, center = true);

        }
}

// SMD sizes (LWH)
// 603 package   1.55, 0.85, 0.45
// 603 pad       (0.6 * 2) + 0.9, 0.9, n/a
// 0.55 pad slack
module smd(xlist = [0 : 8], ylist = [0 : 6]) {    
    for(y = ylist) {
        for(x = xlist) {
            if(!(
                ((x == 0) && ((y == 0) || (y == 6))) ||
                ((x == 7) && ((y == 5) || (y == 6))) ||
                ((x == 8) && ((y == 5) || (y == 6))) ||
                ((x == 6) && (y == 6))
                )) {
                translate([4.25 + 5.5 * x, 2.95 + 4.253 * y, 1.2 / 2]) {
                    rotate([180, 0, 45]) {
                        hull() {
                            scale([1.6 * $WINDOWSCALE, 1.3 * $WINDOWSCALE, 1]) {
                                linear_extrude(height = 1.21, center = true, slices = 24, scale = $TAPERSCALE) {
                                        square([0.9, ((0.6 * 2) + 0.9) - 0.9], center = true);
                                        translate([0, ((0.6 * 2) + 0.9) / 2 - 0.9 / 2, 0])
                                            circle(d = 0.9, center = true);
                                        translate([0, -(((0.6 * 2) + 0.9) / 2 - 0.9 / 2), 0])
                                            circle(d = 0.9, center = true);
                                }
                            }
                        }
                        // solder pad land pattern template
//                        %translate([0, 0, (-0.9 + 1.2 / 2) + 0.45 /2]) { cube([0.9, (0.6 * 2) + 0.9, 0.45], center = true); }
                    }
                }
            }
        }
    }
}

module clip() {
    difference() {
        union() {
            translate([0, 11.5, 0])
                cube([4, 11, 1.2]);
            translate([0, 11.5, 0])
                cube([3, 11, 1.2 + 2]);
            // attempt a minor friction fit while doing a cheeky 50-degree overhang
            difference() {
                translate([0, 11.5, 1.2 + 2.1 - 0.2])
                    cube([3.8, 11, 1.2]);
                
                translate([3, 10.5, 1.2 + 2.1 - 0.2])
                    rotate([0, 60, 0])
                        cube([1.2, 13, 1.5]);
            }
        }
        // radius corners
        translate([0, 11, ((1.2 + 2.1 + 1.2) + 2) / 2  - 1])
            rotate([0, 0, 0])
                fillet(4.5, (1.2 + 2.1 + 1.2) + 2);
        translate([0, 11 + 12, 5 / 2 - 1])
            rotate([0, 0, -90])
                fillet(4.5, (1.2 + 2.1 + 1.2) + 2);
    }
}

module halfshade() {
    difference() {
        translate([0, 0, 0]) { cube([102 / 2, 32, 1.2]); }

        // top corner
        translate([0, 0, (1.2 + 2) / 2 - 1])
            rotate([0, 0, 0])
               fillet(8, 1.2 + 2);
        // bottom corner
        translate([0, 32, (1.2 + 2) / 2 - 1])
            rotate([180, 0, 0])
                fillet(10, 1.2 + 2);
        // nosepiece
        translate([102 / 2, 47.08, (1.2 + 2) / 2 - 1])
            scale([1, 1.08, 1])
            cylinder(d = 42.8, h = 1.2 + 2, center = true);
        difference() {
            union() {
                translate([47, 32, (1.2 + 2) / 2 - 1])
                    rotate([180, 180, 0])
                        fillet(20, 1.2 + 2);
                translate([55, 32, (1.2 + 2) / 2 - 1])
                    rotate([180, 0, 0])
                        fillet(20, 1.2 + 2);
            }
            
            translate([(102 / 2), 18, (1.2 + 2) / 2 - 1])
                cube([50, 20, 1.2 + 2], center = true);
        }
    }

    if($HASCLIP) { 
        translate([-3.8, 0, 0])
            clip();
    }
}


// MAIN
//translate([0, 16.3, 17.5]) { import("led-shield.stl"); }
difference () {
    union() {
        halfshade();
        translate([101.999, 0, 0]) {
            mirror([1, 0, 0]) {
                halfshade();
            }
        }
    }

    // SMD grid holes
    if($TYPE == 1) {
        smd();
        translate([101.999, 0, 0]) {
            mirror([1, 0, 0]) {
                smd();
            }
        }
    }
    // "dive goggles"
    else if($TYPE == 2) {
        hull() {
            smd();
        }
        hull() {
            translate([101.999, 0, 0]) {
                mirror([1, 0, 0]) {
                    smd();
                }
            }
        }
    }
    // outline
    else if($TYPE == 3) {
        translate([(102 - (102 * 0.96)) / 2, (32 - (32 * 0.90)) / 2 - 0.1, -1]) {
            scale([.96, .897, 2]) {
                $HASCLIP = false;
                halfshade();
                translate([101.999, 0, 0]) {
                    mirror([1, 0, 0])
                        halfshade();
                }
            }
        }
    }
    // horizontal slats
    else if($TYPE == 4) {
        for(ylist = [0 : 6]) {
            hull() {
                smd([0, 1, 5, 6, 8], ylist);
            }
            translate([101.999, 0, 0]) {
                mirror([1, 0, 0]) {
                    hull() {
                        smd([0, 1, 5, 6, 8], ylist);
                    }
                }
            }
        }
    }
    // full horizontal slats
    else if($TYPE == 5) {
        for(ylist = [0 : 6]) {
            if(ylist < 5 ) {
                hull() {
                    smd([0, 1], ylist);
                    translate([101.999, 0, 0]) {
                        mirror([1, 0, 0]) {
                            smd([0, 1], ylist);
                        }
                    }
                }
            }
            else {
                hull() {
                    smd([0, 1, 5, 6], ylist);
                }
                hull() {
                    translate([101.999, 0, 0]) {
                        mirror([1, 0, 0]) {
                            smd([0, 1, 5, 6], ylist);
                        }
                    }
                }
            }
        }
    }
    // vertical slats
    else if($TYPE == 6) {
        for(xlist = [0 : 8]) {
            hull() {
                smd(xlist, [0 : 6]);
            }
            translate([101.999, 0, 0]) {
                mirror([1, 0, 0]) {
                    hull() {
                        smd(xlist, [0 : 6]);
                    }
                }
            }
        }
    }
}