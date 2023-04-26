import os
import shutil
from Structs import *
from rstools import RSoftCircuit

class Circuit:
    c = RSoftCircuit()
    dimension_y = 0
    ref_indexes = []
    ind_file=str
    out_file=str
    launch_field = ""
    pathway = ""
    monitor = ""

    first_l_f = True
    first_l_f_pos = 0
    first_l_f_power = 0

    def __init__(self, dimension=int, dimension_y=int, in_file_name=str, out_file_name=str, free_space_wavelength=None):
        self.ind_file = in_file_name + ".ind"
        self.out_file = out_file_name
        self.c.set_symbol("dimension", dimension)
        self.dimension_y = dimension_y
        if free_space_wavelength:
            self.c.set_symbol("free_space_wavelength", free_space_wavelength)

    def add_segment(self, pos=vec3, offset=vec3, dimension_x=int, index=float):
        self.c.add_segment(position=(pos.x, pos.y, pos.z), offset=(offset.x, offset.y, offset.z), dimensions=(dimension_x, self.dimension_y))
        self.ref_indexes.append(index)

    def add_pathway(self, segments =[str]): # segments = string array
        for i in range(len(segments)):
            self.pathway += ("\t" + segments[i] + "\n")
        self.pathway += "/"
    
    def add_monitor(self, pathway=int, type=monitor_type, tilt=str, component=monitor_component):
        self.monitor += "pathway = " + str(pathway) + "\n\tmonitor_type = " + str(type) + "\n\tmonitor_tilt = " + str(tilt) + "\n\tmonitor_component = " + str(component) + "\n/"

    def add_lauch_field(self, x, power, launch_type, launch_pathway, launch_tilt):
        if self.first_l_f:
            self.first_l_f = False
            self.first_l_f_pos = x
            self.first_l_f_power = power
        self.launch_field += "launch_pathway = " + str(launch_pathway) + "\n\tlaunch_type = " + str(launch_type) + "\n\tlaunch_tilt = " + str(launch_tilt) + "\n\tlaunch_position = " + str(x) + "\n\tlaunch_power = " + str(power) + "/"

    def run_simulation(self):
        try:
            if os.path.exists(os.getcwd() + "\\res"):
                shutil.rmtree(os.getcwd() + "\\res")
            os.mkdir(os.getcwd() + "\\res")
            os.mkdir(os.getcwd() + "\\res\\ind")
            os.mkdir(os.getcwd() + "\\res\\sim")
            if len(self.launch_field) > 0:
                self.c.set_symbol("launch_position", self.first_l_f_pos)
                self.c.set_symbol("launch_power", self.first_l_f_power)
            self.c.write("res\\ind\\" + self.ind_file)
            with open(name="res\\ind\\" + self.ind_file, mode="r") as OGfile:
                with open(name="res\\ind\\temp_" + self.ind_file, mode="w") as MODfile:
                    i = 0
                    while has_another_line(OGfile):
                        readString = OGfile.readline()
                        if readString.startswith("segment"):
                            MODfile.write(readString)
                            MODfile.write("\tbegin.delta = " + str(self.ref_indexes[i]) + "-background_index\n")
                            MODfile.write("\tend.delta = " + str(self.ref_indexes[i]) + "-background_index\n")
                            i += 1
                        else:
                            MODfile.write(readString)
                    pw = self.pathway.split("/")
                    for i in range(len(pw) - 1):
                        MODfile.write("pathway " + str(i+1) + "\n" + pw[i] + "end pathway\n")

                    mo = self.monitor.split("/")
                    for i in range(len(mo) - 1):
                        MODfile.write("\nmonitor " + str(i+1) + "\n\t" + mo[i] + "end monitor\n")

                    lf = self.launch_field.split("/")
                    for i in range(len(lf) - 1):
                        MODfile.write("\nlaunch_field " + str(i+1) + "\n\t" + lf[i] + "\nend launch_field\n")
            os.remove(os.getcwd() + "\\res\\ind\\" + self.ind_file)
            os.rename(os.getcwd() + "\\res\\ind\\temp_" + self.ind_file, os.getcwd() + "\\res\\ind\\" + self.ind_file)
            os.system("bsimw32 " + "res\\ind\\" + self.ind_file + " prefix=res\\sim\\" + self.out_file + " slice_display_mode=0")
            
            if os.path.exists(os.getcwd() + "\\res\\sim\\" + self.out_file + ".mon"):
                with open(name="res\\sim\\" + self.out_file + ".mon", mode="r") as OGfile:
                    value = OGfile.readlines()[-1].split(" ")
                    value[len(value)-1] = value[len(value)-1].replace("\n", "")
                    value.pop(0)
                    return value
        except OSError as error: 
            print(error) 

def has_another_line(file):
    cur_pos = file.tell()
    does_it = bool(file.readline())
    file.seek(cur_pos)
    return does_it
