import subprocess
import sys
import re

import numpy as np

from math import sin, cos, radians, degrees
from sympy import Line, Point, Circle, Ray

stroke = "blue"
style = ""
width = "0.2"
R = 200

def xml_map_2_stl(xml_map):
    return 'g.stl'


def run_parser(stl_map_file):
    try:
        x = subprocess.run(["slic3r", "--load", "config.ini", stl_map_file])
        assert x.returncode == 0, ', '.join(["slic3r", "--scale", "20", "--load", "config.ini", stl_map_file])
        res = stl_map_file.replace(".stl",".gcode")
    except (FileNotFoundError, AssertionError) as e:
        print('error', e, file=sys.stderr)
        exit(1)
    return res


def extract_moves(gcode_map_file):
    x = [ x.strip() for x in open(gcode_map_file).readlines() ]
    y = [ x for x in x if x.startswith('G1 X') ]
    coordinates = []
    for move in y:
        p = [ float(x) for x in re.findall(r'.*?X(.*?)\sY(.*?) ', move)[0] ]
        coordinates += [p]

    coordinates_array = np.array(coordinates)
    delta = coordinates_array.min(axis=0)
    size = (coordinates_array - delta).max(axis=0)

    return coordinates_array - delta, size


def gcode_2_svg(gcode_map_file, start_pos):
    coordinates_array, size = extract_moves(gcode_map_file)
    p0 = np.array(start_pos)

    svg = f'''<svg version="1.1"
     baseProfile="full"
     width="{size[0]}" height="{size[1]}"
     xmlns="http://www.w3.org/2000/svg">
'''
    for p1 in coordinates_array:
        svg += f'''<line x1="{p0[0]}" y1="{p0[1]}" 
                        x2="{p1[0]}" y2="{p1[1]}"  
                        stroke="{stroke}" fill="transparent" 
                        style="{style}" stroke-width="{width}" />
'''
        p0 = p1

    svg += '''</svg>'''

    return svg

def get_coords_by_distance(distance, start_pos=(0,0), start_angle=0):
    coords = start_pos
    angle = start_angle + 90
    r = Ray(Point(start_pos), radians(angle))
    c = Circle(Point(start_pos), distance)
    stop_pos = r.intersection(c)
    print(stop_pos)

    return coords

def get_turn_coords():

    return 

def cmd_to_svg(cmds, start_pos=(0,0)):

    cmds = gcode_2_cmd(gcode_map_file, start_pos)

    size = (1000, 1000)
    svg = f'''<svg version="1.1"
     baseProfile="full"
     width="{size[0]}" height="{size[1]}"
     xmlns="http://www.w3.org/2000/svg">
    '''

    for c in cmds:
        action = c[0]
        value = int(c[1])
        if 'go' in action:
            print('Line')
        else:
            print('Turn')


    svg += '''</svg>'''

    return svg


def gcode_2_cmd(gcode_map_file, start_pos):
    coordinates_array, size = extract_moves(gcode_map_file)
    r = R
    x0, y0 = start_pos
    z0, z1 = 0, 0

    rez = []

    A = Point(x0, y0)
    B = Point(x0 + sin(radians(z0)), y0 + cos(radians(z0)))
    ab = Line(A, B)
    pp = ab.perpendicular_line(A)
    me = Circle(A, R)

    for p in coordinates_array[1:]:
        x1, y1 = (p * 1000).astype(int)
        C = Point(x1, y1)
        if A.distance(C) > R:
            D, E = [ x for x in pp.intersection(me) ]
            l, r = D.distance(C), E.distance(C)
            f, b = B.distance(C), A.distance(C)

            if abs(l - r) > 0.1 or f > b :
                # F = sorted([D, E], key=lambda x: x.distance(C))[0]
                k = 'left' if l < r else 'right'
                F = D if l < r else E
                tc = Circle(F, R)
                commands = []
                for tl in tc.tangent_lines(C):
                    p = tl.p2
                    l = Line(p, F)
                    if k == 'right':
                        z1 = round(degrees(l.angle_between(pp)))
                    else:
                        z1 = 180 - round(degrees(l.angle_between(pp)))
                    commands += [(f'{k} {z1}', f'go {round(p.distance(C) / 2)}')]
                commands = commands[0] if k == 'right' else commands[-1]
                rez += [" ".join(commands)]
            else:
                rez += [f'go {round(A.distance(C) / 2)}']
        else:
            rez += []

        x0, y0 = x1, y1
        z0 = z1
        A = Point(x0, y0)
        B = Point(x0 + sin(radians(z0)), y0 + cos(radians(z0)))
        ab = Line(A, B)
        pp = ab.perpendicular_line(A)
        me = Circle(A, R)

    return rez

def find_cleaning_path(xml_map, start_pos=(0,0)):
    stl_map_file = xml_map_2_stl(xml_map)
    gcode_map_file = run_parser(stl_map_file)
    svg_map = gcode_2_svg(gcode_map_file, start_pos)
    commands = gcode_2_cmd(gcode_map_file, start_pos)
    print(commands)
    return svg_map


if __name__ == '__main__':
    # gcode_2_svg('c.gcode')
    # xml_map = open('test.svg').read()
    svg = find_cleaning_path('xml_map', start_pos=(300,300))
    open('/tmp/test.svg','w').write(svg)