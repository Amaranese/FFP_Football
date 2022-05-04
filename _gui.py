class gui():
    def __init__(self,screen,width,height,font):
        self.screen       = screen
        self.width        = width
        self.height       = height
        self.font         = font


        self.gameState    = 'ingame'
        self.userInput    = None # Loaded at runtime
        self.running      = True
        self.dt           = 0
        self.gameElapsed  = 0
        self.debugSwitch  = False
        self.mx           = 0
        self.my           = 0



    def debug(self,debugMessage):
        if(self.debugSwitch):
            print(debugMessage)

class fitbaObject():
    """
    takes in sprite classs from utils
    """
    def __init__(self,football):
        self.sprite  = football
        self.x       = self.sprite.x
        self.y       = self.sprite.y
        self.w       = self.sprite.w
        self.h       = self.sprite.h
        self.kick    = None
        self.kicked  = False
        self.kickSpd = 10
    
    def kickBall(self,kickDirection,inc=2):
        """
        self.kick is the direction, it needs resetting at the end
        """
        
        #print('self.kicked ' + str(self.kicked))
        #print('self.kick ' + str(self.kick))
        #print('kickDirection ' + str(kickDirection))
        #print('kickSpd ' + str(self.kickSpd))
        #print(' ')


        if(self.kicked):
            if(kickDirection=='down'): 
                self.y+=self.kickSpd
            if(kickDirection=='up'): 
                self.y-=self.kickSpd
            if(kickDirection=='left'): 
                self.x-=self.kickSpd
            if(kickDirection=='right'): 
                self.x+=self.kickSpd

            self.kickSpd -=1
            if(self.kickSpd<0.5):
                self.kicked  = False
                self.kickSpd = 10
                self.kick=None
    


    def updateSprite(self,gui):
        self.sprite.x,self.sprite.y = self.x,self.y
        self.sprite.animate(gui)

        if(self.kick!=None): self.kicked = True 
        
        self.kickBall(self.kick)
