from __future__ import annotations
from typing import Optional
from os import PathLike
from math import *
import pygame

class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = 1

    def __add__(a, b):
        if type(b) == Vector3:
            return Vector3(a.x + b.x, a.y + b.y, a.z + b.z)
        return Vector3(a.x + b, a.y + b, a.z + b)

    def __sub__(a, b):
        if type(b) == Vector3:
            return Vector3(a.x - b.x, a.y - b.y, a.z - b.z)
        return Vector3(a.x - b, a.y - b, a.z - b)

    def __mul__(a, b):
        if type(b) == Vector3:
            return Vector3(a.x * b.x, a.y * b.y, a.z * b.z)
        return Vector3(a.x * b, a.y * b, a.z * b)

    def __truediv__(a, b):
        if type(b) == Vector3:
            return Vector3(a.x / b.x, a.y / b.y, a.z / b.z)
        return Vector3(a.x / b, a.y / b, a.z / b)

    def norm(self):
        mg = sqrt( pow(self.x,2) + pow(self.y,2) + pow(self.z,2) )
        if mg == 0:
            self.x, self.y, self.z = 0, 0, 0
        else:
            self.x, self.y, self.z =  self.x/mg, self.y/mg, self.z/mg
    
    def dot(self, b):
        return self.x * b.x + self.y * b.y + self.z * b.z
    

    def toMatrix(self):
        return [[self.x, self.y, self.z, self.w]]


    def GetTuple(self):
        return (int(self.x), int(self.y))

    def __repr__(self):
        #debug
        return f" vec3-> ({self.x}, {self.y}, {self.z})"

class Camera:
    def __init__(self, position, near, far, fov):
        self.position = position
        self.near = near
        self.far = far
        self.fov = fov
        self.yaw = 0
        self.phi = 0
        self.tangent = 1.0 / tan(self.fov * 0.5 / 180 * pi)
        self.direction = Vector3()
        self.up = Vector3()
        self.transform = Matrix.identity()
        self.target = position
        self.speed = 0.1
        self.rotationSpeed = 1.5
        self.temp = Vector3()

    def HandleInput(self, dt):
        keys = pygame.key.get_pressed()
        delta = self.speed * dt

        if keys[pygame.K_UP]:
            self.position.y += delta
        if keys[pygame.K_DOWN]:
            self.position.y -= delta
        if keys[pygame.K_RIGHT]:
            self.position.x -= delta
        if keys[pygame.K_LEFT]:
            self.position.x += delta

        self.temp = self.target * delta

        if keys[pygame.K_w]: #zoom in
            self.position += self.temp
        if keys[pygame.K_s]: #zoom out
            self.position -= self.temp
        if keys[pygame.K_a]:
            self.yaw -= 0.04
        if keys[pygame.K_d]:
            self.yaw += 0.04

    def HandleMouseEvent(self, x, y, deltaTime):
        # not finished
        self.yaw += x

    def projection(self) -> Matrix:
        """Compute the projection Matrix corresponding to the current camera position
        and orientation.
        Returns:
            Matrix - the projection matrix
        """
        matrix = Matrix()
        matrix.val = [
            [aspect * self.tangent, 0.0, 0.0, 0.0],
            [0.0, self.tangent, 0.0, 0.0],
            [0.0, 0.0, self.far / (self.far - self.near), 1],
            [0.0, 0.0, (-self.far * self.near) / (self.far - self.near), 0.0],
        ]
        return matrix

Size = 1000, 1000
Width, Height = Size
BackgroundColor = (0 , 0, 0)
aspect = Height/Width #aspect ratio

clipping = 1.5
mouse_sensitivity = 200
Zoffset = 7

dim = 0.01 #the darkest spot on the screen

