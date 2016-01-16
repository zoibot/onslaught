import pygame

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays.vbo import *

class GfxObject(object):
    pos = 0,0
    angle = 0
    vbo = None
    tex_vbo = None
    active = False

next_id = 0
objects = {}
def create_object(geometry, close_loop = True):
    global next_id
    id = next_id
    next_id += 1
    obj = GfxObject()
    obj.vbo, obj.tex_vbo = create_geometry(geometry, close_loop)
    objects[id] = obj
    return id
def destroy_object(id):
    del objects[id]
def show_object(id, show):
    objects[id].active = show
def set_transform(id, pos, angle):
    obj = objects[id]
    obj.pos = pos
    obj.angle = angle

class TextObject(object):
    pos = 0,0
    angle = 0
    active = False
    str = ''

next_text_id = 0
text_objects = {}
def create_text():
    global next_text_id
    id = next_text_id
    next_text_id += 1
    obj = TextObject()
    text_objects[id] = obj
    return id
def destroy_text(id):
    del text_objects[id]
def show_text(id, show):
    text_objects[id].active = show
def set_text_transform(id, pos, angle):
    obj = text_objects[id]
    obj.pos = pos
    obj.angle = angle
def set_text(id, str):
    text_objects[id].str = str

VS = """
#version 120

// Main function, which needs to set `gl_Position`.
void main()
{
    vec4 position = gl_ModelViewProjectionMatrix * gl_Vertex;
    gl_Position = position;
    gl_TexCoord[0] = gl_MultiTexCoord0;
}
"""

FS = """
#version 120 

// Main fragment shader function.
void main()
{
    //vec4 position = gl_FragCoord;
    vec4 tex = gl_TexCoord[0];
    float l = tex.p;
    float i = 0.3-abs(0.6*(tex.s-.5)) + 0.7/(pow(30*(tex.s-0.5),2) + 1);
    //float e = 0.5*i/(pow(tex.t-5,2) + 1);
    float e = 0;
    float s = min(((l/4 - 2)-abs(0.5*(tex.t-(l/2)))/(0.1*i)), 1);
    gl_FragColor = 1/*s*/ * (e+i) * vec4(0.1,1,0.1,1);
}
"""

vbo = None
vbo2 = None
program = None

def init():
    init_pygame()
    init_shaders()
    init_gl()
    init_text()

def init_pygame():
    # TODO refactor
    pygame.init()
    pygame.display.set_mode((640,480), pygame.OPENGL|pygame.DOUBLEBUF)

def init_shaders():
    global program
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, VS)
    glCompileShader(vertex_shader)
    result = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if not(result):
        raise RuntimeError(glGetShaderInfoLog(vertex_shader))
    
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, FS)
    glCompileShader(fragment_shader)
    result = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if not(result):
        raise RuntimeError(glGetShaderInfoLog(fragment_shader))
    
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

def init_gl():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0,640,480,0)

    glClearColor(0, 0, 0, 1)

def create_geometry(lines, close_loop):
    #TODO transform into triangles surrounding lines in geometry shader instead of here
    def lines_from_points(points):
        if close_loop:
            return list(zip(points, points[1:])) + [(points[-1], points[0])]
        else:
            return list(zip(points, points[1:]))
    
    dest_array = np.zeros((2 * 3 * len(lines), 3), dtype='f')
    tex_array = np.zeros((2 * 3 * len(lines), 3), dtype='f')
    i = 0
    for start, end in lines_from_points(lines):
        # 1. get perp. left hand vector
        # 2. add and subtract unit? amount from each point
        #TODO 3. need to also add and subtract in length direction for ends
        v = end - start
        vn = v / np.linalg.norm(v)
        s = start# - 5 * vn
        e = end# + 5 * vn
    
        perp = np.array([v[1], -v[0], 0])
        perp = perp / np.linalg.norm(perp)
        off = perp * 20 
    
        l = np.linalg.norm(v)
    
        dest_array[i+0] = s - off
        tex_array[i+0] = np.array([0,0,l])
        dest_array[i+1] = e + off
        tex_array[i+1] = np.array([1,l,l])
        dest_array[i+2] = e - off
        tex_array[i+2] = np.array([0,l,l])
        dest_array[i+3] = s - off
        tex_array[i+3] = np.array([0,0,l])
        dest_array[i+4] = s + off
        tex_array[i+4] = np.array([1,0,l])
        dest_array[i+5] = e + off
        tex_array[i+5] = np.array([1,l,l])
        i += 6
    
    return VBO(dest_array), VBO(tex_array)

digits_lines = [
# 0
[[-5,8],[5,8],[5,-8],[-5,-8],[-5,8]],
# 1
[[5,8],[5,-8]],
# 2
[[5,8],[-5,8],[-5,0],[5,0],[5,-8],[-5,-8]],
# 3
[[-5,8],[5,8],[5,0],[-5,0],[5,0],[5,-8],[-5,-8]],
# 4
[[5,8],[5,-8],[5,0],[-5,0],[-5,-8]],
# 5
[[-5,8],[5,8],[5,0],[-5,0],[-5,-8],[5,-8]],
# 6
[[-5,0],[-5,8],[5,8],[5,0],[-5,0],[-5,-8],[5,-8]],
# 7
[[5,8],[5,-8],[-5,-8]],
# 8
[[-5,8],[5,8],[5,-8],[-5,-8],[-5,0],[5,0],[-5,0],[-5,8]],
# 9
[[5,8],[5,-8],[-5,-8],[-5,0],[5,0]],
]
digits = []
def init_text():
    for lines in digits_lines:
        np_lines = np.array([[x,y,1] for [x,y] in lines])
        digits.append(create_object(np_lines, False))

def cleanup():
    for id, obj in objects.iteritems():
        del obj.vbo
        del obj.tex_vbo

def loop():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)

    for id, obj in objects.iteritems():
        if not obj.active:
            continue

        glPushMatrix()
        glTranslated(obj.pos[0], obj.pos[1], 0)
        glRotated(obj.angle, 0, 0, 1)

        vbo = obj.vbo
        vbo2 = obj.tex_vbo
        vbo.bind()
        glVertexPointerf(vbo)

        vbo2.bind()
        glTexCoordPointerf(vbo2)
 
        glDrawArrays(GL_TRIANGLES, 0, len(vbo))

        glPopMatrix()

    for id, obj in text_objects.iteritems():
        if not obj.active:
            continue

        glPushMatrix()
        glTranslated(obj.pos[0], obj.pos[1], 0)
        glRotated(obj.angle, 0, 0, 1)

        for char in obj.str:
            digit_obj = objects[digits[int(char)]]
            vbo = digit_obj.vbo
            vbo2 = digit_obj.tex_vbo
            vbo.bind()
            glVertexPointerf(vbo)

            vbo2.bind()
            glTexCoordPointerf(vbo2)
 
            glDrawArrays(GL_TRIANGLES, 0, len(vbo))
            glTranslated(15, 0, 0)

        glPopMatrix()

    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)

    pygame.display.flip()
