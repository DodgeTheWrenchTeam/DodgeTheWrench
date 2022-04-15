# Test run for algorithm in determination of projectile avoidance
import math
import time


# defining vector object class
class Vector:
    # Initializing vector object based on class call
    def __init__(self, x=0, y=0, z=0):

        self.x = x

        self.y = y

        self.z = z
        # identifying the vector's norm as an attribute
        self.norm = math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # Printing the vector
    def print(self):

        print('[', self.x, self.y, self.z, ']')

    # displaying norm value
    def printNorm(self):

        print(self.norm)

    # normalizing the vector and creating a unit vector from it
    def unit(self):

        a = self.x / self.norm

        b = self.y / self.norm

        c = self.z / self.norm

        return Vector(a, b, c)

    # eliminating vector component depending on which basis plane you want it projected on
    def project(self, direction):

        if direction == 'x':

            d = 0

            e = self.y

            f = self.z

        elif direction == 'y':

            d = self.x

            e = 0

            f = self.z

        elif direction == 'z':

            d = self.x

            e = self.y

            f = 0

        return Vector(d, e, f)


# Subtracting two vectors to determine a current velocity


# def calculateVelocity(p, q):

#     velocity = Vector(q.x - p.x, q.y - p.y, q.z - p.z)

#     return velocity


# #Taking data(position) as a list or array and converting to a vector class object

# def list2Vector(r):

#     position = Vector(r[0], r[1], r[2])

#     return position

# #Test vectors for troubleshooting
# p = [9, 20, 30]
#
# q = [7, 5, 20]
#
# p = list2Vector(p)
#
# q = list2Vector(q)
#
# x_tol = 10

# Main algorithm for object avoidance determination


# Inputs:
# p     position 1, defined as a list
# q     position 2, defined as a list
# x_tol tolerance in mm for collision box
def DodgeWrench(p, q, x_tol, y_tol, FPS, sampleLength):
    # start time of algorithm for determining algorithm run time
    start = time.time()
    # Convert input lists into necessary vectors
    p = Vector(p[0], p[1], p[2])

    q = Vector(q[0], q[1], q[2])

    #Defining time in seconds between two sample locations (based on number of frames between locations and fps of camera)
    sampleRate = sampleLength/FPS

    # finding velocity from two measured points
    v_net = Vector((q.x - p.x)/sampleRate, (q.y - p.y)/sampleRate , (q.z - p.z)/sampleRate)

    if v_net.norm <= 1000 or v_net.z >= 0:
        return "Stay", 0

    # projecting onto planes of interest
    v_zx_naught = v_net.project('y')
    v_zy_naught = v_net.project('x')

    # generating unit vectors of interest
    v_zx_hat = v_zx_naught.unit()
    v_zy_hat = v_zy_naught.unit()

    # using dot product to find relative angles
    theta = math.acos((-v_zx_hat.z*p.z)/p.z)
    alpha = math.acos(-v_zy_hat.z)

    # solving for distance from expected point of x-y plane intersection
    r_contact_zx = p.z/math.cos(theta)
    r_contact_zy = p.z/math.cos(alpha)

    # quantity used to determine intersection point relative to the oak-D
    x_T = math.sqrt((r_contact_zx**2) - (p.z**2))
    y_T = math.sqrt((r_contact_zy**2) - (p.z**2))

    # defining initial x direction with considerations made for niche cases
    if p.x != 0:
        x_hat = p.x/abs(p.x)
    elif v_zx_naught.x < 0:
        x_hat = -1
    elif v_zx_naught.x > 0:
        x_hat = 1
    else:
        x_hat = 0

    # defining initial y direction with considerations made for niche cases
    if p.y != 0:
        y_hat = p.y/abs(p.y)
    elif v_zy_naught.y < 0:
        y_hat = -1
    elif v_zy_naught.y > 0:
        y_hat = 1
    else:
        y_hat = 0

    # some tolerance so that the program doesnt break
    epsilon = 0.001

    # initializing x* and y* so that program is happy
    x_star = 0
    y_star = 0

    # checking possible cases to determine proper way to calculate x*
    if abs(v_zx_naught.x) < epsilon:
        x_star = p.x

    elif v_zx_hat.x * x_hat > 0:
        x_star = (abs(p.x) + x_T)*x_hat

    elif x_T > abs(p.x):
        x_star = -(x_T - abs(p.x))*x_hat

    elif x_T < abs(p.x):
        x_star = (abs(p.x) - x_T)*x_hat
    
     # checking possible cases to determine proper way to calculate y*
    if abs(v_zy_naught.y) < epsilon:
        y_star = p.y

    elif v_zy_hat.y * y_hat > 0:
        y_star = (abs(p.y) + y_T)*y_hat

    elif y_T > abs(p.y):
        y_star = -(y_T - abs(p.y))*y_hat

    elif y_T < abs(p.y):
        y_star = (abs(p.y) - y_T)*x_hat

    # determining choice based on value of x*, y*, and desired collision window
    if abs(y_star) <= y_tol:
        if abs(x_star) > x_tol:
            Choice = 'Stay'
        elif abs(x_star) <= epsilon:
            Choice = 'Move Either Way'
        elif abs(x_star) <= x_tol and x_star < 0:
            Choice = 'right'
        elif abs(x_star) <= x_tol and x_star > 0:
            Choice = 'left'
        else:
            Choice = 'Error'
    else:
        Choice = 'Stay'

    # How far does the cart need to move to avoid the projectile?
    if Choice != 'Stay':
        moveDistance = x_tol - abs(x_star)
    else:
        moveDistance = 0
    runTime = time.time() - start
    #print('Run Time =', "%.10f" % runTime)
    return Choice, moveDistance


if __name__ == "__main__":
    p = [0,0,1000]
    q = [-10,-40,900]
    x_tol = 1000
    y_tol = 500
    output = DodgeWrench(p, q, x_tol, y_tol, 30, 2)
    print('Result =', output)





