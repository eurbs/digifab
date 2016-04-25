translate([11, 11, 0]) {    
    difference() {
        cylinder(r=10, h=15, $fn=100);
        translate([0,0,-1])
            cylinder(r=5, h=17);
    }
}