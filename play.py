# play.py
# Samuel Han (sh779) and Neha Rao (nr276)
# 12/4/16
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    ball_count
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBricks(self):
        """ This method serves as a getter to access self._bricks
        from module Play
        """
        return self._bricks
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """ Initializer: creates bricks, the paddle, and the ball
        Calls on helper method _createBrick() to create the bricks
        """
        self._bricks = []
        self._createBrick(self._bricks)
        
        self._paddle = Paddle(x = GAME_WIDTH/2, y = PADDLE_OFFSET,
                              width = PADDLE_WIDTH, height = PADDLE_HEIGHT,
                              linecolor = colormodel.BLACK,
                              fillcolor = colormodel.BLACK) 
        self._ball = None
                 
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, p_input):
        """This method moves the paddle left and right and makes sure it
        it doesn't go out of the boundaries of the game.
        
        Parameter p_input: the input attribute of breakout
        Precondition: is an instance of GInput
        
        Acknowledgements: Uses code from arrows.py made by author Walker M. White
        """
        if p_input.is_key_down('left') and self._paddle.left >= 0:
            self._paddle.x -= 7
        if p_input.is_key_down('right') and self._paddle.right <= GAME_WIDTH:
            self._paddle.x += 7
            
    def serveBall(self):
        """This method creates an object of class Ball and serves it to
        the player of the game
        """
        self._ball = Ball(x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
                          width = BALL_DIAMETER, height = BALL_DIAMETER,
                          fillcolor = colormodel.BLUE)
        
    def updateBall(self):
        """This method serves and moves the ball.
        Calls on helper method _detectBounce() to detect when the ball bounces
        """
        self._ball.x += self._ball._vx
        self._ball.y += self._ball._vy
        self._detectBounce()
            
        if self._paddle.collidesPaddle(self._ball) and self._ball._vy < 0:
            self._determineDirection()
        
        for i in self._bricks:
            if i.collidesBrick(self._ball):
                random.choice(self.createSound()).play()
                self._bricks.remove(i)
                self._ball._vy = -self._ball._vy
                          
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawBrick(self, view):
        """This method draws the bricks.
        
        Parameter view: used in the original draw method
        Precondition: is an attribute from Breakout
        """
        i = 0
        while i < len(self._bricks):
            self._bricks[i].draw(view)
            i = i + 1
    
    def drawPaddle(self, view):
        """This method draws the paddle.
        
        Parameter view: used in the original draw method
        Precondition: is an attribute from Breakout
        """
        self._paddle.draw(view)
           
    def drawBall(self, view):
        """This method draws the ball.
        
        Parameter view: used in the original draw method
        Precondition: is an attribute from Breakout
        """
        self._ball.draw(view)
            
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def createSound(self):
        """This method creates a list of Sound objects for when the
        ball collides with a brick
        """
        bounceSound = Sound('bounce.wav')
        cupSound = Sound('cup1.wav')
        saucer1Sound = Sound('saucer1.wav')
        saucer2Sound = Sound('saucer2.wav')
        soundList = [bounceSound, cupSound, saucer1Sound, saucer2Sound]
        return soundList
    
    def _determineDirection(self):
        """This method determines which direction the ball moves
        depending on which part of the paddle it hits. If ball is coming
        from the right and it hits the left side of the paddle, it goes back
        in the direction it came from (same concept for left side)
        """
        if (self._ball._vx > 0 and self._ball.x >= self._paddle.left and
            self._ball.x <= self._paddle.left + self._paddle.width/4):
                self._ball._vx = -self._ball._vx
                self._ball._vy = -self._ball._vy
        if (self._ball._vx < 0 and self._ball.x <= self._paddle.right and
            self._ball.x >= self._paddle.right - self._paddle.width/4):
                self._ball._vx = -self._ball._vx
                self._ball._vy = -self._ball._vy
        if (self._ball.x > self._paddle.left + self._paddle.width/4 and
            self._ball.x < self._paddle.right - self._paddle.width/4):
                self._ball._vy = -self._ball._vy
        
    def _detectBounce(self):
        """This method serves as a helper method of updateBall()
        It detects the bounce of the ball.
        """
        if self._ball.top >= GAME_HEIGHT:
            self._ball._vy = -self._ball._vy
            
        if self._ball.right >= GAME_WIDTH:
            self._ball._vx = -self._ball._vx
        
        if self._ball.left <= 0:
            self._ball._vx = -self._ball._vx
    
    def _createBrick(self, bricks):
        """This method serves as a helper method of __init__()
        It creates the bricks for the game.
        
        Parameter bricks: list of bricks
        Precondition: is a list
        """
        #horizontal spacing per block 
        hor_spacing = 0
        #vertical spacing per block
        ver_spacing = 0
        color_index = 0
        for i in range(BRICKS_IN_ROW):
            for j in range(BRICK_ROWS):
                if j%10 == 0 or j %10 == 1:
                    color_index = 0
                elif j%10 == 2 or j %10 == 3:
                    color_index = 1
                elif j%10 == 4 or j %10 == 5:
                    color_index = 2
                elif j%10 == 6 or j %10 == 7:
                    color_index = 3
                elif j%10 == 8 or j %10 == 9:
                    color_index = 4
                brick = Brick(left = BRICK_SEP_H/2 + hor_spacing,
                    bottom = GAME_HEIGHT - BRICK_Y_OFFSET - ver_spacing,
                    width = BRICK_WIDTH, height = BRICK_HEIGHT,
                    linecolor = BRICK_COLORS[color_index],
                    fillcolor = BRICK_COLORS[color_index])
                ver_spacing = ver_spacing + BRICK_HEIGHT + BRICK_SEP_V
                self._bricks.append(brick)
            hor_spacing = hor_spacing + BRICK_WIDTH + BRICK_SEP_H
            #reset ver_spacing for next line. 
            ver_spacing = 0
            
