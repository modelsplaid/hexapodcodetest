from    copy            import deepcopy
import warnings

class WalkDirType:
    WLK_FWD  = 'walkingforward' 
    WLK_BKWD = 'walkingbackward'
    ROT_LFT  = 'rotatingleft'  
    ROT_RHT  = 'rotatingright' 
    NO_MOV   = '' 
    WLK_LST  = [WLK_FWD,WLK_BKWD,ROT_LFT,ROT_RHT]
    __slots__ = ("curdir","_iter_idx_" )

    def __init__(self,cur_dir:str=''):
        """
        Set current direction
        0:'walkingforward' ,1:'walkingbackward',2: 'rotatingleft',3: 'rotatingright'
        """
        self.curdir = ''
        if cur_dir == '':
            self.curdir = ''
        else:
            self.set_cur_dir(cur_dir)
            
    def is_frwd(self)->bool:
        if self.curdir == self.WLK_FWD:
            return True
        else: 
            return False 

    def is_bkwd(self)->bool:
        if self.curdir == self.WLK_BKWD:
            return True
        else: 
            return False 

    def is_rotl(self)->bool:
        if self.curdir == self.ROT_LFT:
            return True
        else: 
            return False 
        
    def is_rotr(self)->bool:
        if self.curdir == self.ROT_RHT:
            return True
        else: 
            return False     

    def clone(self):
        """
        Clone a copy of self-object 
        """
        cls    = self.__class__
        result = cls.__new__(cls)
        # copy value 
        result.curdir     = deepcopy(self.curdir  )
        result._iter_idx_ = deepcopy(self._iter_idx_)

        return result

    def get_cur_dir(self)->str:
        """
        Get current direction
        return: 0:'walkingforward' ,1:'walkingbackward',2: 'rotatingleft',3: 'rotatingright'
        """
        return self.curdir
    
    def get_cur_dir(self)->str:
        """
        Get current direction index 
        index: 0:'walkingforward' ,1:'walkingbackward',2: 'rotatingleft',3: 'rotatingright'
        """
        for i in range(len(self.WLK_LST)):
            if self.WLK_LST[i] == self.curdir:
                return self.curdir
    
    def set_cur_dir(self,cur_dir_str:str='walkingforward' ):
        """
        param cur_dir_str: 'walkingforward' 'walkingbackward' 'rotatingleft' 'rotatingright'
        return: True: Setting successful. False: Failed to set 
        """
        for i in range(len(self.WLK_LST)):
            if self.WLK_LST[i] == cur_dir_str:
                self.curdir = cur_dir_str
                return True
        warnings.warn("Invalid value")
        return False

    def set_cur_dir_idx(self,dir_idx:int=0):
        """
        Set current direction by given dir_idx(direction index)
        param dir_idx: dir_idx is modulated based on len(self.WLK_LST)
        index: 0:'walkingforward' ,1:'walkingbackward',2: 'rotatingleft',3: 'rotatingright'
        """
        self.curdir = self.WLK_LST[dir_idx%len(self.WLK_LST)]

    def __str__(self):
        fstr= "Direction is: "+str(self.curdir)   
        return fstr
    
    def __eq__(self,obj):
        if isinstance(obj,str):
            if self.curdir == obj:
                return True
            else: 
                return False
        elif isinstance(obj,WalkDirType):
            if self.curdir == obj.curdir:
                return True
            else: 
                return False
        else: 
            return False

    def __iter__(self):
        self._iter_idx_ = 0
        return self
    
    def __next__(self)->str:
        if self._iter_idx_ < len(self.WLK_LST):
            dir_obj = self.clone()
            dir_obj.set_cur_dir(self.WLK_LST[self._iter_idx_])
            
            self._iter_idx_ += 1
            return dir_obj
        else:
            raise StopIteration     
           
if __name__ == "__main__":
    a = WalkDirType()
    a.set_cur_dir_idx(0)
    print(1)

    b = WalkDirType()
    b.set_cur_dir_idx(2)
    print(2)

    c = WalkDirType()
    c.set_cur_dir_idx(2)
    print(3)

    d = WalkDirType()
    d.set_cur_dir_idx(1)
    print(4)

    e = WalkDirType()
    e.set_cur_dir('walkingbackward')
    print(5)

    f = WalkDirType("undefined")
    print(6)
    g = WalkDirType()
    print(7)


    print("a==10: ", a==10)
    print("b==c: " , b==c)
    print("b==d: " , b==d)
    print("a==e: " , a==e)
    print("a==f: " , a==f)
    print("a==g: " , a==g)

    print(e==WalkDirType.WLK_BKWD)