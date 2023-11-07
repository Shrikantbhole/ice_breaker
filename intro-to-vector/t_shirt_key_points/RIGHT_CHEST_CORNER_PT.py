import cv2
import numpy as np
from decimal  import  Decimal

from matplotlib import pyplot as plt


def RIGHT_CHEST_CORNER_PT(predictions, t_shirt_builder, filtered_contour, index):
    right_sleeve = [x for x in predictions if x.class_ == "right_sleeve_verified"][0]
    right_sleeve_contour = []
    for point in right_sleeve.points:
        right_sleeve_contour.append((point.x, point.y))
    right_sleeve_contour = np.array(right_sleeve_contour)
    print(right_sleeve_contour)
    t_shirt = [x for x in predictions if x.class_ == "t_shirt"][0]
    t_shirt_contour = []
    for point in t_shirt.points:
        t_shirt_contour.append((point.x, point.y))
    t_shirt_contour = np.array(t_shirt_contour)
    break_both_loops = False
    mIndex = index
    print("filter contur len")
    print(len(filtered_contour))
    print(t_shirt_contour[mIndex])

    for fIndex, contour in enumerate(filtered_contour):

        if contour[2] < mIndex:
            continue

        print(contour)
        index = 0
        print(contour)
        while True:

            # print(border_contour)

            if (abs(right_sleeve_contour[index][0] - contour[0]) +
                    abs(right_sleeve_contour[index][1] - contour[1]) < 11.0):
                print("Hey found")
                mIndex = filtered_contour[fIndex - 1][2]

                break_both_loops = True
                break
            index = (index + 1)
            if index == len(right_sleeve_contour) - 1:
                print("Not found")
                break





        if break_both_loops:
            break
        if fIndex == len(filtered_contour) - 1:
            mIndex = filtered_contour[fIndex][2]
            break

    break_both_loops = False
    while True:
        index = 0
        while True:
            if (abs(right_sleeve_contour[index][0] - t_shirt_contour[mIndex][0]) +
                     abs(right_sleeve_contour[index][1] - t_shirt_contour[mIndex][1]) < 7.0):
                    print("Hey")
                    plt.scatter(int(t_shirt_contour[mIndex][0]), int(t_shirt_contour[mIndex][1]), c='black',
                                marker='o', s=100, label='Changed Point')

                    t_shirt_builder.RIGHT_CHEST_CORNER_PT = t_shirt_builder.RIGHT_CHEST_CORNER_PT._replace(
                        coordinates=(int(t_shirt_contour[mIndex][0]), int(t_shirt_contour[mIndex][1])),
                        border_contour_index=mIndex
                    )
                    plt.savefig('sleeves_1.png')
                    break_both_loops = True
                    break
            index = index + 1

            if index == len(right_sleeve_contour) - 1:
                mIndex = mIndex + 1
                print("Nopes")
                break
        if break_both_loops:
            break


    # Add labels and a title




