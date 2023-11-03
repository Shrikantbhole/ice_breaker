import cv2
import numpy as np


def LEFT_CHEST_CORNER_PT(border_contour, read_image, t_shirt_builder, index):
    reshaped_contour = border_contour.reshape(border_contour.shape[0], 2)

    while True:
        if reshaped_contour[index][1] < reshaped_contour[index + 1][1]:
            coordinates = tuple(reshaped_contour[index])
            t_shirt_builder.LEFT_CHEST_CORNER_PT = t_shirt_builder.LEFT_CHEST_CORNER_PT._replace(
                coordinates=coordinates, border_contour_index=index
            )
            break

        else:
            index = index + 1
    cv2.circle(read_image, tuple(coordinates), 25, (255, 0, 0), 3)
