from Cad import Circuit
from Structs import *

def main():
    c1 = Circuit(dimension=2, dimension_y=3, in_file_name="design", out_file_name="result")

    c1.add_segment(pos=vec3(0, 0, 0), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(2, 0, 0), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(4, 0, 0), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(6, 0, 0), offset=vec3(0, 0, 1), dimension_x=1, index=2)

    c1.add_segment(pos=vec3(3, 0, 1), offset=vec3(0, 0, 7), dimension_x=7, index=2)
    
    for i in [float(k) / 2 for k in range(4, 14, 1)]:
        for j in[float(l) / 2 for l in range(1, 12, 1)]:
            c1.add_segment(pos=vec3(j, 0, i), offset=vec3(0, 0, 0.5), dimension_x=0.5, index=3)

    c1.add_segment(pos=vec3(0, 0, 8), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(2, 0, 8), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(4, 0, 8), offset=vec3(0, 0, 1), dimension_x=1, index=2)
    c1.add_segment(pos=vec3(6, 0, 8), offset=vec3(0, 0, 1), dimension_x=1, index=2)

    for i in range(1,5):
        c1.add_pathway([str(10*11+5+i)])
    
    c1.add_monitor(1, monitor_type.MONITOR_WGMODE_POWER, "1", monitor_component.COMPONENT_MINOR)
    c1.add_monitor(2, monitor_type.MONITOR_WGMODE_POWER, "1", monitor_component.COMPONENT_MINOR)
    c1.add_monitor(3, monitor_type.MONITOR_WGMODE_POWER, "1", monitor_component.COMPONENT_MINOR)
    c1.add_monitor(4, monitor_type.MONITOR_WGMODE_POWER, "1", monitor_component.COMPONENT_MINOR)
    
    c1.add_lauch_field(0, 1, launch_type.LAUNCH_WGMODE, 0, 1)
    c1.add_lauch_field(2, 1, launch_type.LAUNCH_WGMODE, 0, 1)
    c1.add_lauch_field(4, 1, launch_type.LAUNCH_WGMODE, 0, 1)
    c1.add_lauch_field(6, 1, launch_type.LAUNCH_WGMODE, 0, 1)
    
    print(c1.run_simulation())

main()