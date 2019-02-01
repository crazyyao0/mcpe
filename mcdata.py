from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import json
import numpy as np
import ctypes

class BlockRender():
    def __init__(self, config):
        self.textures = config["textures"]
        if "alphablend" in config:
            self.alphablend = config["alphablend"]
        else:
            self.alphablend = False
        self.definemodel()
    
    def modelmatrix(self, data):
        pass
    
    def definemodel(self):
        self.databuf = np.array([
            # front
             0.5,  0.5,  0.5, 1, 1, -0.5,  0.5,  0.5, 0, 1, -0.5, -0.5,  0.5, 0, 0,
            -0.5, -0.5,  0.5, 0, 0,  0.5, -0.5,  0.5, 1, 0,  0.5,  0.5,  0.5, 1, 1,
            # back                   
             0.5,  0.5, -0.5, 0, 1,  0.5, -0.5, -0.5, 0, 0, -0.5, -0.5, -0.5, 1, 0, 
            -0.5, -0.5, -0.5, 1, 0, -0.5,  0.5, -0.5, 1, 1,  0.5,  0.5, -0.5, 0, 1,
            # left                   
            -0.5,  0.5,  0.5, 1, 1, -0.5,  0.5, -0.5, 0, 1, -0.5, -0.5, -0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 0, -0.5, -0.5,  0.5, 1, 0, -0.5,  0.5,  0.5, 1, 1,
            # right                   
             0.5,  0.5,  0.5, 0, 1,  0.5, -0.5,  0.5, 0, 0,  0.5, -0.5, -0.5, 1, 0,
             0.5, -0.5, -0.5, 1, 0,  0.5,  0.5, -0.5, 1, 1,  0.5,  0.5,  0.5, 0, 1,
            # top                   
             0.5,  0.5,  0.5, 1, 0,  0.5,  0.5, -0.5, 1, 1, -0.5,  0.5, -0.5, 0, 1,
            -0.5,  0.5, -0.5, 0, 1, -0.5,  0.5,  0.5, 0, 0,  0.5,  0.5,  0.5, 1, 0,
            #bottom                   
             0.5, -0.5,  0.5, 1, 1, -0.5, -0.5,  0.5, 0, 1, -0.5, -0.5, -0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 0,  0.5, -0.5, -0.5, 1, 0,  0.5, -0.5,  0.5, 1, 1,
        ], dtype="float32")
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.databuf) * 4, self.databuf, GL_STATIC_DRAW)
        self.nvertex=36
    
    def rendermodel(self, data):
        if data > len(self.textures):
            data = 0
        glBindTexture(GL_TEXTURE_2D, self.textures[data])
        glDrawArrays(GL_TRIANGLES, 0, self.nvertex)
            
    def render(self, x, y, z, data):
        glPushMatrix()
        glTranslatef(x+0.5, y+0.5, z+0.5)
        self.modelmatrix(data)
        if self.alphablend:
            glEnable(GL_BLEND);
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glAlphaFunc(GL_GREATER, 0.5);
            glEnable(GL_ALPHA_TEST);
        glEnable(GL_TEXTURE_2D)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 20, ctypes.c_void_p(0))
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glTexCoordPointer(2, GL_FLOAT, 20, ctypes.c_void_p(12))
        self.rendermodel(data)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
        if self.alphablend:
            glDisable(GL_BLEND)
        
class GrassRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)
        self.toptext = self.textures[0]
        self.sidetext = self.textures[1]
        self.bottomtext = self.textures[2]
    
    def rendermodel(self, data):
        glBindTexture(GL_TEXTURE_2D, self.sidetext)
        glDrawArrays(GL_TRIANGLES, 0, 24)
        glBindTexture(GL_TEXTURE_2D, self.toptext)
        glDrawArrays(GL_TRIANGLES, 24, 6)
        glBindTexture(GL_TEXTURE_2D, self.bottomtext)
        glDrawArrays(GL_TRIANGLES, 30, 6)

class LogRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)
        
    def rendermodel(self, data):
        logid = data % 4
        facing = data >> 2
        sidetxt = self.textures[logid*2]
        toptxt = self.textures[logid*2 + 1]
        if facing == 3:
            toptxt = sidetxt     
        glBindTexture(GL_TEXTURE_2D, sidetxt)
        glDrawArrays(GL_TRIANGLES, 0, 24)
        glBindTexture(GL_TEXTURE_2D, toptxt)
        glDrawArrays(GL_TRIANGLES, 24, 12)
    
    def modelmatrix(self, data):
        facing = data >> 2
        if facing == 1:
            glRotatef(90, 0, 0, 1.0)
        elif facing == 2:
            glRotatef(90, 1.0, 0, 0)

class StrippedLogRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)
        
    def rendermodel(self, data):
        sidetxt = self.textures[0]
        toptxt = self.textures[1]
        if data == 3:
            toptxt = sidetxt
        glBindTexture(GL_TEXTURE_2D, sidetxt)
        glDrawArrays(GL_TRIANGLES, 0, 24)
        glBindTexture(GL_TEXTURE_2D, toptxt)
        glDrawArrays(GL_TRIANGLES, 24, 12)
    
    def modelmatrix(self, data):
        if data == 1:
            glRotatef(90, 0, 0, 1.0)
        elif data == 2:
            glRotatef(90, 1.0, 0, 0)
            
class CrossRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)
    
    def definemodel(self):
        self.databuf = np.array([
             0.5, 0.5,-0.5,1,1, -0.5, 0.5, 0.5,0,1, -0.5,-0.5, 0.5,0,0,
            -0.5,-0.5, 0.5,0,0,  0.5,-0.5,-0.5,1,0,  0.5, 0.5,-0.5,1,1,
             0.5, 0.5, 0.5,1,1, -0.5, 0.5,-0.5,0,1, -0.5,-0.5,-0.5,0,0,
            -0.5,-0.5,-0.5,0,0,  0.5,-0.5, 0.5,1,0,  0.5, 0.5, 0.5,1,1,
        ], dtype="float32")
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(self.databuf) * 4, self.databuf, GL_STATIC_DRAW)
        self.nvertex=12

class DispenserRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)

    def rendermodel(self, data):
        fronttxt = self.textures[0]
        sidetxt = self.textures[1]
        toptxt = self.textures[2]
        glBindTexture(GL_TEXTURE_2D, fronttxt)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindTexture(GL_TEXTURE_2D, sidetxt)
        glDrawArrays(GL_TRIANGLES, 6, 18)
        glBindTexture(GL_TEXTURE_2D, toptxt)
        glDrawArrays(GL_TRIANGLES, 24, 12)
    
    def modelmatrix(self, data):
        facing = data % 8
        if facing == 0:  #facing down
            glRotatef(90, 1, 0, 0)
        elif facing == 1:#facing up
            glRotatef(270, 1, 0, 0)
        elif facing == 2:#facing north
            glRotatef(180, 0, 1, 0)
        elif facing == 3:#facing south
            pass
        elif facing == 4:#facing west
            glRotatef(270, 0, 1, 0)
        elif facing == 5:#facing east
            glRotatef(90, 0, 1, 0)
  
class SandstoneRender(BlockRender):
    def __init__(self, config):
        super().__init__(config)

    def rendermodel(self, data):
        if data > 2:
            data = 0
        toptxt = self.textures[0]
        sidetxt = self.textures[data+1]
        glBindTexture(GL_TEXTURE_2D, sidetxt)
        glDrawArrays(GL_TRIANGLES, 0, 24)
        glBindTexture(GL_TEXTURE_2D, toptxt)
        glDrawArrays(GL_TRIANGLES, 24, 12)
            
class MCData():
    def _load_texture(self, filename):        
        textureSurface = pygame.image.load("images/" + filename).convert_alpha()
        textureData = pygame.image.tostring(textureSurface,"RGBA",1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()
        texid = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texid)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return texid
    
    def __init__(self):
        self.conf = json.loads(open("blocks.json").read())
        self.textures = {}
        self.renders = {}
        
        for name, config in self.conf.items():
            t = []
            for filename in config["textures"]:
                if not filename in self.textures:
                    self.textures[filename] = self._load_texture(filename)
                t.append(self.textures[filename])
                config["textures"] = t
        
        for name, config in self.conf.items():
            render = globals()[config["class"]](config)
            self.renders[name] = render
        