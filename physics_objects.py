"""
David Roberts
CS152
November 28
"""

"""
This is a supporting file which provides objects for colission.py
The parent class, ball, block, and other shapes are subclasses. 
"""
import graphicsPlus as gr


class Thing():
    #parent class for objects
    def __init__(self, win, the_type):
        self.type= the_type
        self.mass = 1
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.elasticity = 1
        self.win = win
        self.scale = 10
        self.vis = []
        self.color = [0, 0, 0]
        self.drawn = False
    #setters and getters
    def getPosition(self):
        """returns two element tuple"""
        return tuple(self.position[:])
    
    def setPosition(self, px, py):
        """sets the psition to px and py cordinates. Enables motion by constantly updating position based on frames"""
        point = self.getPosition()
        # assign to x_old the current x position
        x_old = point[0]
        # assign to y_old the current y position
        y_old = point[1]
        # assign to the x coordinate in self.pos the new x coordinate
        # assign to the y coordinate in self.pos the new y coordinate
        self.position = [px, py]
        newpoint = self.getPosition()
        # assign to dx the change in the x position times self.scale
        dx = (newpoint[0] - x_old) * self.scale
        # assign to dy the change in the y position times -self.scale
        dy = (newpoint[1] - y_old) * -1 * self.scale
        # for each item in the vis field of self
        for item in self.vis:
            # call the move method of the item, passing in dx and dy
            item.move(dx, dy)
    
    def getMass(self):
        """returns mass of object as scalar"""
        return float(self.mass)
    def setMass(self, m):
        """sets m as the new mass of the object"""
        self.mass = m
    def getVelocity(self):
        """returns two element tuple for velocity values"""
        return tuple(self.velocity[:])
    def setVelocity(self, vx, vy):
        """makes vx and vy the new x and y velocities of the Ball object."""
        self.velocity = [vx, vy]
    def getAcceleration(self):
        """returns a 2-element tuple with the x and y acceleration values"""
        return tuple(self.acceleration[:])
    def setAcceleration(self, ax, ay):
        """updates ax and ay as the new x and y accelerations of the Ball object."""
        self.acceleration = [ax, ay]
    def getElasticity(self):
        """method that returns the amount of energy retained after a collision"""
        return float(self.elasticity)
    def setElasticity(self, e):
        """sets elasticity to e"""
        self.elasticity = e
    def getScale(self):
        """method to retun the scale factor"""
        return float(self.scale)
    
    def getType(self):
        "method to return the type of the object."
        return str(self.type)
    def getColor(self):
        return tuple(self.color[:])
    def setColor(self, c): 
        self.color = c
        if c != None:
            color_name = gr.color_rgb(c[0], c[1], c[2])
            for x in self.vis:
                x.setFill(color_name)
    def draw(self):
        vis = self.vis
        win = self.win
        for shape in vis:
            shape.draw(win)
        self.drawn = True
    
    def undraw(self):
        vis = self.vis
        for shape in vis:
            shape.undraw()
        self.drawn = False

    def update(self, dt):
        """Method to update the object's position and velocity valus based on forces and accleration. 
        By updating the position motion is visualized"""
        point = self.getPosition()
        vel = self.getVelocity()
        acc = self.getAcceleration()
        # initialize x old to current x position
        x_old = point[0]
        # initialize y old to current y position
        y_old = point[1]
        x_vel = vel[0]
        y_vel = vel[1]
        x_acc = acc[0]
        y_acc = acc[1]
        # update the x position 
        update_x_pos = x_old + x_vel * dt + 0.5 * x_acc * dt * dt
        self.position[0] = update_x_pos
        # update the y position 
        update_y_pos = y_old + y_vel * dt + 0.5 * y_acc * dt * dt
        self.position[1] = update_y_pos
        # find change in x position times the scale factor
        dx = (update_x_pos - x_old) * self.scale
        # find change in y position times the scale factor
        dy = (update_y_pos - y_old) * -1 * self.scale
        for item in self.vis:
        # call the move method of the graphics object with dx and dy as arguments
            item.move(dx, dy)
        # update the x velocity 
        update_x_vel = x_acc * dt + x_vel
        self.velocity[0] = update_x_vel
        # update the y velocity 
        update_y_vel = y_acc * dt + y_vel
        self.velocity[1] = update_y_vel
class Ball(Thing):
    def __init__(self, win, radius = 1, x0 = 0, y0 = 0, color = None):
        Thing.__init__(self,win, 'ball')
        self.radius = radius
        self.position = [x0, y0]
        self.refresh()
        self.setColor(color)

    
    def refresh(self):
        drawn = self.drawn
        if drawn:
            self.undraw()

        win = self.win
        self.vis = [gr.Circle(gr.Point(self.position[0] * self.scale, win.getHeight() - (self.position[1] * self.scale)), self.radius * self.scale)]
        if drawn:
            self.draw()

    def getRadius(self):
        return float(self.radius)
    
    def setRadius(self, r):
        self.radius= r
        self.refresh()
    
