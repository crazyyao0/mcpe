import struct

class NBTParser:
    NBT_TAG_End = 0
    NBT_TAG_Byte = 1
    NBT_TAG_Short = 2
    NBT_TAG_Int = 3
    NBT_TAG_Long = 4
    NBT_TAG_Float = 5
    NBT_TAG_Double = 6
    NBT_TAG_Byte_Array = 7
    NBT_TAG_String = 8
    NBT_TAG_List = 9
    NBT_TAG_Compound = 10
    NBT_TAG_Int_Array = 11
    NBT_TAG_Long_Array = 12
    
    def _readbyte(self):
        c = self.buf[self.pos]
        self.pos += 1
        return c
    
    def _readint(self):
        l = struct.unpack_from(self.endian+"i", self.buf, self.pos)[0]
        self.pos += 4
        return l
    
    def _readstring(self):
        l = struct.unpack_from(self.endian+"H", self.buf, self.pos)[0]
        s = self.buf[self.pos+2:self.pos+2+l].decode("utf-8")
        self.pos += 2 + l
        return s
    
    def parse_value(self, t):
        if t == self.NBT_TAG_Byte:
            return self._readbyte()
        elif t == self.NBT_TAG_Short:
            l = struct.unpack_from(self.endian+"h", self.buf, self.pos)[0]
            self.pos += 2
            return l
        elif t == self.NBT_TAG_Int:
            return self._readint()
        elif t == self.NBT_TAG_Long:
            l = struct.unpack_from(self.endian+"q", self.buf, self.pos)[0]
            self.pos += 8
            return l
        elif t == self.NBT_TAG_Float:
            l = struct.unpack_from(self.endian+"f", self.buf, self.pos)[0]
            self.pos += 4
            return l
        elif t == self.NBT_TAG_Double:
            l = struct.unpack_from(self.endian+"d", self.buf, self.pos)[0]
            self.pos += 8
            return l
        elif t == self.NBT_TAG_Byte_Array:
            l = struct.unpack_from(self.endian+"I", self.buf, self.pos)[0]
            s = self.buf[self.pos+4:self.pos+4+l]
            self.pos += 4 + l
            return s
        elif t == self.NBT_TAG_String:
            return self._readstring()
        elif t == self.NBT_TAG_List:
            ret = []
            tt = self._readbyte()
            ll = self._readint()
            for _ in range(ll):
                ret.append(self.parse_value(tt))
            return ret
        elif t == self.NBT_TAG_Compound:
            ret = {}
            while True:
                tt = self._readbyte()
                if tt == self.NBT_TAG_End:
                    break
                nn = self._readstring()
                ret[nn] = self.parse_value(tt)
            return ret
        elif t == self.NBT_TAG_Int_Array:
            ll = self._readint()
            ret = list(struct.unpack_from(self.endian+"%dI"%(ll), self.buf, self.pos + 4))
            self.pos += 4 + ll * 4
            return ret
        elif t == self.NBT_TAG_Long_Array:
            ll = self._readint()
            ret = list(struct.unpack_from(self.endian+"%dQ"%(ll), self.buf, self.pos + 4))
            self.pos += 4 + ll * 8
            return ret
        else:
            raise Exception("unsupported NTB TAG value")            
    
    def __init__(self, buf, endian='<'):
        self.endian = endian
        self.buf = buf
        self.pos = 0
        
    def seek(self, pos):
        self.pos = pos
    
    def readobj(self):
        t = self._readbyte()
        self._readstring()
        return self.parse_value(t)
    
    def readobjlist(self):
        ret = []
        while True:
            try:
                ret.append(self.readobj())
            except:
                break
        return ret