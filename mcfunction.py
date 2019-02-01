

class MCFunction():
    def __init__(self):
        self.blocks = {}
    
    def _setblock(self, x, y, z, name, data, replacetileonly="", replacedata=-1):
        key = "%d,%d,%d"%(x,y,x)
            
        if name == "air":
            if key in self.blocks:
                if replacetileonly == "":
                    del self.blocks[key]
                elif self.blocks[key][3] == replacetileonly and (replacedata == -1 or replacedata == self.blocks[key][4]):
                    del self.blocks[key]
        else:
            if replacetileonly != "":
                if key in self.blocks and self.blocks[key][3] == replacetileonly and (replacedata == -1 or replacedata == self.blocks[key][4]):
                    self.blocks[key] = [x, y, z, name, data]
            else:
                self.blocks[key] = [x, y, z, name, data]
                
    def dosetblock(self, seps):
        coor = [s.strip("~") for s in seps[1:4]]
        A = [0 if s == "" else int(s) for s in coor]
        name = seps[4]
        if name.startswith("minecraft:"):
            name = name[10:]        
        data = 0
        mode = "replace"
        if len(seps) > 5:
            data = int(seps[5])
        if len(seps) > 6:
            mode = seps[6]
        if mode == "replace" or mode == "destroy":
            self.setblock(A[0],A[1],A[2], name, data)
        else:
            self.setblock(A[0],A[1],A[2], name, data, "air")
    
    def dofill(self, seps):
        coor = [s.strip("~") for s in seps[1:7]]
        coor = [0 if s == "" else int(s) for s in coor]
        A = [coor[0], coor[1], coor[2]]
        B = [coor[3], coor[4], coor[5]]
        if B[0] > A[0]:
            A[0], B[0] = B[0], A[0]
        if B[1] > A[1]:
            A[1], B[1] = B[1], A[1]
        if B[2] > A[2]:
            A[2], B[2] = B[2], A[2]
        name = seps[7]
        if name.startswith("minecraft:"):
            name = name[10:]
            
        data = 0
        mode = "replace"
        replacename = ""
        replacedata = -1
        if len(seps) > 8:
            data = int(seps[8])
        if len(seps) > 9:
            mode = seps[9]
        if len(seps) > 10:
            replacename = seps[10] 
        if len(seps) > 11:
            replacedata = seps[11]
            
        for x in range(A[0], B[0]+1):
            for y in range(A[1], B[1]+1):
                for z in range(A[2], B[2]+1):
                    if mode == "replace":                            
                        self.setblock(x, y, z, name, data, replacename, replacedata)
                    elif mode == "destroy":
                        self.setblock(x, y, z, name, data)
                    elif mode == "keep":
                        self.setblock(x, y, z, name, data, "air")
                    elif mode == "hollow":
                        if x == A[0] or x == B[0] or y == A[1] or y == B[1] or z == A[2] or z == B[2]:
                            self.setblock(x, y, z, name, data)
                        else:
                            self.setblock(x, y, z, "air", data)
                    elif mode == "outline":
                        if x == A[0] or x == B[0] or y == A[1] or y == B[1] or z == A[2] or z == B[2]:
                            self.setblock(x, y, z, name, data)
    
    def doclone(self, seps):
        coor = [s.strip("~") for s in seps[1:10]]
        coor = [0 if s == "" else int(s) for s in coor]
        A = [coor[0], coor[1], coor[2]]
        B = [coor[3], coor[4], coor[5]]
        C = [coor[6], coor[7], coor[8]]
        if B[0] > A[0]:
            A[0], B[0] = B[0], A[0]
        if B[1] > A[1]:
            A[1], B[1] = B[1], A[1]
        if B[2] > A[2]:
            A[2], B[2] = B[2], A[2]
                      
    def decode(self, line):
        seps = line.strip().split(" ")
        if seps[0] == "fill":
            self.dofill(seps)
        elif seps[0] == "setblock":
            self.dosetblock(seps)
        elif seps[0] == "clone":
            self.doclone(seps)
            
    def loadfile(self, filename):
        for line in open(filename):
            self.blocks += self.decode(line)
