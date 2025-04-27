# pyshade.py

import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np

class ShaderPostProcessor:
    DEFAULT_VERTEX_SHADER = """
    #version 330
    in vec2 position;
    out vec2 texCoords;
    
    void main()
    {
        texCoords = (position + 1.0) * 0.5;
        gl_Position = vec4(position, 0.0, 1.0);
    }
    """

    DEFAULT_FRAGMENT_SHADER = """
    #version 330
in vec2 texCoords;
out vec4 fragColor;

uniform sampler2D screenTexture;
uniform float time;

float rand(vec2 co){
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    vec2 uv = texCoords;
    
    // Add random horizontal band offset
    float glitch = rand(vec2(time * 0.5, uv.y * 10.0)) * 0.02;
    uv.x += glitch;

    // RGB Split (different offsets per channel)
    float r = texture(screenTexture, uv + vec2(0.003, 0.0)).r;
    float g = texture(screenTexture, uv + vec2(0.0, 0.0)).g;
    float b = texture(screenTexture, uv + vec2(-0.003, 0.0)).b;

    fragColor = vec4(r, g, b, 1.0);
}

    """

    def __init__(self, surface_size, fragment_shader_source=None):
        self.width, self.height = surface_size

        # Compile shader
        fragment_src = fragment_shader_source or self.DEFAULT_FRAGMENT_SHADER
        self.program = self._create_shader_program(self.DEFAULT_VERTEX_SHADER, fragment_src)
        glUseProgram(self.program)

        # Setup fullscreen quad
        vertices = np.array([
            -1, -1,
             1, -1,
            -1,  1,
            -1,  1,
             1, -1,
             1,  1,
        ], dtype=np.float32)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        position = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 2, GL_FLOAT, GL_FALSE, 0, None)

    def _compile_shader(self, shader_type, source):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            raise RuntimeError(glGetShaderInfoLog(shader).decode())
        return shader

    def _create_shader_program(self, vertex_src, fragment_src):
        program = glCreateProgram()
        vertex_shader = self._compile_shader(GL_VERTEX_SHADER, vertex_src)
        fragment_shader = self._compile_shader(GL_FRAGMENT_SHADER, fragment_src)
        glAttachShader(program, vertex_shader)
        glAttachShader(program, fragment_shader)
        glLinkProgram(program)
        if not glGetProgramiv(program, GL_LINK_STATUS):
            raise RuntimeError(glGetProgramInfoLog(program).decode())
        return program

    def _surface_to_texture(self, surface):
        data = pygame.image.tostring(surface, "RGB", True)
        tex = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex

    def render(self, surface, time=0.0):
        tex = self._surface_to_texture(surface)

        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.program)

        # If shader has 'time' uniform, pass it
        time_loc = glGetUniformLocation(self.program, "time")
        if time_loc != -1:
            glUniform1f(time_loc, time)

        glBindTexture(GL_TEXTURE_2D, tex)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        glDeleteTextures([tex])

