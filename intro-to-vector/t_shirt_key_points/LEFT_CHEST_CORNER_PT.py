import cv2
import numpy as np
import matplotlib.pyplot as plt
from _decimal import Decimal



def LEFT_CHEST_CORNER_PT(predictions, t_shirt_builder,filtered_contour, index):
    left_sleeve = [x for x in predictions if x.class_ == "left_sleeve_verified"][0]
    left_sleeve_contour = []
    for point in left_sleeve.points:
        left_sleeve_contour.append((point.x, point.y))
    left_sleeve_contour = np.array(left_sleeve_contour)
    print(left_sleeve_contour)
    t_shirt = [x for x in predictions if x.class_ == "t_shirt"][0]
    t_shirt_contour = []
    for point in t_shirt.points:
        t_shirt_contour.append((point.x, point.y))
    t_shirt_contour = np.array(t_shirt_contour)
    break_both_loops = False
    mIndex = index
    for fIndex, contour in enumerate(filtered_contour):

        if contour[2] < mIndex:
            continue

        print(contour)
        index = 0
        while True:

            # print(border_contour)

            if (abs(left_sleeve_contour[index][0] - contour[0]) +
                    abs(left_sleeve_contour[index][1] - contour[1]) < 11.0):
                print("Hey")
                break
            index = (index + 1)
            if index == len(left_sleeve_contour) - 1:
                print("Helooooooo")
                gIndex = filtered_contour[fIndex - 1][2]
                qIndex = 0
                while True:
                    while True:
                        if (abs(left_sleeve_contour[qIndex][0] - t_shirt_contour[gIndex][0]) +
                                abs(left_sleeve_contour[qIndex][1] - t_shirt_contour[gIndex][1]) < 7.0):
                            print("Hey")
                            gIndex = gIndex + 1
                            qIndex = 0
                            break
                        qIndex = qIndex + 1

                        if qIndex == len(left_sleeve_contour) - 1:

                            print("t-shirt coordinate")
                            print(t_shirt_contour[gIndex][0], t_shirt_contour[gIndex][1])
                            plt.scatter(int(t_shirt_contour[gIndex-1][0]), int(t_shirt_contour[gIndex-1][1]), c='black',
                                    marker='o', s=100, label='Changed Point')

                            t_shirt_builder.LEFT_CHEST_CORNER_PT = t_shirt_builder.LEFT_CHEST_CORNER_PT._replace(
                                coordinates=(int(t_shirt_contour[gIndex-1][0]), int(t_shirt_contour[gIndex-1][1])), border_contour_index=gIndex-1
                            )
                            break_both_loops = True
                            break
                    if break_both_loops:
                        break
            if break_both_loops:
                break

        if break_both_loops:
            break

    # Add labels and a title

    plt.savefig('sleeves_1.png')
