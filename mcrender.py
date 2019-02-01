import pygame
import os
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
import mcdata


class GameWindow(): 
    def __init__(self):
        pass
    
    def run(self):
        self.root = tk.Tk()
        embed = tk.Frame(self.root, width = 600, height = 600) #creates embed frame for pygame window
        embed.grid(columnspan = (600), rowspan = 600) # Adds grid
        embed.pack(side = tk.LEFT) #packs window to the left
        self.controlpanel = tk.Frame(self.root, width = 400, height = 600)
        self.controlpanel.pack(side = tk.LEFT)
        
        
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        screen = pygame.display.set_mode((600,600))
        screen.fill(pygame.Color(255,255,255))
        pygame.display.init()
        pygame.display.update()
        self.root.update()
        pygame.display.set_mode((500,500), DOUBLEBUF|OPENGL)
        
        self.mcdata = mcdata.MCData()
        self.rotate = 0
        self.scale = 10
        
        self.root.after(10, self.openglmain)
        self.root.mainloop()

    def Cube(self):
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)

        glBegin(GL_LINES)
        for i in range(-8, 9):
            glVertex3f(i, 0, -8)
            glVertex3f(i, 0, 8)
            glVertex3f(-8, 0, i)
            glVertex3f(8, 0, i)
        glEnd()
        
        block = self.mcdata.renders["log"]
        block.render(0,0,0,1)
        block.render(3,0,0,2)
        block = self.mcdata.renders["leaves"]
        block.render(0,1,0,0)
        block = self.mcdata.renders["dispenser"]
        block.render(1,0,0,3)        
        block = self.mcdata.renders["sandstone"]
        block.render(2,0,0,1)
            
    def openglmain(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotate += 15
        if keys[pygame.K_RIGHT]:
            self.rotate -= 15
        if keys[pygame.K_UP]:
            self.scale /= 1.1
        if keys[pygame.K_DOWN]:
            self.scale *= 1.1
        
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-1*self.scale, self.scale, -1*self.scale, self.scale, 0.1, self.scale*100)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(32,32,32,0,0,0,0,1,0)
        glRotatef(self.rotate, 0, 1, 0)
        self.Cube()
        pygame.display.flip()
        self.root.after(100, self.openglmain)

GameWindow().run()