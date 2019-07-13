from shapely.geometry import Polygon
from shapely.geometry import Point

class CoordinateSystem:
    rectangle1 = []
    rectangle2 = []
    centreOfRectangle2 = None

    def __init__(self, rectangles):
        self.rectangle1, self.rectangle2 = rectangles
        self.centreOfRectangle2 = self.getCentreOfRectangle(self.rectangle2)

    def getCentreOfRectangle(self,coordinates):
        p = Polygon(coordinates)
        bound = p.bounds
        centreX = (bound[2] + bound[0])/2
        centreY = (bound[3] + bound[1])/2
        return centreX,centreY