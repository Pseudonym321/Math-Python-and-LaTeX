
import math
import numpy
import sympy

def invert_point(x, y):
    """
    Purpose:
        Performs inversion on a complex point.
    Parameters:
        x - the real input
        y - the complex input
    Return:
        inv_arg - the argument
        inv_mod - the modulus
    """
    if x == 0 and y == 0:
        return math.inf
    arg, mod = cartesian_to_polar(x, y)
    inv_arg = -arg
    inv_mod = 1/mod
    return inv_arg, inv_mod

def cartesian_to_polar(x, y):
    """
    Purpose:
        Converts cartesian complex points to their polar form in degrees.
    Parameters:
        x - the real input
        y - the complex input
    Return:
        inv_arg - the argument
        inv_mod - the modulus
    """
    arg = math.atan2(y,x)*(180/math.pi)
    mod = math.sqrt(x**2 + y**2)
    return arg, mod

def polar_to_cartesian(arg, mod): # works, input in degrees
    x = mod * math.cos(arg*(math.pi/180))
    y = mod * math.sin(arg*(math.pi/180))
    return x, y

def stereographic_projection(xi, eta, zeta):
    Re = xi/(1-zeta)
    Im = eta/(1-zeta)
    return Re, Im

def inverse_stereographic_projection(Re, Im):
    xi = 2*Re/(1+Re**2+Im**2)
    eta = 2*Im/(1+Re**2+Im**2)
    zeta = (Re**2+Im**2-1)/(1+Re**2+Im**2)
    return xi, eta, zeta
 

class Sphere:
    """
    Spheres are defined by a midpoint (x,y,z), and a radius (r).
    """
    def __init__(self, x:float, y:float, z:float, r:float):
        """
        Purpose:
           Initializes a Sphere object, based on a midpoint and a radius.
        Parameters:
           float - x: the x-component of the sphere's midpoint
           float - y: the y-component of the sphere's midpoint
           float - z: the z-component of the sphere's midpoint
           float - r: the sphere's radius
        Return:
           Void.
        """
        self.c = (x,y,z)
        if not (r > 0):
            assert False, "Negative Radius Inputted."
        self.r = r

    def signed_distance_from_midpoint_to_plane(self,plane) -> float:
        numerator = plane.A*self.c[0]+plane.B*self.c[1]+plane.C*self.c[2]+plane.D # plus or minus plane.D?
        denominator = plane.m
        return numerator/denominator
    
    def intersect_by_plane(self,plane):
        p = self.signed_distance_from_midpoint_to_plane(plane)
        if not (-self.r < p < self.r):
            assert False, "Plane not within vicinity of sphere."
        radius = math.sqrt(self.r**2-p**2)
        center = (self.c[0]+p*plane.unit_normal_vector[0],self.c[1]+p*plane.unit_normal_vector[1],self.c[2]+p*plane.unit_normal_vector[2])
        azimuth = math.atan(center[1]/center[0])
        polar = math.asin((center[2]-1)/math.sqrt(abs(center[0])**2+abs(center[1])**2))
        return radius, center, azimuth, -polar

class Plane:
    """
    Ax+By+Cz=D
    """
    def __init__ (self, A:float, B:float, C:float, D:float):
        """
        Purpose: Ax + By + Cz = D
        Parameters:
        Return:
        """
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.m = math.sqrt(A**2+B**2+C**2)
        self.unit_normal_vector = (A/self.m,B/self.m,C/self.m)


'''
Riemann_sphere = Sphere(0,0,0,1)
plane1 = Plane(-1/1,0,-1,1)
r, c, a, p = Riemann_sphere.intersect_by_plane(plane1)
print(f"Radius:{r}, Center:{c}, Azimuth:{a*180/math.pi}, Polar:{p*180/math.pi}")
'''