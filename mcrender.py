import pygame
import os
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
import mcdata
import mcfunction
import math

class GameWindow(): 
    def __init__(self):
        self.state = 0
        self.script = mcfunction.MCFunction()
        self.script.loadfile("functions/test.mcfunction")
        print(self.script.blocks)
    
    def _moveforward(self):
        self.centerx += math.cos(math.radians(self.hr))
        self.centerz += math.sin(math.radians(self.hr))
    def _movebackward(self):
        self.centerx -= math.cos(math.radians(self.hr))
        self.centerz -= math.sin(math.radians(self.hr))
    def _moveleft(self):
        self.centerx += math.sin(math.radians(self.hr))
        self.centerz -= math.cos(math.radians(self.hr))
    def _moveright(self):
        self.centerx -= math.sin(math.radians(self.hr))
        self.centerz += math.cos(math.radians(self.hr))
    def _resetview(self):
        self.hr = 45
        self.vr = 45
        self.centerx = 0
        self.centery = 0
        self.centerz = 0
        self.scale = 10
        self.top = 0        
        
    def run(self):
        self.root = tk.Tk()
        embed = tk.Frame(self.root, width = 600, height = 600) #creates embed frame for pygame window
        embed.grid(columnspan = (600), rowspan = 600) # Adds grid
        embed.pack(side = tk.LEFT) #packs window to the left
        self.controlpanel = tk.Frame(self.root, width = 400, height = 600)
        self.controlpanel.pack(side = tk.LEFT)
        
        tk.Button(self.controlpanel, width = 2, height = 1, text ="⇑", command=lambda:setattr(self, "vr", 90 if self.vr + 15 > 90 else self.vr + 15)).grid(row=0, column=0)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="↑", command=self._moveforward).grid(row=0, column=1)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="⇓", command=lambda:setattr(self, "vr", 0 if self.vr - 15 < 0 else self.vr - 15)).grid(row=0, column=2)
        
        tk.Button(self.controlpanel, width = 2, height = 1, text ="←", command=self._moveleft).grid(row=1, column=0)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="⃝", command=self._resetview).grid(row=1, column=1)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="→", command=self._moveright).grid(row=1, column=2)
        
        tk.Button(self.controlpanel, width = 2, height = 1, text ="↳", command=lambda:setattr(self, "hr", self.hr + 15)).grid(row=2, column=0)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="↓", command=self._movebackward).grid(row=2, column=1)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="↲", command=lambda:setattr(self, "hr", self.hr - 15)).grid(row=2, column=2)
        
        
        tk.Button(self.controlpanel, width = 2, height = 1, text ="▲", command=lambda:setattr(self, "top", self.top + 1)).grid(row=3, column=0)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="▼", command=lambda:setattr(self, "top", self.top - 1)).grid(row=3, column=1)
        
        tk.Button(self.controlpanel, width = 2, height = 1, text ="+", command=lambda:setattr(self, "scale", self.scale / 1.1)).grid(row=4, column=0)
        tk.Button(self.controlpanel, width = 2, height = 1, text ="-", command=lambda:setattr(self, "scale", self.scale * 1.1)).grid(row=4, column=1)
        
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        screen = pygame.display.set_mode((600,600))
        screen.fill(pygame.Color(255,255,255))
        pygame.display.init()
        pygame.display.update()
        self.root.update()
        pygame.display.set_mode((500,500), DOUBLEBUF|OPENGL)
        
        self.mcdata = mcdata.MCData()
        self.hr = 60
        self.vr = 45
        self.centerx = 0
        self.centery = 0
        self.centerz = 0
        
        self.scale = 10
        self.top = 0
        
        self.root.after(10, self.openglmain)
        self.root.mainloop()

    def Cube(self):
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glBegin(GL_LINES)
        glColor3f(0.3,0.3,0.3)
        for i in range(-16, 17):
            glVertex3f(i, self.top + 0.01, -18)
            glVertex3f(i, self.top + 0.01, 18)
            glVertex3f(-18, self.top + 0.01, i)
            glVertex3f(18, self.top + 0.01, i)
        glColor3f(1,0,0)
        glVertex3f(0,self.top + 0.01,0)
        glVertex3f(20,self.top + 0.01,0)
        
        glColor3f(0,1,0)
        glVertex3f(0,self.top + 0.01,0)
        glVertex3f(0,self.top + 0.01,20)
        
        glColor3f(1,1,1)
        glEnd()
        glDepthFunc(GL_LESS)
        blocklist = [item for item in self.script.blocks.values() if item[1]<=self.top]
        self.mcdata.renderlist(blocklist)
        '''
        block = self.mcdata.renders["log"]
        block.render(0,0,0,1)
        block.render(3,0,0,2)
        block = self.mcdata.renders["stone_slab"]
        block.render(0,1,0,8)
        block = self.mcdata.renders["dispenser"]
        block.render(1,0,0,3)        
        block = self.mcdata.renders["sandstone"]
        block.render(2,0,0,1)
        ''' 
    def openglmain(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1*self.scale, self.scale, -1*self.scale, self.scale, 0.1, self.scale*100)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.centerx + 50*math.cos(math.radians(self.vr))*math.cos(math.radians(self.hr)),
                  self.centery + 50*math.sin(math.radians(self.vr)),
                  self.centerz + 50*math.cos(math.radians(self.vr))*math.sin(math.radians(self.hr)),
                  self.centerx,self.centery,self.centerz,0,1,0)
        self.Cube()
        pygame.display.flip()
        self.root.after(100, self.openglmain)

GameWindow().run()