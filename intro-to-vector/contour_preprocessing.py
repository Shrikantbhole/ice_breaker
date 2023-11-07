import cv2
import numpy as np
import matplotlib.pyplot as plt
from _decimal import Decimal


def key_points_identified_by_slope_transition(border_contour):
    i = 0
    filtered_points = []
    for index, point in enumerate(border_contour):
        if index == 0:
            # cv2.circle(image, tuple(border_contour[0]), 2, (255, 255, 0), 4)
            corner_pt = tuple((border_contour[0][0], border_contour[0][1], index))
            slope = abs(Decimal("-0.32"))
            filtered_points.append(corner_pt)
            i = 1
            continue
        if index == len(border_contour) - 11:
            break

        p0 = tuple(border_contour[index])
        # print(corner_pt)
        p1 = tuple(border_contour[index + 1])
        p2 = tuple(border_contour[index + 2])
        p3 = tuple(border_contour[index + 3])
        p4 = tuple(border_contour[index + 4])
        p5 = tuple(border_contour[index + 5])
        p6 = tuple(border_contour[index + 6])
        p7 = tuple(border_contour[index + 7])
        p8 = tuple(border_contour[index + 8])
        p9 = tuple(border_contour[index + 9])
        p10 = tuple(border_contour[index + 10])
        # m0 = (p0[1] - corner_pt[1]) / (p0[0] - corner_pt[0])

        if p1[0] != corner_pt[0]:
            m1 = abs(Decimal((p1[1] - corner_pt[1]) / (p1[0] - corner_pt[0])))
        else:
            m1 = 1000

        if p2[0] != corner_pt[0]:
            m2 = abs(Decimal((p2[1] - corner_pt[1]) / (p2[0] - corner_pt[0])))
        else:
            m2 = 1000

        if p3[0] != corner_pt[0]:
            m3 = abs(Decimal((p3[1] - corner_pt[1]) / (p3[0] - corner_pt[0])))
        else:
            m3 = 1000

        if p4[0] != corner_pt[0]:
            m4 = abs(Decimal((p4[1] - corner_pt[1]) / (p4[0] - corner_pt[0])))
        else:
            m4 = 1000

        if p5[0] != corner_pt[0]:
            m5 = abs(Decimal((p5[1] - corner_pt[1]) / (p5[0] - corner_pt[0])))
        else:
            m5 = 1000

        if p6[0] != corner_pt[0]:
            m6 = Decimal((p6[1] - corner_pt[1]) / (p6[0] - corner_pt[0]))
        else:
            m6 = 1000

        if p7[0] != corner_pt[0]:
            m7 = Decimal((p7[1] - corner_pt[1]) / (p7[0] - corner_pt[0]))
        else:
            m7 = 1000

        if p8[0] != corner_pt[0]:
            m8 = Decimal((p8[1] - corner_pt[1]) / (p8[0] - corner_pt[0]))
        else:
            m8 = 1000

        # m2 = Decimal((p2[1] - corner_pt[1]) / (p2[0] - corner_pt[0]))
        # m3 = Decimal((p3[1] - corner_pt[1]) / (p3[0] - corner_pt[0]))
        # m4 = Decimal((p4[1] - corner_pt[1]) / (p4[0] - corner_pt[0]))
        # m5 = Decimal((p5[1] - corner_pt[1]) / (p5[0] - corner_pt[0]))
        # m6 = Decimal((p6[1] - corner_pt[1]) / (p6[0] - corner_pt[0]))
        # m7 = Decimal((p7[1] - corner_pt[1]) / (p7[0] - corner_pt[0]))
        # m8 = Decimal((p8[1] - corner_pt[1]) / (p8[0] - corner_pt[0]))
        # m9 = Decimal((p9[1] - corner_pt[1]) / (p9[0] - corner_pt[0]))
        # m10 = Decimal((p10[1] - corner_pt[1]) / (p10[0] - corner_pt[0]))
        try:
            1 == 1
            print("Point: " + str(p0[0]) + "-" + str(p0[1]) + "slope: " + str(round(slope, 2)) + " m1: " + str(
                round(m1, 2)) + " m2: " + str(round(m2, 2)) + " m3: " + str(round(m3, 2)))

            if m1 > slope and m2 > slope and m3 > slope and m4 > slope and m5 > slope \
                    and m5 > m1:
                if 1 == 1:
                    # cv2.circle(image, tuple(border_contour[index]), 15, (255, 0, 0), 3)
                    corner_pt = tuple((border_contour[index][0], border_contour[index][1], index))

                    filtered_points.append(corner_pt)
                    p10 = tuple(border_contour[index + 10])
                    i = i + 1
                    # print("Corner point found", corner_pt, i)

                    slope = abs(Decimal((p10[1] - corner_pt[1]) / (p10[0] - corner_pt[0])))
            if m1 < slope and m2 < slope and m3 < slope and m4 < slope and m5 < slope and m5 < m1:
                if 1 == 1:
                    # cv2.circle(image, tuple(border_contour[index]), 15, (255, 0, 0), 3)
                    corner_pt = tuple((border_contour[index][0], border_contour[index][1], index))

                    filtered_points.append(corner_pt)
                    p10 = tuple(border_contour[index + 10])
                    i = i + 1
                    # print("Corner point found", corner_pt, i)
                    slope = abs(Decimal((p10[1] - corner_pt[1]) / (p10[0] - corner_pt[0])))
        except:
            1 == 1
    # plt.imshow(image)
    # plt.show()
    return filtered_points


def key_points_filtered_by_gradient(contour):
    refined_filter_contour = []
    print("Heyya")
    # marked_image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
    # cv2.circle(marked_image, tuple(filtered_contour[0]), 2, (255, 255, 0), 3)
    for i in range(len(contour)):
        try:
            if i == 0:
                continue
            if i == len(contour) - 2:
                break
            prev_point = np.array(contour[i - 1])
            curr_point = np.array(contour[i])
            next_point = np.array(contour[i + 1])

            vector1 = curr_point - prev_point
            vector2 = curr_point - next_point

            dot_product = np.dot(vector1, vector2)
            magnitude1 = np.linalg.norm(vector1)
            magnitude2 = np.linalg.norm(vector2)
            angle = np.arccos(dot_product / (magnitude1 * magnitude2))
            # print("index: ", angle, i + 1)
            print(angle)
            if angle > 2.5:
                # print(contour[i])
                # print(angle)
                refined_filter_contour.append((contour[i][0], contour[i][1], contour[i][2]))
                print(i)
                plt.scatter(contour[i][0], contour[i][1], c='brown', marker='o', s=100, label='Changed Point')

            # Add labels and a title
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.title('Scatter Plot')

            # Show the plot
            plt.show()
            plt.savefig('sleeves_1.png')


        except:
            1 == 1
    print(refined_filter_contour)
    return refined_filter_contour