#colors
blue = (0, 0, 255)
orange = (255, 160, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (0, 255, 255)

def HandleEvent(camera, deltaTime):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                x, y = event.rel
                x /= mouse_sensitivity
                y /= mouse_sensitivity
                camera.HandleMouseEvent(x, y, deltaTime)

    return running

class Light: # simple directional light
    def __init__(self, position):
        self.position = position
        self.direction = Normalize(self.position)

from copy import deepcopy

class Matrix:
    """Represents a matrix with standard operation support."""

    def __init__(self, r: int = 4, c: int = 4):
        """Initialize new Matrix with r rows and c cols. Sets all values to 0.0."""
        self.val = [[0.0 for _ in range(c)] for _ in range(r)]

    def __repr__(self) -> str:
        """repr(self)"""
        return f"matrix->{self.val}"

    @property
    def row(self) -> int:
        """The number of rows in self."""
        return len(self.val)

    @property
    def col(self) -> int:
        """The number of cols in self."""
        return len(self.val[0])

    @classmethod
    def from_vector(cls, vec: Vector3) -> Matrix:
        """Construct a new Matrix formed by a Vector3.
        Returns:
            Matrix - matrix with size 1, 4 populated by vec's x, y, z, w.
        """
        rv = cls(1, 4)
        rv.val = [[vec.x, vec.y, vec.z, vec.w]]
        return rv

    @classmethod
    def rotation_x(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the x-axis by angle radians
        Arguments:
            angle - angle in radians to for xrotmat to represent.
        Returns:
            Matrix - angle rotation around x-axis Matrix
        """
        matrix = cls()
        matrix.val = [
            [1, 0.0, 0.0, 0.0],
            [0.0, cos(angle), sin(angle), 0.0],
            [0.0, -sin(angle), cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def rotation_y(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the y-axis by angle radians
        Arguments:
            angle - angle in radians to for yrotmat to represent.
        Returns:
            Matrix - angle rotation around y-axis Matrix
        """
        matrix = cls()
        matrix.val = [
            [cos(angle), 0.0, -sin(angle), 0.0],
            [0.0, 1, 0.0, 0.0],
            [sin(angle), 0.0, cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def rotation_z(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the z-axis by angle radians
        Arguments:
            angle - angle in radians to for zrotmat to represent.
        Returns:
            Matrix - angle rotation around z-axis Matrix
        """
        matrix = cls()
        matrix.val = [
            [cos(angle), sin(angle), 0.0, 0.0],
            [-sin(angle), cos(angle), 0.0, 0.0],
            [0.0, 0.0, 1, 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def scaling(cls, scale: float) -> Matrix:
        """Construct a scaling matrix for the given scale factor.
        Arguments:
            scale - float, the scale value for Matrix to be constructed for
        Returns:
            Matrix - the scaling Matrix
        """
        matrix = cls()
        matrix.val = [
            [scale, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, scale, 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    @classmethod
    def identity(cls, size: int = 4) -> Matrix:
        """Construct an identity matrix of the given size. Defined as a square matrix
        with 1s on the main diagonal, and 0s elsewhere.
        Arguments:
            size - int, the size of the identity matrix.
        Returns:
            Matrix - the specified identity matrix.
        """
        matrix = cls()
        matrix.val = [
            [1.0 if i == j else 0.0 for j in range(size)] for i in range(size)
        ]
        return matrix

    @classmethod
    def translate(cls, position: Vector3) -> Matrix:
        """Construct a Matrix that performs a translation specified by the give
        position.
        Arguments:
            position - the Vector3 to construct translation matrix by.
        Returns:
            Matrix - the constructed translation Matrix.
        """
        matrix = cls()
        matrix.val = [
            [1, 0.0, 0.0, position.x],
            [0.0, 1, 0.0, position.y],
            [0.0, 0.0, 1, position.z],
            [0.0, 0.0, 0.0, 1],
        ]
        return matrix

    def __matmul__(self, other: Matrix) -> Matrix:
        """Support for self @ other, defined as matrix multiplication.
        Raises:
            ValueError - if self and other have incompatible dimensions.
        Returns:
            Matrix - product of self and other, size is self.row x other.col.
        """
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.col != other.row:
            raise ValueError(
                "Matrices incompatible for multiplication, got: "
                f"{(self.row, self.col)}, {(other.row, other.col)}"
            )

        rv = Matrix(self.row, other.col)
        for x in range(self.row):
            for y in range(other.col):
                val = sum(self.val[x][z] * other.val[z][y] for z in range(self.col))
                rv.val[x][y] = round(val, 5)

        return rv

    def transpose(self) -> Matrix:
        """Compute the transpose of self. Defined as the matrix formed by swapping the
        rows and cols of self.
        Returns:
            Matrix - transpose of self.
        """
        rv = Matrix(self.row, self.col)
        for x in range(self.row):
            for y in range(self.col):
                rv.val[x][y] = self.val[y][x]
        return rv

    def submatrix(self, row: int, col: int) -> Matrix:
        """Form the matrix resulting from removing the specified row and col
        from self.
        Returns:
            Matrix - self without row or col.
        """
        temp = deepcopy(self)
        del temp.val[row]
        for i in range(self.row):
            del temp.val[i][col]

        return temp

    def det(self) -> float:
        """Calculate the determinant of self.
        Raises:
            ValueError - If self is not square.
        Returns:
            float - self's determinant.
        """
        if self.row != self.col:
            raise ValueError("Matrix determinant only defined for square matrices.")

        if self.row == 2:
            return self.val[0][0] * self.val[1][1] - self.val[0][1] * self.val[1][0]

        d = 0.0
        for j in range(self.col):
            c = self.cofactor(0, j)
            d += c * self.val[0][j]
        return d

    def updateInfo(self):
        self.row = len(self.val)
        self.col = len(self.val[0])

    def transpose(self):
        temp = [[0 for i in range(self.col)] for j in range(self.row)]
        for x in range(self.row):
            for y in range(self.col):
                temp[x][y] = self.val[y][x]
        self.val = temp

    def __repr__(self):
        ## DEBUG
        return f'matrix->{self.val}'


def multiplyMatrix(m1, m2):
    m = Matrix(m1.row, m2.col)

    if m1.col != m2.row:
        print("we can't this two matricies")
        return None

    for x in range(m1.row):
        for y in range(m2.col):
            sum = 0
            for z in range(m1.col):
                sum += m1.val[x][z] * m2.val[z][y]
            m.val[x][y] = round(sum, 5)

    return m

def multiplyMatrixVector(vec, mat):
    temp = Matrix(1, 4)
    temp.val = vec.toMatrix()
    m = multiplyMatrix(temp, mat)
    v = toVector3(m)
    if m.val[0][3] != 0:
        v = v / m.val[0][3]
    return v

def TransposeMatrix(m):
    m1 = Matrix(m.row, m.col)
    for x in range(m.row):
        for y in range(m.col):
            m1.val[x][y] = m.val[y][x]

    return m1

def Determinant2x2(matrix):
    # print(matrix.val)
    return matrix.val[0][0] * matrix.val[1][1] - matrix.val[0][1] * matrix.val[1][0]

def submatrix(matrix, row, column):
    temp = deepcopy(matrix)
    del temp.val[row]
    for i in range(len(temp.val)):
        del temp.val[i][column]

    temp.updateInfo()
    # print(temp.val)
    return temp

def Minor3x3(matrix, row, column):
    s = submatrix(matrix, row, column)

    if len(s.val) > 2:
        return Determinant(s)
    else:
        return Determinant2x2(s)

def Cofactor3x3(matrix, row, column):
    minor = Minor3x3(matrix, row, column)
    if (row + column) % 2 == 0:
        return minor
    else:
        return -minor

def Determinant(matrix):
    if matrix.row == 2:
        return Determinant2x2(matrix.val)
    else:
        d = 0
        for j in range(len(matrix.val[0])):
            c = Cofactor3x3(matrix, 0, j)

            d += c * matrix.val[0][j]
        return d

def MatrixInversion(matrix):
    d = Determinant(matrix)
    if d == 0:
        print("this matrix is not invertible")
        return None

    new = Matrix(matrix.row, matrix.col)
    for x in range(matrix.row):
        for y in range(matrix.col):
            new.val[x][y] = round(Cofactor3x3(matrix, x, y) / d, 6)
    new.transpose()
    # print(new.val)
    return new

def QuickInverse(m):
    matrix = Matrix()
    matrix.val[0][0], matrix.val[0][1], matrix.val[0][2], matrix.val[0][3] = m.val[0][0], m.val[1][0], m.val[2][0], 0.0
    matrix.val[1][0], matrix.val[1][1], matrix.val[1][2], matrix.val[1][3] = m.val[0][1], m.val[1][1], m.val[2][1], 0.0
    matrix.val[2][0], matrix.val[2][1], matrix.val[2][2], matrix.val[2][3] = m.val[0][2], m.val[1][2], m.val[2][2], 0.0
    matrix.val[3][0] = -(m.val[3][0] * matrix.val[0][0] + m.val[3][1] * matrix.val[1][0] + m.val[3][2] * matrix.val[2][0])
    matrix.val[3][1] = -(m.val[3][0] * matrix.val[0][1] + m.val[3][1] * matrix.val[1][1] + m.val[3][2] * matrix.val[2][1])
    matrix.val[3][2] = -(m.val[3][0] * matrix.val[0][2] + m.val[3][1] * matrix.val[1][2] + m.val[3][2] * matrix.val[2][2])
    matrix.val[3][3] = 1.0
    return matrix

def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2) * ((value-min1)/(max1-min1))

def CubeTriangles(color, position=Vector3(), scale=1):
    return [
    Triangle( Vector3(-1.0, -1.0, -1.0) * scale + position, Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position, color),
    Triangle( Vector3(-1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position, Vector3(1.0, -1.0, -1.0) * scale + position, color),

    Triangle( Vector3(1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position, color),
    Triangle( Vector3(1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position, Vector3(1.0, -1.0, 1.0) * scale + position, color),

    Triangle( Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position, color),
    Triangle( Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, 1.0) * scale + position, color),

    Triangle( Vector3(-1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, -1.0) * scale + position, color),
    Triangle( Vector3(-1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(-1.0, -1.0, -1.0) * scale + position, color),

    Triangle( Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position, color),
    Triangle( Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position, color),

    Triangle( Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, -1.0) * scale + position, color),
    Triangle( Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, -1.0) * scale + position, Vector3(1.0, -1.0, -1.0) * scale + position, color),
]

def QuadTriangles(color=(255, 255, 255), size=5):
    vertices = [
        Vector3(-size, -size, -size),
        Vector3(-size, size, -size),
        Vector3(size, size, -size),
        Vector3(size, -size, -size)
    ]

    return [
        Triangle(vertices[0], vertices[1], vertices[2], color),
        Triangle(vertices[0], vertices[2], vertices[3], color)
    ]

def PlaneTriangles(color=(255, 255, 255), resolution=10, size=2):
    meshData = []
    vertices = [[None for i in range(resolution)] for j in range(resolution)]

    for i in range(resolution):
        for j in range(resolution):
            x = translate(i, 0, resolution, -size, size)
            y = translate(j, 0, resolution, -size, size)
            vertices[i][j] = Vector3(x, 0, y)

    for i in range(resolution):
        for j in range(resolution):
            if i + 1 < resolution and j + 1 < resolution:
                v1 = vertices[i][j]
                v2 = vertices[i+1][j]
                v3 = vertices[i][j+1]
                v4 = vertices [i+1][j+1]
                meshData.append(Triangle(v1, v2, v3, color))
                meshData.append(Triangle(v4, v3, v2, color))


    return meshData

class Point:
    def __init__(self, position, color=(255, 255, 255), radius=10):
        self.position = position
        self.color = color
        self.radius = radius
        self.transform = Matrix.identity()

    def update(self,screen, camera,showPoint=False):

        projected = None
        transformed = None
        transformed = multiplyMatrixVector(self.position, self.transform)
        transformed += Vector3(0, 0, Zoffset)
        transformed = multiplyMatrixVector(transformed, camera.viewMatrix)
        projected = multiplyMatrixVector(transformed, camera.projection())
        projected *= Vector3(-1, -1, 1)

        offsetView = Vector3(1, 1, 0)
        projected = projected + offsetView
        projected *= Vector3(Width, Height, 1) * 0.5
        if showPoint:
            pygame.draw.circle(screen,self.color, projected.GetTuple(), self.radius)
        return projected

def SphereTriangles(color,n_subdivision=10, radius=1):
    #simple UV SPHERE
    meshData = []
    vertices  = []

    #adding top vertex
    vertices.append(Vector3(0, radius, 0))
    #generate vertices of the sphere
    for i in range(n_subdivision):
        phi = pi * (i+1) / n_subdivision
        for j in range(n_subdivision):
            theta = 2 * pi * j / n_subdivision
            x = radius * sin(phi) * cos(theta)
            y = radius * cos(phi)
            z = radius * sin(phi) * sin(theta)
            vertices.append(Vector3(x, y, z))
    #add bottom vertex
    vertices.append(Vector3(0, -radius, 0))

    #add top and bottom triangles
    for i in range(n_subdivision):
        i0 = i + 1
        i1 = (i+1) % n_subdivision + 1
        meshData.append(Triangle(vertices[0], vertices[i1], vertices[i0], color) )
        i0 = i + n_subdivision * (n_subdivision - 2) + 1
        i1 = (i+1) % n_subdivision + n_subdivision * (n_subdivision - 2) + 1
        meshData.append( Triangle(vertices[-1], vertices[i1], vertices[i0], color) )

    for j in range(n_subdivision-2):
        j0 = j * n_subdivision + 1
        j1 = (j+1) * n_subdivision + 1
        for i in range(n_subdivision):
            i0 = j0 + i
            i1 = j0 + (i + 1) % n_subdivision
            i2 = j1 + (i + 1) % n_subdivision
            i3 = j1 + i
            meshData.append( Triangle(vertices[i0], vertices[i1], vertices[i2], color))
            meshData.append( Triangle(vertices[i0], vertices[i2], vertices[i3], color))

    return meshData

def GetMiddlePoint(vec1, vec2, vertices, middlePointCache):
    a = vertices.index(vec1)
    b = vertices.index(vec2)

    # check if the edge is already divided to avoid duplicated vertices
    smallerIndex, greaterIndex = b, a
    if a < b:
        smallerIndex = a
        greaterIndex = b
    key = f"{smallerIndex}, {greaterIndex}"

    if key in middlePointCache:
        return middlePointCache[key]

    vertex1 = vertices[a]
    vertex2 = vertices[b]

    middle = Normalize( (vertex1+vertex2)/2 )
    vertices.append(middle)

    _index = vertices.index(middle)
    middlePointCache.update({key: _index})

    return _index

def IcosphereTriangles(color=(255, 255, 255), subdivision=0, radius=1):
    middlePointCache = {}
    g = (1 + sqrt(5))/2 #golden ratio

    vertices = [
        Normalize(Vector3(-1,  g, 0)),
        Normalize(Vector3( 1,  g, 0)),
        Normalize(Vector3(-1, -g, 0)),
        Normalize(Vector3( 1, -g, 0)),

        Normalize(Vector3( 0, -1,  g)),
        Normalize(Vector3( 0,  1,  g)),
        Normalize(Vector3( 0, -1, -g)),
        Normalize(Vector3( 0,  1, -g)),

        Normalize(Vector3( g,  0,  -1)),
        Normalize(Vector3( g,  0,  1)),
        Normalize(Vector3( -g,  0,  -1)),
        Normalize(Vector3( -g,  0,  1))
    ]
    triangles = [
         # 5 faces around point 0
         Triangle(vertices[0], vertices[11], vertices[5], color),
         Triangle(vertices[0], vertices[5], vertices[1], color),
         Triangle(vertices[0], vertices[1], vertices[7], color),
         Triangle(vertices[0], vertices[7], vertices[10], color),
         Triangle(vertices[0], vertices[10], vertices[11], color),
         # Adjacent faces
         Triangle(vertices[1], vertices[5], vertices[9], color),
         Triangle(vertices[5], vertices[11], vertices[4], color),
         Triangle(vertices[11], vertices[10], vertices[2], color),
         Triangle(vertices[10], vertices[7], vertices[6], color),
         Triangle(vertices[7], vertices[1], vertices[8], color),
         # 5 faces around 3
         Triangle(vertices[3], vertices[9], vertices[4], color),
         Triangle(vertices[3], vertices[4], vertices[2], color),
         Triangle(vertices[3], vertices[2], vertices[6], color),
         Triangle(vertices[3], vertices[6], vertices[8], color),
         Triangle(vertices[3], vertices[8], vertices[9], color),
         # Adjacent faces
         Triangle(vertices[4], vertices[9], vertices[5], color),
         Triangle(vertices[2], vertices[4], vertices[11], color),
         Triangle(vertices[6], vertices[2], vertices[10], color),
         Triangle(vertices[8], vertices[6], vertices[7], color),
         Triangle(vertices[9], vertices[8], vertices[1], color)
    ]

    # subdivision
    for i in range(subdivision):
        subdivisions = []
        for triangle in triangles:
            _i0 = GetMiddlePoint(triangle.vertex1, triangle.vertex2, vertices, middlePointCache)
            _i1 = GetMiddlePoint(triangle.vertex2, triangle.vertex3, vertices, middlePointCache)
            _i2 = GetMiddlePoint(triangle.vertex3, triangle.vertex1, vertices, middlePointCache)

            vertex1 = vertices[_i0]
            vertex2 = vertices[_i1]
            vertex3 = vertices[_i2]

            subdivisions.append(Triangle(triangle.vertex1, vertex1, vertex3, color))
            subdivisions.append(Triangle(triangle.vertex2, vertex2, vertex1, color))
            subdivisions.append(Triangle(triangle.vertex3, vertex3, vertex2, color))
            subdivisions.append(Triangle(vertex1, vertex2, vertex3, color))

        triangles = subdivisions
    #print(triangles)
    return triangles

def FibonnaciSphereTriangles(color=(255, 255, 255), n=50):
    #not finished
    triangles = []
    vertices = []
    # golden ratio in radians
    g = pi * (3 - sqrt(5))/2

    for i in range(n):
        y = 1 - (i / float(n - 1)) * 2  # y goes from 1 to -1
        radius = sqrt(1 - y * y)  # radius at y
        theta = g * i  # golden angle increment
        x = cos(theta) * radius
        z = sin(theta) * radius
        vertices.append(Vector3(x, y, z))

    for i in range(len(vertices)-3):
        vertex1 = vertices[i]
        vertex2 = vertices[i+1]
        vertex3 = vertices[i+2]
        triangles.append(Triangle(vertex1, vertex2, vertex3, color))

    print("work in progress")
    return triangles

import colorsys

def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

def DrawTriangle(screen, triangle, fill, wireframe, vertices, radius, verticeColor, wireframeColor, lineWidth):

    if fill == True:
        #print(triangle.color)
        pygame.draw.polygon(screen, triangle.color, triangle.GetPolygons())

    if wireframe == True:
        pygame.draw.line(screen, wireframeColor, triangle.vertex1.GetTuple(), triangle.vertex2.GetTuple(), lineWidth)
        pygame.draw.line(screen, wireframeColor, triangle.vertex2.GetTuple(), triangle.vertex3.GetTuple(), lineWidth)
        pygame.draw.line(screen, wireframeColor, triangle.vertex3.GetTuple(), triangle.vertex1.GetTuple(), lineWidth)

    if vertices == True:
        color = (255, 255 ,255) if verticeColor==False else triangle.verticeColor

        pygame.draw.circle(screen, color, triangle.vertex1.GetTuple(), radius)
        pygame.draw.circle(screen, color, triangle.vertex2.GetTuple(), radius)
        pygame.draw.circle(screen, color, triangle.vertex3.GetTuple(), radius)

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def LoadMesh(objectPath, color=(255, 255, 255)):
    vert_data = []
    triangle_indices = []
    data = None
    meshData = []

    #read and close file
    with open(objectPath, 'r') as objectFile:
        data = objectFile.readlines()

    # get data
    for _line in data:
        _line = _line.split(" ")
        if _line[0] == 'v':
            vert_data.append(Vector3(float(_line[1]), float(_line[2]), float(_line[3])))
        elif _line[0] == 'f':
            temp = _line[1:]
            line_indices = []
            for el in temp:
                indexList = el.split('/')
                line_indices.append(int(indexList[0]) )

            triangle_indices.append(line_indices)

    for t in triangle_indices:
        triangle = Triangle( vert_data[t[0]-1], vert_data[t[1]-1],vert_data[t[2]-1], color)
        meshData.append(triangle)
    return meshData

def translateValue(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

def SignedDist(pos, normal, p):
    n = Normalize(pos)
    return (normal.x * pos.x + normal.y * pos.y + normal.z * pos.z - dotProduct(normal, p))

def TriangleClipped(pos, normal, triangle, outTriangle, clippingDebug=False):
    #normal = Normalize(normal)

    insidePoints, insideCount = [None for _ in range(3)], 0
    outsidePoints, outsideCount = [None for _ in range(3)], 0

    d0 = SignedDist(triangle.vertex1, normal, pos)
    d1 = SignedDist(triangle.vertex2, normal, pos)
    d2 = SignedDist(triangle.vertex3, normal, pos)

    if d0 >= 0:
        insidePoints[insideCount] = triangle.vertex1
        insideCount += 1
    else:
        outsidePoints[outsideCount] = triangle.vertex1
        outsideCount += 1

    if d1 >= 0:
        insidePoints[insideCount] = triangle.vertex2
        insideCount += 1
    else:
        outsidePoints[outsideCount] = triangle.vertex2
        outsideCount += 1

    if d2 >= 0:
        insidePoints[insideCount] = triangle.vertex3
        insideCount += 1
    else:
        outsidePoints[outsideCount] = triangle.vertex3
        outsideCount += 1

    if insideCount == 0:
        return 0
    if insideCount == 3:
        outTriangle[0] = triangle

        return 1

    if insideCount == 1 and outsideCount == 2:
        # outTriangle[0].color = (0, 255,24)
        outTriangle[0].color = triangle.color if clippingDebug==False else red

        outTriangle[0].vertex1 = insidePoints[0]
        outTriangle[0].vertex2 = PlaneLineIntersection(pos, normal, insidePoints[0], outsidePoints[0])
        outTriangle[0].vertex3 = PlaneLineIntersection(pos, normal, insidePoints[0], outsidePoints[1])
        return 1

    if insideCount == 2 and outsideCount == 1:

        # outTriangle[0].color = (55, 60, 255)
        # outTriangle[1].color = (255,51, 12)
        outTriangle[0].color = triangle.color if clippingDebug==False else blue
        outTriangle[1].color = triangle.color if clippingDebug==False else green
        outTriangle[0].vertex1 = insidePoints[1]
        outTriangle[0].vertex2 = insidePoints[0]
        outTriangle[0].vertex3 = PlaneLineIntersection(pos, normal, insidePoints[0], outsidePoints[0])

        outTriangle[1].vertex1 = insidePoints[1]
        outTriangle[1].vertex2 = outTriangle[0].vertex3
        outTriangle[1].vertex3 = PlaneLineIntersection(pos, normal, insidePoints[1], outsidePoints[0])

        return 2

def DrawAxis(screen, camera, scale=3,center=None, Xaxis=True, Yaxis=True, Zaxis=True, stroke=5):
    if center == None:
        center = Point(Vector3(0, 0, 0))

    X = Point(Vector3(scale, 0, 0), (255, 0, 0))
    Y = Point(Vector3(0, scale, 0), (0, 255, 0))
    Z = Point(Vector3(0, 0, scale), (0, 0, 255))
    origin = center.update(screen, camera)

    if Xaxis:
        x_axis = X.update(screen, camera, True)
        pygame.draw.line(screen, X.color, origin.GetTuple(),x_axis.GetTuple(), stroke)
    if Zaxis:
        z_axis = Z.update(screen, camera, True)
        pygame.draw.line(screen, Z.color, origin.GetTuple(), z_axis.GetTuple(), stroke)
    if Yaxis:
        y_axis = Y.update(screen, camera, True)
        pygame.draw.line(screen, Y.color, origin.GetTuple(), y_axis.GetTuple(), stroke)

def PointAt(current, next, up) -> Matrix:
    #f = (next - current).norm()
    #u = (up - f * up.dot(f)).norm()
    #r = u.cross(f)  # right vector
    f = Normalize(next - current) # forward vector
    u = (up - f * dotProduct(up, f)) # up vector
    r = crossProduct(u, f) # right vector

    m = Matrix()
    m.val = [
        [r.x, r.y, r.z, 0.0],
        [u.x, u.y, u.z, 0.0],
        [f.x, f.y, f.z, 0.0],
        [current.x, current.y, current.z, 1.0],
    ]
    return m


# TODO: perhaps this function should take in a Matrix as arg
# TODO: should move into matrix.Matrix class?
def Shearing(
    xy: float, xz: float, yx: float, yz: float, zx: float, zy: float
) -> Matrix:
    m = Matrix()
    m.val = [
        [1, xy, xz, 0.0],
        [yx, 1, yz, 0.0],
        [zx, zy, 1, 0.0],
        [0.0, 0.0, 0.0, 1],
    ]
    return m

class Triangle:
    def __init__(self, v1=None, v2=None, v3=None, color=(255, 255, 255)):
        self.vertex1 = v1
        self.vertex2 = v2
        self.vertex3 = v3
        self.color = color
        self.verticeColor = color

    def Shade(self, val):
        r, g, b = 0, 0, 0
        if self.color[0] * val > 255:
            r = 255
        elif self.color[0] * val < 0:
            r = 0
        else:
            r = int(self.color[0] * val)

        if self.color[1] * val > 255:
            g = 255
        elif self.color[1] * val < 0:
            g = 0
        else:
            g = int(self.color[1] * val)

        if self.color[2] * val > 255:
            b = 255
        elif self.color[2] * val < 0:
            b = 0
        else:
            b = int(self.color[2] * val)

        return (r, g, b)

    def GetPolygons(self):
        return [(int(self.vertex1.x), int(self.vertex1.y)),
                (int(self.vertex2.x), int(self.vertex2.y)),
                (int(self.vertex3.x), int(self.vertex3.y))]

    def __repr__(self):
        #debug
        return f"triangle-> {(self.vertex1), (self.vertex2), (self.vertex3), {self.color}}"

import colorsys

class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __add__(a, b):
        if type(b) == Vector2:
            return Vector2(a.x + b.x, a.y + b.y)
        return Vector2(a.x + b, a.y + b)

    def __sub__(a, b):
        if type(b) == Vector2:
            return Vector2(a.x - b.x, a.y - b.y)
        return Vector2(a.x - b, a.y - b)

    def __mul__(a, b):
        if type(b) == Vector2:
            return Vector2(a.x * b.x, a.y * b.y)
        return Vector2(a.x * b, a.y * b)

    def __truediv__(a, b):
        if type(b) == Vector2:
            return Vector2(a.x / b.x, a.y / b.y)
        return Vector2(a.x / b, a.y / b)

    def __repr__(self):
        return f"vec2-> ({self.x}, {self.y})"

def toVector3(matrix):
    return Vector3(matrix.val[0][0], matrix.val[0][1], matrix.val[0][2])

def crossProduct(a, b):
    x = a.y * b.z - a.z * b.y
    y = a.z * b.x - a.x * b.z
    z = a.x * b.y - a.y * b.x
    return Vector3(x, y, z)

def dotProduct(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def GetMagnitude(a):
    if type(a) == Vector3:
        return sqrt( pow(a.x,2) + pow(a.y,2) + pow(a.z,2) )
    else:
        return sqrt(pow(a.x,2) + pow(a.y,2))

def Normalize(a):
    mg = GetMagnitude(a)
    if mg == 0:
        return Vector3()
    return Vector3(a.x/mg, a.y/mg, a.z/mg)

def PlaneLineIntersection(pos, normal, lineStart, lineEnd):
    normal = Normalize(normal)
    p = - dotProduct(normal, pos)
    ad  = dotProduct(lineStart, normal)
    bd = dotProduct(lineEnd, normal)
    t = (-p -ad) / (bd - ad)
    lineStartEnd = lineEnd - lineStart
    lineTointersect = lineStartEnd * t
    return (lineStart + lineTointersect)

class Scene:
    def __init__(self, world=[]):
        self.world = world

    def update(self, dt, camera, light, screen, showAxis=False,
               fill=True, wireframe=False, vertices=False, depth=True,
               clippingDebug=False, showNormals=False,
               radius=8, verticeColor=False,
               wireframeColor=(255, 255, 255),ChangingColor=0, lineWidth=1):
        camera.HandleInput(dt)

        camera.direction = Vector3(0, 0, 1)
        camera.up = Vector3(0, 1, 0)
        camera.target = Vector3(0, 0, 1)
        camera.rotation = Matrix.rotation_y(camera.yaw)
        camera.direction = multiplyMatrixVector(camera.target, camera.rotation)
        camera.target = camera.position + camera.direction
        lookAtMatrix = PointAt(camera.position, camera.target, camera.up)
        camera.viewMatrix = QuickInverse(lookAtMatrix)
        camera.target= Vector3(0, 0, 1)

        triangles = []
        origins = []
        for ob in self.world:
            triangles += ob.update(screen,fill, wireframe, dt, camera, light, depth, clippingDebug, ChangingColor)

        # sort the triangles list based on the average of their
        # z coordinate -> painters algorithm
        def Zsort(val):
            return (val.vertex1.z + val.vertex2.z + val.vertex3.z) / 3.0

        triangles.sort(key=Zsort)

        normals_length = 250
        normals = []

        for projected in reversed(triangles):
            origin = (projected.vertex1+projected.vertex2+projected.vertex3)/3
            line1 = projected.vertex2 - projected.vertex1
            line2 = projected.vertex3 - projected.vertex1
            normal = crossProduct(line1, line2) * normals_length
            DrawTriangle(screen, projected, fill, wireframe,vertices, radius, verticeColor, wireframeColor, lineWidth)
            origins.append(origin)
            normals.append(normal)

        if showAxis:
            DrawAxis(screen, camera)

        if showNormals == True: #---to fix later
            # get the normal vectors
            for i, n in enumerate(normals):
                endPoint = origins[i] + (n)
                #pygame.draw.circle(screen, (0,255, 0), endPoint.GetTuple(), 10)
                pygame.draw.line(screen, (0, 255, 0), origins[i].GetTuple(), endPoint.GetTuple(), 2)

class Mesh:
    def __init__(self, position=Vector3(), scale=1):
        self.triangles = []
        self.position = position
        self.color = (255, 255, 255)
        self.transform = Matrix.identity()
        self.translate = Matrix.identity()
        self.scale = scale
    @classmethod
    def from_file(
        cls,
        fname: PathLike,
        color: tuple[int, int, int],
        position: Optional[Vector3] = None,
    ) -> Mesh:
        triangles = LoadMesh(fname, color)
        return cls(triangles, position)

    @classmethod
    def cube(
        cls, color: tuple[int, int, int], position: Optional[Vector3] = None, scale: float = 1
    ) -> Mesh:
        print(scale)
        tris = CubeTriangles(1, color)
        return cls(tris, position, scale)

    @classmethod
    def icosphere(
        cls,
        color: tuple[int, int, int],
        subdivision=0,
        radius=1,
        position: Optional[Vector3] = None,
    ) -> Mesh:
        tris = IcosphereTriangles(color, subdivision, radius)
        return cls(tris, position)

    # TODO: refactor this method, its way too long
    def update(
        self, screen, fill, wireframe, dt, camera, light, depth, clippingDebug, hue=0
    ):
        tris = []
        normals = []

        for index, triangle in enumerate(self.triangles):
            projected = Triangle()
            projected.verticeColor = triangle.verticeColor
            transformed = Triangle()

            transformed.vertex1 = multiplyMatrixVector(triangle.vertex1+self.position , self.transform)
            transformed.vertex2 = multiplyMatrixVector(triangle.vertex2+self.position , self.transform)
            transformed.vertex3 = multiplyMatrixVector(triangle.vertex3+self.position , self.transform)

            transformed.vertex1 += Vector3(0, 0, Zoffset)
            transformed.vertex2 += Vector3(0, 0, Zoffset)
            transformed.vertex3 += Vector3(0, 0, Zoffset)

            # get the normal vector
            line1 = transformed.vertex2 - transformed.vertex1
            line2 = transformed.vertex3 - transformed.vertex1
            normal = Normalize( crossProduct(line1, line2) )

            temp = transformed.vertex1 - camera.position
            d = dotProduct( temp, normal)
            if d < 0.0 or depth == False:
                if hue != 0:
                    triangle.color = hsv2rgb(hue, 1, 1)

                # print(normal)

                # directional light -> illumination
                # dim = 0.0001
                _light = max(dim, dotProduct(light.direction, normal) ) if light != None else 1
                transformed.color = triangle.Shade(_light)

                transformed.vertex1 = multiplyMatrixVector(transformed.vertex1, camera.viewMatrix )
                transformed.vertex2 = multiplyMatrixVector(transformed.vertex2, camera.viewMatrix )
                transformed.vertex3 = multiplyMatrixVector(transformed.vertex3, camera.viewMatrix )

                clipped = 0
                clippedTriangles = [Triangle() for _ in range(2)]
                clipped = TriangleClipped(Vector3(0, 0, clipping), Vector3(0, 0, 1), transformed, clippedTriangles, clippingDebug)

                for i in range(clipped):
                    #print(clippedTriangles)
                    # project to 2D screen
                    projected.vertex1 = multiplyMatrixVector(clippedTriangles[i].vertex1, camera.projection())
                    projected.vertex2 = multiplyMatrixVector(clippedTriangles[i].vertex2, camera.projection())
                    projected.vertex3 = multiplyMatrixVector(clippedTriangles[i].vertex3, camera.projection())


                    projected.color = clippedTriangles[i].color
                    # fix the inverted x
                    projected.vertex1 *= Vector3(1, -1, 1)
                    projected.vertex2 *= Vector3(1, -1, 1)
                    projected.vertex3 *= Vector3(1, -1, 1)

                    offsetView = Vector3(1, 1, 0)
                    projected.vertex1 = projected.vertex1 + offsetView
                    projected.vertex2 = projected.vertex2 + offsetView
                    projected.vertex3 = projected.vertex3 + offsetView

                    # half_v1 = projected.vertex1 / 2
                    # half_v2 = projected.vertex2 / 2
                    # half_v3 = projected.vertex3 / 2

                    projected.vertex1 *= Vector3(Width, Height, 1) * 0.5
                    projected.vertex2 *= Vector3(Width, Height, 1) * 0.5
                    projected.vertex3 *= Vector3(Width, Height, 1) * 0.5
                    if i == 0 and wireframe == True:
                        pygame.draw.line(screen, (255, 255,255), projected.vertex1.GetTuple(), projected.vertex2.GetTuple(), 1)
                        pygame.draw.line(screen, (255, 255,255), projected.vertex2.GetTuple(), projected.vertex3.GetTuple(), 1)
                        pygame.draw.line(screen, (255, 255,255), projected.vertex3.GetTuple(), projected.vertex1.GetTuple(), 1)
                        #pygame.draw.polygon(screen, projected.color, projected.GetPolygons())
                    if i == 0 and fill==True:
                        # have to fix this part
                        pygame.draw.polygon(screen, projected.color, projected.GetPolygons())

                    tris.append(projected)
                    #DrawTriangle(screen, projected, Fill, wireframe, wireframeColor)

        return tris

def matrix_multiplication(a, b):
        columns_a = len(a[0])
        rows_a = len(a)
        columns_b = len(b[0])
        rows_b = len(b)

        result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
        if columns_a == rows_b:
            for x in range(rows_a):
                for y in range(columns_b):
                    sum = 0
                    for k in range(columns_a):
                        sum += a[x][k] * b[k][y]
                    result_matrix[x][y] = sum
            return result_matrix

        else:
            print("columns of the first matrix must be equal to the rows of the second matrix")
            return None
