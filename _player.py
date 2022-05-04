class playerSprite():
    def __init__(self,imageFrames):
        self.imageFrames = imageFrames
        

        self.upF         = self.imageFrames[:3]
        self.downF       = self.imageFrames[3:6]
        self.rightF      = self.imageFrames[6:9]
        self.leftF       = self.imageFrames[9:12]

        self.liveFrames  = self.downF
        self.numFrames   = len(self.downF)





        self.framePos    = 0
        self.x           = 0
        self.y           = 0
        self.w           = self.imageFrames[0].get_rect().w
        self.h           = self.imageFrames[0].get_rect().h
        self.frameTime   = 0


        self.u           = False
        self.d           = False
        self.l           = False
        self.r           = False

        self.currentDirection   = None


    

    def getDirection(self,ang):

        direction = None
        if(ang.u): 
            direction = 'up'
            self.liveFrames = self.upF
        if(ang.d): 
            direction = 'down'
            self.liveFrames = self.downF
        if(ang.l): 
            direction = 'left'
            self.liveFrames = self.leftF
        if(ang.r): 
            direction = 'right'
            self.liveFrames = self.rightF

        return(direction)




    def animate(self,gui,ang,interval=0.2,stop=False):
        """
        animages image every interval (in seconds)
        once image reaches end, it resets to first image
        """

        # Update direction Frames
        direction = self.getDirection(ang)


        # --------change sprite templates
        if(self.currentDirection!=direction):
            self.currentDirection = direction
            self.framePos = 0
            self.numFrames = len(self.liveFrames)


        

        if(stop):
            gui.screen.blit(self.liveFrames[0],(self.x,self.y))
            return()
        

        #-----------animate
        # incremented timer
        self.frameTime += gui.dt/1000
        
        # increment frame when interval reached
        if(self.frameTime>=interval):
            self.framePos  +=1
            self.frameTime  = 0
        
        # wrap image around
        if(self.framePos>=self.numFrames): 
            self.framePos=0
        
        gui.screen.blit(self.liveFrames[self.framePos],(self.x,self.y))




class playerObject():
    """
    takes in playersprite classs from utils
    """
    def __init__(self,playerSprite,x,y,vx,vy):
        self.sprite  = playerSprite
        self.x       = x
        self.y       = y
        self.vx      = vx
        self.vy      = vy
        self.ballpos = []
        self.facing  = 'u'



    def dribble(self,colliding,fitba,inRange,gui,bounce=1):
        if(colliding):
            if(self.u): 
                fitba.y -= bounce*self.vy
            if(self.d): 
                fitba.y += bounce*self.vy
            if(self.l):  
                fitba.x -= bounce*self.vx
                fitba.y  = self.y + (0.6*self.sprite.h) # position ball
            if(self.r): 
                fitba.x += bounce*self.vx
                fitba.y  = self.y + (0.6*self.sprite.h) # position ball


        if(gui.userInput.kick and inRange):
            if(self.facing=='u'): fitba.kick  ='up'
            if(self.facing=='d'): fitba.kick  ='down'
            if(self.facing=='l'): fitba.kick  ='left'
            if(self.facing=='r'): fitba.kick  ='right'

    


        

    def inRange(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+pw
        playerLeftSide     = px-pw
        playerBottomSide   = py+1.5*ph
        playerTopSide      = py-0.5*ph
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)

    def collides(self,playerPos,otherObj):
        x,y,w,h = otherObj.x,otherObj.y,otherObj.w,otherObj.h
        px,py,pw,ph = playerPos[0],playerPos[1],self.sprite.w,self.sprite.h
        
        playerRightside    = px+0.5*pw
        playerLeftSide     = px-0.5*pw
        playerBottomSide   = py+ph
        playerTopSide      = py

        # get ball relative pos
        self.ballpos = []
        if(x>playerRightside): self.ballpos.append('l')
        if(x<playerLeftSide):  self.ballpos.append('r')
        if(y<playerTopSide):   self.ballpos.append('u')
        if(y>playerTopSide):   self.ballpos.append('d')

        # check if collides
        if x > playerLeftSide and x < playerRightside:
            if y > playerTopSide and y < playerBottomSide:
                return(True)
        return(False)
    
    def play_selected(self,gui,fitba):

        #self.sprite.animate(gui,stop=True)
        stop = (gui.userInput.up==False and gui.userInput.down==False and gui.userInput.left==False and gui.userInput.right==False)
        
        # Set Direction, set  velocity
        self.u,self.d,self.l,self.r = False,False,False,False
        # Manage Velocity
        if(gui.userInput.up):    
            self.y -= self.vy
            self.u = True
            self.facing = 'u'
        if(gui.userInput.down):  
            self.y += self.vy
            self.d = True
            self.facing = 'd'
        if(gui.userInput.left):  
            self.x -= self.vx
            self.l = True
            self.facing = 'l'
        if(gui.userInput.right): 
            self.x += self.vx
            self.r = True
            self.facing = 'r'

        # -------check if colliding
        colliding = self.collides((self.x,self.y),fitba)
        inRange   = self.inRange((self.x,self.y),fitba)
        
        # ------ dribble ball
        self.dribble(colliding,fitba,inRange,gui)
        
        # ------Animate
        self.sprite.animate(gui,self,stop=stop)

        # -------update position
        self.updateSprite(gui)

        #
        self.ballpos 

    def updateSprite(self,gui):
        self.sprite.x,self.sprite.y = self.x,self.y