class Block(Thing):
    def __init__(self, win, width = 2, height = 1, x0=0, y0=0, color = None):
        Thing.__init__(self, win, "block")
        self.dx = width
        self.dy = height
        self.position = [x0, y0]
        self.reshape()
        self.setColor(color)

    def refresh(self):
        
        drawn = self.drawn
        if drawn == True:
            self.undraw()
        self.vis = [gr.Circle( gr.Point(self.position[0]*self.scale, self.win.getHeight()-self.position[1]*self.scale), self.radius * self.scale ) ]
        if drawn == False:
            self.draw()    
    
    def reshape(self):
        drawn = self.drawn
        if drawn:
            self.undraw()
        win = self.win
        self.vis = [gr.Rectangle(gr.Point((self.position[0] - (self.dx / 2)) * self.scale, win.getHeight() - ((self.position[1] - (self.dy / 2)) * self.scale)), gr.Point((self.position[0] + (self.dx / 2)) * self.scale, win.getHeight() - ((self.position[1] + (self.dy / 2)) * self.scale)))]
        if drawn:
            self.draw()
    
    def getWidth(self):
        return float(self.dx)
    
    def setWidth(self, w):
        self.dx = w
        self.reshape()

    def getHeight(self):
        return float(self.dy)
    
    def setHeight(self, h):
        '''This method makes h the new height of the object.'''
        self.dy = h
        self.reshape()

class Triangle(Ball):
    """This object is a subclass of ball with alternative properties. For example, radius is replaced by height and width"""
    def __init__(self, win, width = 2, height = 2, x0 = 0, y0 = 0, color = None):
        """method to initialize the triangle object based off the ball class"""
        Ball.__init__(self, win)
        self.width = width
        self.height = height
        self.position = [x0, y0]
        self.reshape()
        self.setColor(color)
    
    def reshape(self):
        """mathod to update visualization by undrawing and redrawing the triangle with configurations"""
        drawn = self.drawn
        if drawn:
            self.undraw()
        win = self.win
        self.vis = [gr.Polygon(gr.Point((self.position[0] - (self.width / 2)) * self.scale, win.getHeight() - ((self.position[1] - (self.height / 2)) * self.scale)), gr.Point(self.position[0] * self.scale, win.getHeight() - ((self.position[1] + (self.height / 2)) * self.scale)), gr.Point((self.position[0] + (self.width / 2)) * self.scale, win.getHeight() - ((self.position[1] - (self.height / 2)) * self.scale)))]
        if drawn:
            self.draw()

    #setters and getters
    def getWidth(self):
        return float(self.width)
    
    def setWidth(self, w):
        self.width = w
        self.reshape()
    
    def getHeight(self):
        return float(self.height)

    def setHeight(self, h= 5):
        self.height = h
        self.reshape()

class Tetrahedral_Molecule(Ball):
    """This object is a subclass of ball with some alternative properties"""

    def __init__(self, win, radius = 1.5, x0 = 0, y0 = 0, color = None):
        """method to intitilize features of the Tetrahedral_Molecule based of the Ball class"""
        Ball.__init__(self, win)
        self.radius = radius
        self.position = [x0, y0]
        self.reshape()
        self.setColor(color)

    def reshape(self):
        """This method reshapes or updates the visualization by undrawing and redrawing objects"""
        drawn = self.drawn
        if drawn:
            self.undraw()
        win = self.win
        self.vis = [gr.Circle(gr.Point(self.position[0] * self.scale, win.getHeight() - (self.position[1] * self.scale)), self.radius * 2 / 3 * self.scale), 
        gr.Circle(gr.Point(self.position[0] * self.scale, win.getHeight() - ((self.position[1] + (self.radius * 2 / 3)) * self.scale)), self.radius * 1 / 3 * self.scale), 
        gr.Circle(gr.Point((self.position[0] + (self.radius * 2 / 3)) * self.scale, win.getHeight() - (self.position[1] * self.scale)), self.radius * 1 / 3 * self.scale), 
        gr.Circle(gr.Point(self.position[0] * self.scale, win.getHeight() - ((self.position[1] - (self.radius * 2 / 3)) * self.scale)), self.radius * 1 / 3 * self.scale), 
        gr.Circle(gr.Point((self.position[0] - (self.radius * 2 / 3)) * self.scale, win.getHeight() - (self.position[1] * self.scale)), self.radius * 1 / 3 * self.scale)]
        if drawn:
            self.draw()
        
    def setRadius(self, r):
        """method to determine the new radius"""
        self.radius = r
        self.reshape()