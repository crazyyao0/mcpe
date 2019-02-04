import os
from OpenGL.GL import *
from OpenGL.GLU import *
import tkinter as tk
import mcdata
import mcfunction
import math
from ctypes import WinDLL, c_void_p
from ctypes.wintypes import HDC
from OpenGL.WGL import PIXELFORMATDESCRIPTOR, ChoosePixelFormat, SetPixelFormat, SwapBuffers, wglCreateContext, wglMakeCurrent

class OpenGLFrame(tk.Frame):
    def __init__(self, *args, **kw):
        tk.Frame.__init__( self, *args, **kw )

    def InitOpenGLContext(self):
        _user32 = WinDLL('user32')
        GetDC = _user32.GetDC
        GetDC.restype = HDC
        GetDC.argtypes = [c_void_p]
        pfd = PIXELFORMATDESCRIPTOR()
        PFD_TYPE_RGBA =         0
        PFD_MAIN_PLANE =        0
        PFD_DOUBLEBUFFER =      0x00000001
        PFD_DRAW_TO_WINDOW =    0x00000004
        PFD_SUPPORT_OPENGL =    0x00000020
        pfd.dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_DOUBLEBUFFER
        pfd.iPixelType = PFD_TYPE_RGBA
        pfd.cColorBits = 24
        pfd.cDepthBits = 16
        pfd.iLayerType = PFD_MAIN_PLANE
        
        self.hwnd = self.winfo_id()
        self.hdc = GetDC(self.hwnd)
        pixelformat = ChoosePixelFormat(self.hdc, pfd)
        SetPixelFormat(self.hdc, pixelformat, pfd)
        self.hrc = wglCreateContext(self.hdc)
        self.OpenGLActiveContext()
        self.OpenGLResizeViewport()
        
    def OpenGLActiveContext(self):
        wglMakeCurrent(self.hdc, self.hrc)
    
    def OpenGLResizeViewport(self):
        self.wndsize = (float(self.winfo_width()), float(self.winfo_height()))
        glViewport(0, 0, self.winfo_width(), self.winfo_height())
    
    def SwapBuffer(self):
        SwapBuffers(self.hdc)
        
        
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
        
    def MouseMove(self, event):
        self.label1.config(text = "(%d,%d)"%(event.x, event.y))
        vx = (event.x * 2 - self.mainglwnd.wndsize[0])/self.mainglwnd.wndsize[0] * self.scale
        vy = -(event.y * 2 - self.mainglwnd.wndsize[1])/self.mainglwnd.wndsize[1] * self.scale
        tx = -math.cos(math.radians(self.hr))
        ty = -math.sin(math.radians(self.hr))
        tx1 = tx/math.sin(math.radians(self.vr))*vy
        ty1 = ty/math.sin(math.radians(self.vr))*vy
        self.mousex = math.floor(-ty * vx + tx1)
        self.mousey = math.floor(tx * vx + ty1)
        
        self.label2.config(text = "(%d,%d)"%(self.mousex, self.mousey))
        
    def run(self):
        self.root = tk.Tk()
        self.mainglwnd = OpenGLFrame(self.root, width = 600, height = 600) #creates embed frame for pygame window
        self.mainglwnd.grid(columnspan = (600), rowspan = 600) # Adds grid
        self.mainglwnd.pack(side = tk.LEFT) #packs window to the left
        self.mainglwnd.bind('<Motion>',self.MouseMove)
        
        self.controlpanel = tk.Frame(self.root, width = 400, height = 600)
        self.controlpanel.pack(side = tk.LEFT)
        
        self.label1 = tk.Label(self.controlpanel, text="", width = 10, height = 1)
        self.label1.grid(row = 0, column=0, columnspan=3)
        self.label2 = tk.Label(self.controlpanel, text="", width = 10, height = 1)
        self.label2.grid(row = 1, column=0, columnspan=3)
        
        tk.Button(self.controlpanel, width = 3, height = 1, text ="⇑", command=lambda:setattr(self, "vr", 90 if self.vr + 15 > 90 else self.vr + 15)).grid(row=2, column=0)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="↑", command=self._moveforward).grid(row=2, column=1)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="⇓", command=lambda:setattr(self, "vr", 0 if self.vr - 15 < 0 else self.vr - 15)).grid(row=2, column=2)
        
        tk.Button(self.controlpanel, width = 3, height = 1, text ="←", command=self._moveleft).grid(row=3, column=0)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="⃝", command=self._resetview).grid(row=3, column=1)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="→", command=self._moveright).grid(row=3, column=2)
        
        tk.Button(self.controlpanel, width = 3, height = 1, text ="↳", command=lambda:setattr(self, "hr", self.hr + 15)).grid(row=4, column=0)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="↓", command=self._movebackward).grid(row=4, column=1)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="↲", command=lambda:setattr(self, "hr", self.hr - 15)).grid(row=4, column=2)
        
        
        tk.Button(self.controlpanel, width = 3, height = 1, text ="▲", command=lambda:setattr(self, "top", self.top + 1)).grid(row=5, column=0)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="▼", command=lambda:setattr(self, "top", self.top - 1)).grid(row=5, column=1)
        
        tk.Button(self.controlpanel, width = 3, height = 1, text ="+", command=lambda:setattr(self, "scale", self.scale / 1.1)).grid(row=6, column=0)
        tk.Button(self.controlpanel, width = 3, height = 1, text ="-", command=lambda:setattr(self, "scale", self.scale * 1.1)).grid(row=6, column=1)
        
        self.root.update()        
        self.mainglwnd.InitOpenGLContext()
        
        self.hr = 60
        self.vr = 45
        self.centerx = 0
        self.centery = 0
        self.centerz = 0
        self.scale = 10
        self.top = 0
        
        self.mcdata = mcdata.MCData()
        self.root.after(100, self.openglmain)
        self.root.mainloop()

    def DrawAxis(self):
        glEnable(GL_LINE_SMOOTH)
        glLineWidth(1)
        glBegin(GL_LINES)
        glColor3f(0.3,0.3,0.3)
        for i in range(-16, 17):
            glVertex3f(i, self.top + 0.01, -16)
            glVertex3f(i, self.top + 0.01, 17)
            glVertex3f(-16, self.top + 0.01, i)
            glVertex3f(17, self.top + 0.01, i)
        glEnd()
        
        glLineWidth(3)
        glColor3f(1,0,0)
        glBegin(GL_LINES)
        glVertex3f(0.51, self.top + 0.01, 0.51)
        glVertex3f(1.51, self.top + 0.01, 0.51)
        
        glColor3f(0,1,0)
        glVertex3f(0.51, self.top + 0.01, 0.51)
        glVertex3f(0.51, self.top + 1.01, 0.51)

        glColor3f(0,0,1)
        glVertex3f(0.51, self.top + 0.01, 0.51)
        glVertex3f(0.51, self.top + 0.01, 1.51)
        glColor3f(1,1,1)
        glEnd()

    def RedrawAll(self):
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        glEnable(GL_DEPTH_TEST)

        self.DrawAxis()
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
                  self.centery + 50*math.sin(math.radians(self.vr)) + self.top + 0.01,
                  self.centerz + 50*math.cos(math.radians(self.vr))*math.sin(math.radians(self.hr)),
                  self.centerx, self.centery + self.top + 0.01, self.centerz,
                  -math.cos(math.radians(self.hr)),1,-math.sin(math.radians(self.hr)))
        self.RedrawAll()
        self.mainglwnd.SwapBuffer()
        self.root.after(100, self.openglmain)

GameWindow().run()