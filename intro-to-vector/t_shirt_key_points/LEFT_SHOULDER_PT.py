import cv2
import numpy as np


def LEFT_SHOULDER_PT(border_contour, read_image, t_shirt_builder):

    index = 0
    while True:
        print(border_contour)
        if border_contour[index][0] >  border_contour[(index + 1)][0]:
            coordinates = tuple(border_contour[index])
            t_shirt_builder.LEFT_SHOULDER_PT = t_shirt_builder.LEFT_SHOULDER_PT._replace(
                coordinates=coordinates, border_contour_index=index
            )
            print(coordinates)
            break
        else:
            index = (index + 1) % (len(border_contour))

    # print("left sleeve outside point", self.left_sleeve_outside_pt)
    cv2.circle(read_image, tuple(int(cord) for cord in coordinates), 25, (255, 0, 0), 3)
    cv2.imwrite("Marked_Points.jpg", read_image)

