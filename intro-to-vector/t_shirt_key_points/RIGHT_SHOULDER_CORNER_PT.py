import cv2
import numpy as np


def RIGHT_SHOULDER_CORNER_PT(border_contour, read_image, t_shirt_builder):
    reshaped_contour = border_contour.reshape(border_contour.shape[0], 2)

    min_y_index = np.argmin(reshaped_contour[0, :])
    min_y_coordinate = reshaped_contour[min_y_index]
    coordinates = tuple(min_y_coordinate)

    for index, point in enumerate(reshaped_contour):
        if tuple(border_contour[index]) == coordinates:
            border_contour_index = index
            t_shirt_builder.RIGHT_SHOULDER_CORNER_PT = t_shirt_builder.RIGHT_SHOULDER_CORNER_PT._replace(
                coordinates=coordinates, border_contour_index=border_contour_index
            )

    # print("left sleeve outside point", self.left_sleeve_outside_pt)
    cv2.circle(read_image, tuple(coordinates), 25, (255, 0, 0), 3)
