import cv2
import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt


def LEFT_WAIST_CORNER_PT(predictions, t_shirt_builder, filtered_contour, index):
    t_shirt = [x for x in predictions if x.class_ == "t_shirt"][0]
    t_shirt_contour = []
    for point in t_shirt.points:
        t_shirt_contour.append((point.x, point.y))
    t_shirt_contour = np.array(t_shirt_contour)
    mIndex = index
    break_both_loops = False

    while True:
        #print(t_shirt_contour[mIndex])
        #print(abs(t_shirt_contour[mIndex][1] - t_shirt_contour[mIndex + 10][1]) / t_shirt_contour[mIndex][1])

        if (abs(t_shirt_contour[mIndex][1] - t_shirt_contour[mIndex + 10][1]) / t_shirt_contour[mIndex][1] < 0.02) and (
                t_shirt_contour[mIndex][0] <= t_shirt_contour[mIndex + 10][0]):

            print("Heyaa")
            while True:
                if t_shirt_contour[mIndex + 1][1] > t_shirt_contour[mIndex][1]:
                    mIndex = mIndex + 1
                else:
                    print(int(t_shirt_contour[mIndex][0]), int(t_shirt_contour[mIndex][1]))
                    plt.scatter(int(t_shirt_contour[mIndex][0]), int(t_shirt_contour[mIndex][1]), c='black',
                                marker='o', s=100, label='Changed Point')

                    t_shirt_builder.LEFT_WAIST_CORNER_PT = t_shirt_builder.LEFT_WAIST_CORNER_PT._replace(
                        coordinates=(int(t_shirt_contour[mIndex][0]), int(t_shirt_contour[mIndex][1])),
                        border_contour_index=mIndex)
                    plt.savefig('sleeves_1.png')
                    break_both_loops = True

                    break

        if break_both_loops:
            break
        else:

            mIndex = mIndex + 1
