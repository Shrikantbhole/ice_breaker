from enum import Enum
from collections import namedtuple
from decimal import Decimal
import math
import matplotlib.pyplot as plt

from t_shirt_builder import TShirtBuilder
from t_shirt_key_points.LEFT_SHOULDER_CORNER_PT import *
from t_shirt_key_points.LEFT_CHEST_CORNER_PT import LEFT_CHEST_CORNER_PT
from t_shirt_key_points.LEFT_COLLAR_PT import LEFT_COLLAR_PT
from t_shirt_key_points.LEFT_SLEEVE_INSIDE_PT import LEFT_SLEEVE_INSIDE_PT
from t_shirt_key_points.LEFT_SHOULDER_PT import *
from t_shirt_key_points.LEFT_WAIST_CORNER_PT import LEFT_WAIST_CORNER_PT
from t_shirt_key_points.RIGHT_CHEST_CORNER_PT import RIGHT_CHEST_CORNER_PT
from t_shirt_key_points.RIGHT_COLLAR_PT import RIGHT_COLLAR_PT
from t_shirt_key_points.RIGHT_SHOULDER_CORNER_PT import RIGHT_SHOULDER_CORNER_PT
from t_shirt_key_points.RIGHT_SLEEVE_INSIDE_PT import RIGHT_SLEEVE_INSIDE_PT
from t_shirt_key_points.RIGHT_SLEEVE_OUTSIDE_PT import RIGHT_SLEEVE_OUTSIDE_PT
from t_shirt_key_points.RIGHT_WAIST_CORNER_PT import RIGHT_WAIST_CORNER_PT


def build_t_shirt_key_points(border_contour, image_path):

    read_image = cv2.imread("D:\Desktop\ice-breaker\intro-to-vector\sizing_img.jpg")
    t_shirt = TShirtBuilder()
    LEFT_SHOULDER_PT(border_contour, read_image, t_shirt)
    LEFT_SLEEVE_INSIDE_PT(border_contour, read_image, t_shirt, t_shirt.LEFT_SLEEVE_OUTSIDE_PT.border_contour_index + 1)
    LEFT_CHEST_CORNER_PT(border_contour, read_image, t_shirt, t_shirt.LEFT_SLEEVE_INSIDE_PT.border_contour_index + 1)
    LEFT_WAIST_CORNER_PT(border_contour, read_image, t_shirt, t_shirt.LEFT_CHEST_CORNER_PT.border_contour_index + 1)
    RIGHT_WAIST_CORNER_PT(border_contour, read_image, t_shirt, t_shirt.LEFT_WAIST_CORNER_PT.border_contour_index + 1)
    RIGHT_CHEST_CORNER_PT(border_contour,read_image,t_shirt,t_shirt.RIGHT_WAIST_CORNER_PT.border_contour_index + 1)
    RIGHT_SLEEVE_INSIDE_PT(border_contour, read_image, t_shirt, t_shirt.RIGHT_CHEST_CORNER_PT.border_contour_index + 1)
    RIGHT_SLEEVE_OUTSIDE_PT(border_contour, read_image, t_shirt, t_shirt.RIGHT_SLEEVE_INSIDE_PT.border_contour_index + 1)
    RIGHT_COLLAR_PT(border_contour, read_image, t_shirt, t_shirt.RIGHT_SLEEVE_OUTSIDE_PT.border_contour_index + 1)
    LEFT_COLLAR_PT(border_contour, read_image, t_shirt, t_shirt.RIGHT_COLLAR_PT.border_contour_index + 1)

    #plt.imshow(read_image)
    #plt.show()
    #t_shirt.get_key_points_with_marking(read_image, border_contour)


    print("neck_opening", t_shirt.build_neck_opening().neck_opening)
    print("body length", t_shirt.build_body_length().body_length)
    print("sleeve opening", t_shirt.build_sleeve_opening().sleeve_opening)
    print("left waist  pt", t_shirt.LEFT_WAIST_CORNER_PT)
    print("left collar  pt", t_shirt.LEFT_COLLAR_PT)
    #crawler.get_key_points_with_marking(t_shirt)
    return t_shirt, read_image


def build_t_shirt_left_shoulder_pt(border_contour, image, t_shirt):
    border_contour_reshape = border_contour.reshape(border_contour.shape[0], 2).tolist()

    LEFT_SHOULDER_CORNER_PT(border_contour, image, t_shirt)
    #plt.imshow(read_image)
    #plt.show()
    return t_shirt,image

def build_t_shirt_right_shoulder_pt(border_contour, image, t_shirt):
    border_contour_reshape = border_contour.reshape(border_contour.shape[0], 2).tolist()

    RIGHT_SHOULDER_CORNER_PT(border_contour, image, t_shirt)
    return t_shirt, image









class Crawler:


    def __init__(self, border_contour, t_shirt_builder, image, border_contour_1):
        self.border_contour = border_contour
        self.t_shirt_builder = t_shirt_builder
        self.read_image = cv2.imread(image)
        self.polygon_cp = border_contour_1

    def set_attribute(self, variable, value):
        setattr(self.t_shirt_builder, variable, value)

    def get_image(self):
        grid_interval = 30
        grid_colour = (0,255,0)
        #for y in range(0, self.read_image.shape[0], grid_interval):
         #  cv2.line(self.read_image, (0,y), (self.read_image.shape[1],y),grid_colour,1)
        #for x in range(0, self.read_image.shape[1], grid_interval):
         #  cv2.line(self.read_image, (x,0), (x, self.read_image.shape[0]),grid_colour,1)

        #cv2.imwrite("image_with_grid.jpg",self.read_image)

        plt.imshow(self.read_image)
        plt.show()

        #cv2.imshow("Marked Points", self.read_image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()



    def find_slope(self, coordinates, origin):
        # print(coordinates)
        # print(origin)
        return abs(coordinates[1] - origin[1]) / abs(coordinates[0] - origin[0])


    def calculate_length(self):
        length_between_points = 0
        print("First point on border contour", tuple(self.border_contour[0][0]), self.border_contour.shape)
        outer_point_index = 0
        inner_point_index = 0
        self.get_left_sleeve_outside_pt()
        self.get_all_corner_points_using_polygon_appx()
        print("sleeve inside point", self.left_sleeve_inside_pt)
        print("sleeve outside point", self.left_sleeve_outside_pt)

        for index, point in enumerate(self.border_contour):
            if tuple(self.border_contour[index][0]) == self.left_sleeve_outside_pt:
                outer_point_index = index
                break
        for index, point in enumerate(self.border_contour):
            if tuple(self.border_contour[index][0]) == self.left_sleeve_inside_pt:
                inner_point_index = index
                break

        # print("left sleeve outside point", left_sleeve_outside_point)
        print("sleeve length ", cv2.arcLength(self.border_contour[outer_point_index:inner_point_index], False))
