import numpy as np

def gen_map(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[0]-1, grid[1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[0], grid[1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[0]-1, grid[1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[0]) + t[0]*n10
    n1 = n01*(1-t[0]) + t[0]*n11
    return np.sqrt(2)*((1-t[1])*n0 + t[1]*n1)

from math import sin, cos
import pygame

class pyg_Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def key_check(self, key):
        keys = pygame.key.get_pressed()

        if (keys[key]):
            return True

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()

class pyg_Mesh:
    def __init__(self, verts, edges, x, y, z, rotX, rotY, rotZ, scale):
        self.verts = verts
        self.edges = edges
        self.x = x
        self.y = y
        self.z = z
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scale = scale

    def project_and_rotate(self, x, y, z):
        px = (((x * cos(self.rotZ) - sin(self.rotZ) * y) * cos(self.rotY) - z * sin(self.rotY)) * (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX)) + 5) + self.z))) * self.scale + self.x
        py = (((y * cos(self.rotZ) + x * sin(self.rotZ)) * cos(self.rotX) - (z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * sin(self.rotX)) * (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX)) + 5) + self.z))) * self.scale + self.y
        
        return (int(px), int(py))

    def render(self, window):
        window.screen.fill((0, 0, 0))

        for vert in self.verts:
            point = self.project_and_rotate(vert[0], vert[1], vert[2])

            pygame.draw.circle(window.screen, (0, 255, 0), point, 6)

        for edge in self.edges:
            point1 = self.project_and_rotate(self.verts[edge[0]][0], self.verts[edge[0]][1], self.verts[edge[0]][2])
            point2 = self.project_and_rotate(self.verts[edge[1]][0], self.verts[edge[1]][1], self.verts[edge[1]][2])

            pygame.draw.line(window.screen, (0, 255, 0), point1, point2, 5)


class pyg_Cube:
    def __init__(self, x, y, z, rotX, rotY, rotZ, scale):
        self.verts = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, -1), (0, 1, -1), (1, 1, -1), (1, 0, -1)]
        self.edges = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
        self.x = x
        self.y = y
        self.z = z
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scale = scale

    def project_and_rotate(self, x, y, z):
        px = (((x * cos(self.rotZ) - sin(self.rotZ) * y) * cos(self.rotY) - z * sin(self.rotY)) * (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX)) + 5) + self.z))) * self.scale + self.x
        py = (((y * cos(self.rotZ) + x * sin(self.rotZ)) * cos(self.rotX) - (z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * sin(self.rotX)) * (200 / ((((z * cos(self.rotY) + (x * cos(self.rotZ) - sin(self.rotZ) * y) * sin(self.rotY)) * cos(self.rotX) + (y * cos(self.rotZ) + x * sin(self.rotZ)) * sin(self.rotX)) + 5) + self.z))) * self.scale + self.y
        
        return (int(px), int(py))

    def render(self, window):
        window.screen.fill((0, 0, 0))

        for vert in self.verts:
            point = self.project_and_rotate(vert[0], vert[1], vert[2])

            pygame.draw.circle(window.screen, (0, 255, 0), point, 6)

        for edge in self.edges:
            point1 = self.project_and_rotate(self.verts[edge[0]][0], self.verts[edge[0]][1], self.verts[edge[0]][2])
            point2 = self.project_and_rotate(self.verts[edge[1]][0], self.verts[edge[1]][1], self.verts[edge[1]][2])

            pygame.draw.line(window.screen, (0, 255, 0), point1, point2, 5)

