
from contour_preprocessing import key_points_identified_by_slope_transition, key_points_filtered_by_gradient
from t_shirt_builder import TShirtBuilder
from t_shirt_key_points.LEFT_CHEST_CORNER_PT import LEFT_CHEST_CORNER_PT
from t_shirt_key_points.LEFT_SHOULDER_PT import *
from t_shirt_key_points.LEFT_WAIST_CORNER_PT import LEFT_WAIST_CORNER_PT
from t_shirt_key_points.RIGHT_CHEST_CORNER_PT import RIGHT_CHEST_CORNER_PT
from t_shirt_key_points.RIGHT_SHOULDER_PT import RIGHT_SHOULDER_PT
from t_shirt_key_points.RIGHT_SHOULDER_CORNER_PT import RIGHT_SHOULDER_CORNER_PT
from t_shirt_key_points.RIGHT_WAIST_CORNER_PT import RIGHT_WAIST_CORNER_PT


def build_t_shirt_key_points(predictions):

    read_image = cv2.imread("sizing_img.jpg")
    t_shirt_builder = TShirtBuilder()
    t_shirt_contour = []
    t_shirt_class = [x for x in predictions if x.class_ == "t_shirt"][0]
    for point in t_shirt_class.points:
        t_shirt_contour.append((point.x, point.y))
    t_shirt_contour = np.array(t_shirt_contour)
    filtered_contour = key_points_identified_by_slope_transition(t_shirt_contour)
    filtered_contour = key_points_filtered_by_gradient(filtered_contour)

    LEFT_SHOULDER_PT(predictions, t_shirt_builder ,filtered_contour)
    LEFT_CHEST_CORNER_PT(predictions,  t_shirt_builder, filtered_contour, t_shirt_builder.LEFT_SHOULDER_PT.border_contour_index + 1)
    LEFT_WAIST_CORNER_PT(predictions,  t_shirt_builder, filtered_contour, t_shirt_builder.LEFT_CHEST_CORNER_PT.border_contour_index + 1)
    RIGHT_WAIST_CORNER_PT(predictions,  t_shirt_builder ,filtered_contour, t_shirt_builder.LEFT_WAIST_CORNER_PT.border_contour_index + 1)
    RIGHT_CHEST_CORNER_PT(predictions,  t_shirt_builder ,filtered_contour, t_shirt_builder.RIGHT_WAIST_CORNER_PT.border_contour_index + 1)
    RIGHT_SHOULDER_PT(predictions, t_shirt_builder, filtered_contour)
    chest_length = t_shirt_builder.RIGHT_CHEST_CORNER_PT.coordinates[0] - t_shirt_builder.LEFT_CHEST_CORNER_PT.coordinates[0]
    print("chest length: " + str(chest_length) )
    shoulder_length = t_shirt_builder.RIGHT_SHOULDER_PT.coordinates[0] - \
                   t_shirt_builder.LEFT_SHOULDER_PT.coordinates[0]
    print("shoulder length: " + str(shoulder_length))
    coords = t_shirt_contour[t_shirt_builder.LEFT_WAIST_CORNER_PT.border_contour_index
                            :t_shirt_builder.RIGHT_WAIST_CORNER_PT.border_contour_index]
    coords = coords.reshape(coords.shape[0], 2).tolist()
    y_coords = [coord[1] for coord in coords]
    average_y_waist = sum(y_coords) / len(y_coords)
    print(average_y_waist)
    y_neck = t_shirt_class.corner_coordinate.top_coordinate[1]
    plt.scatter(int(t_shirt_class.corner_coordinate.top_coordinate[0]), int(t_shirt_class.corner_coordinate.top_coordinate[1]), c='black',
                marker='o', s=100, label='Changed Point')
    plt.savefig('sleeves_1.png')

    tshirt_length = average_y_waist - y_neck
    print("tshirt length: " + str(tshirt_length))
    print("C/S: " )
    print(round(chest_length/shoulder_length, 2))
    print("C/L: ")
    print(round(chest_length / tshirt_length,2))
    print("S/L: ")
    print(round(shoulder_length / tshirt_length,2))
    return t_shirt_builder













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
        grid_colour = (0 ,255 ,0)
        # for y in range(0, self.read_image.shape[0], grid_interval):
         #  cv2.line(self.read_image, (0,y), (self.read_image.shape[1],y),grid_colour,1)
        # for x in range(0, self.read_image.shape[1], grid_interval):
         #  cv2.line(self.read_image, (x,0), (x, self.read_image.shape[0]),grid_colour,1)

        # cv2.imwrite("image_with_grid.jpg",self.read_image)

        plt.imshow(self.read_image)
        plt.show()

        # cv2.imshow("Marked Points", self.read_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()



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
