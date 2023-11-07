import cv2
import numpy as np
import matplotlib.pyplot as plt

def RIGHT_SHOULDER_PT(predictions, t_shirt_builder,filtered_contour):

    index = 0
    right_sleeve = [x for x in predictions if x.class_ == "right_sleeve_verified"][0]
    right_sleeve_contour = []
    for point in right_sleeve.points:
        right_sleeve_contour.append((point.x, point.y))
    right_sleeve_contour = np.array(right_sleeve_contour)
    right_shoulder_coordinate = right_sleeve.corner_coordinate.top_coordinate
    t_shirt_contour = []
    t_shirt = [x for x in predictions if x.class_ == "t_shirt"][0]
    for point in t_shirt.points:
        t_shirt_contour.append((point.x, point.y))
    t_shirt_contour = np.array(t_shirt_contour)
    proximity_index = 0
    deviation = (abs(t_shirt_contour[0][0] - right_shoulder_coordinate[0]) +
                 abs(t_shirt_contour[0][1] - right_shoulder_coordinate[1]))

    while True:
        #print(border_contour)
        if (abs(t_shirt_contour[index][0] - right_shoulder_coordinate[0]) +
                abs(t_shirt_contour[index][1] - right_shoulder_coordinate[1]) < deviation):
            #print("heyaa")
            deviation = abs(t_shirt_contour[index][0] - right_shoulder_coordinate[0]) + abs(t_shirt_contour[index][1] - right_shoulder_coordinate[1])
            print(t_shirt_contour[index])
            print(deviation)
            proximity_index = index

        index = (index + 1)
        if index == len(t_shirt_contour) - 1:
            print("Noppwwww")
            break
    index = 0
    deviation = (abs(right_sleeve_contour[0][0] - t_shirt_contour[proximity_index][0]) +
                 abs(right_sleeve_contour[0][1] - t_shirt_contour[proximity_index][1]))
    sleeve_proximity_index = 0
    while True:
        # print(border_contour)
        if (abs(right_sleeve_contour[index][0] - t_shirt_contour[proximity_index][0]) +
                abs(right_sleeve_contour[index][1] - t_shirt_contour[proximity_index][1]) < deviation):
            # print("heyaa")
            deviation = abs(right_sleeve_contour[index][0] - t_shirt_contour[proximity_index][0]) + abs(
                right_sleeve_contour[index][1] - t_shirt_contour[proximity_index][1])
            print(right_sleeve_contour[index])
            print(deviation)
            sleeve_proximity_index = index

        index = (index + 1)
        if index == len(right_sleeve_contour) - 1:
            print("Noppwwww")
            break
    x = int((t_shirt_contour[proximity_index][0] + right_sleeve_contour[sleeve_proximity_index][0])/2)
    y = int((t_shirt_contour[proximity_index][1] + right_sleeve_contour[sleeve_proximity_index][1]) / 2)
    t_shirt_builder.RIGHT_SHOULDER_PT = t_shirt_builder.RIGHT_SHOULDER_PT._replace(
        coordinates=(x,y), border_contour_index= proximity_index
    )
    print(t_shirt_builder.RIGHT_SHOULDER_PT.coordinates)
    plt.scatter(x, y, c='black', marker='o',
                s=100, label='Changed Point')
    plt.savefig('sleeves_1.png')
    # print("left sleeve outside point", self.left_sleeve_outside_pt)
    #cv2.circle(read_image, tuple(int(cord) for cord in coordinates), 25, (255, 0, 0), 3)
    #cv2.imwrite("Marked_Points.jpg", read_image)

