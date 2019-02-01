import leveldb
import struct
import json
from NBTParser import NBTParser
import mcpe

class MCPERecord():
    pass

class MCPERecordSubChunkPrefix(MCPERecord):
    TagValue = 47
    
    def __init__(self, data):
        if data[0] == 1:
            self.bitsPerBlock = data[1] // 2
            blockDataOff = 2
        else:
            # this is version 8+, cdata[1] contains the number of storage groups in this cubic chunk (can be more than 1)        
            self.bitsPerBlock = data[2] // 2
            blockDataOff = 3
            
        self.blocksPerDword = 32 // self.bitsPerBlock
        totalDwords = (4096 + self.blocksPerDword - 1) // self.blocksPerDword
        offsetBlockInfoList = totalDwords * 4 + blockDataOff
        self.bitmask = (1<<self.bitsPerBlock) - 1
        self.dwdata = struct.unpack_from("<%dI"%(totalDwords), data, blockDataOff)
            
        blockidxsize = struct.unpack_from("<I", data, offsetBlockInfoList)[0]
        self.blockidx = []
        nbt = NBTParser(data)
        nbt.seek(offsetBlockInfoList + 4)
        for _ in range(blockidxsize):
            o=nbt.readobj()
            self.blockidx.append("%s:%d"%(o["name"], o["val"]))
        
    def getblockid(self, x, y, z):
        i = (((x*16) + z) * 16) + y;
        dwidx = i // self.blocksPerDword
        shift = (i % self.blocksPerDword) * self.bitsPerBlock
        v = (self.dwdata[dwidx] >> shift) & self.bitmask
        return self.blockidx[v]

class MCPEMap():
    
    def _getmapborder(self):
        x_min = 32767
        x_max = -32768
        z_min = 32767
        z_max = -32768
        for key in self.db.listkeys():
            #print(key)
            keylen = len(key)
            x, y, z, t, d = 0, 0, 0, 0, 0
            if key[3] != 0 and key[3] != 0xff:
                print(key)
                continue
            elif keylen == 9:
                x, z, t = struct.unpack("<iiB", key)
            elif keylen == 10:
                x, z, t, y = struct.unpack("<iiBB", key)
            elif keylen == 13:
                x, z, d, t = struct.unpack("<iiiB", key)
            elif keylen == 14:
                x, z, d, t, y = struct.unpack("<iiiBB", key)
            else:
                print("Unknown format: " + key)
                continue
            if x > x_max:
                x_max = x
            if x < x_min:
                x_min = x
            if z > z_max:
                z_max = z
            if z < z_min:
                z_min = z
            if not t in (0x2D, 0x2F, 0x31, 0x32, 0x36, 0x76, 0x35):
                print(key, t)
            
                
        self.border = [x_min, z_min, x_max - x_min + 1, z_max - z_min + 1]        
    
    
    def __init__(self, mapfolder):
        self.mapfolder = mapfolder
        self.db = mcpe.LevelDB()
        self.db.open(mapfolder + '\\db2')
        self._getmapborder()
        
    def readBlockData2DRecord(self, x, z):
        key = struct.pack("<iiB", x, z, 0x2D)
        data = self.db.get(key)
        if data == None:
            return None
        heightmap= list(struct.unpack_from("<256H", data, 0))
        biome = list(struct.unpack_from("<256B", data, 512))
        return heightmap, biome
        
    def readSubChunkPrefixRecord(self, x, y, z, d):
        if d == 0:
            key = struct.pack("<iiBB", x, z, 0x2F, y)
        else:
            key = struct.pack("<iiiBB", x, z, d, 0x2F, y)
        data = self.db.get(key)
        if data == None:
            return None
        return MCPERecordSubChunkPrefix(data)
    
    def readBlockEntityRecord(self, x, z):
        key = struct.pack("<iiB", x, z, 0x31)
        data = self.db.get(key)
        if data == None:
            return None
        nbt = NBTParser(data)
        return nbt.readobjlist()
    
    def readEntityRecord(self, x, z):
        key = struct.pack("<iiB", x, z, 0x32)
        data = self.db.get(key)
        if data == None:
            return None
        nbt = NBTParser(data)
        return nbt.readobjlist()
    
    def readPendingTicks(self, x, z):
        key = struct.pack("<iiB", x, z, 0x33)
        data = self.db.get(key)
        if data == None:
            return None
        nbt = NBTParser(data)
        return nbt.readobj()
    
            
#map = MCPEMap('LanGame-c5746dcb-5300-403b-88cd-223edbdb7e29')
#print(map.readPendingTicks(11, -3))
'''
block = map.readSubChunkPrefixRecord(1, 4, -1, 0)
for z in range(16):
    for x in range(16):
        print(block.getblockid(x, 0, z))
'''
parser = NBTParser(open("swrightsideupbackhalf", "rb").read(), '>')
print(json.dumps(parser.readobj(), indent=2))
