import cv2
import numpy as np
import os
from PIL import Image

# Load the T-shirt image and the image of the coin
source_directory = 'add_mobile_to_image/t_shirt_images/test'
target_directory = 'add_mobile_to_image/t_shirt_images_with_mobile/test'


def add_mobile_to_image():
    for filename in os.listdir(source_directory):
        if filename.endswith('.jpg'):
            tshirt_image = Image.open(os.path.join(source_directory, filename))

            # Load the coin image with a transparent background (PNG format)
            mobile_image = Image.open('add_mobile_to_image/transparent_mobile.png')
            # Define a brightness factor (e.g., 1.5 for 1.5 times brighter)
            brightness_factor = 0.3


            # Increase the brightness by multiplying pixel values with the factor
            #mobile_image = np.clip(mobile_image.astype(np.float32) * brightness_factor, 0, 255).astype(np.uint8)

            # Get the current dimensions of the image
            width, height = mobile_image.size

            # Calculate the new dimensions for half size
            new_height = int(height * 0.1)
            new_width = int(width * 0.1)
            new_size = (new_width, new_height)
            # Resize the image to half size
            mobile_image = mobile_image.resize(new_size)

            # Define the position (coordinates) where you want to place the coin on the T-shirt
            x_offset = 300  # Adjust as needed
            y_offset = 350  # Adjust as needed
            position = (x_offset, y_offset)  # Adjust as needed

            tshirt_image.paste(mobile_image,position, mobile_image)
            # Get the dimensions of the coin image
            #mobile_height, mobile_width = mobile_image.shape[:2]

            # Create a region of interest (ROI) for the coin on the T-shirt
            #roi = tshirt_image[y_offset:y_offset + mobile_height, x_offset:x_offset + mobile_width]

            # Create a mask for the coin (use the alpha channel of the coin image if available)
            # Blend the coin onto the T-shirt using a different alpha (transparency) value

            # he [:, :, :3] part is used to exclude the alpha channel (if present) from the coin_image to ensure it only
            # contributes to the RGB channels during blending. Please note here shape of coin_image will be (h,w,dimensions)
            # [:, :, :3] is a slicing operation that extracts the first three channels of the image, which are the RGB
            # channels. In Python, image channels are typically indexed from 0, so [:, :, :3] selects the channels 0, 1,
            # and 2, which correspond to the red, green, and blue channels, respectively.

            #alpha = 1  # This parameter controls the weight of the roi image in the final result
            #beta = 50  #: This parameter controls the weight of the coin_image in the final result
            #result = cv2.addWeighted(roi, alpha, mobile_image[:, :, :3], beta, 0)

            # Copy the result back to the T-shirt image
            #tshirt_image[y_offset:y_offset + mobile_height, x_offset:x_offset + mobile_width] = result

            #print("hello")
            # Save or display the T-shirt image with the superimposed coin
            output_filename = os.path.join(target_directory, filename)
            #cv2.imwrite(output_filename, tshirt_image)
            tshirt_image.save(output_filename)


def extract_contour_from_coin_image():
    coin_image = cv2.imread('add_coin_to_image/coin_image.png', cv2.IMREAD_UNCHANGED)

    # Convert image to grey
    gray_image = cv2.cvtColor(coin_image, cv2.COLOR_BGR2GRAY)
    # Applying binary threshold. 90 is threshold value, pixels with value > 90 would be set to 255 and rest to zero
    _, binary_image = cv2.threshold(gray_image, 90, 255, cv2.THRESH_BINARY)

    # Apply Gaussian blur to reduce noise and enhance edges
    blurred_image = cv2.GaussianBlur(binary_image, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred_image, threshold1=50, threshold2=150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    largest_contour = []
    largest_area = 0.0
    # Iterate through the contours
    for contour in contours:
        # Calculate the area of the current contour
        area = cv2.contourArea(contour)

        # Check if the current contour has a larger area than the previous largest contour
        if area > largest_area:
            largest_area = area
            largest_contour = contour

    # Create a mask filled with zeros
    mask = np.zeros_like(gray_image)

    # Draw the largest contour on the mask with white color to fill the area
    cv2.drawContours(mask, [largest_contour], -1, (255), thickness=cv2.FILLED)

    # Use the mask to extract the filled area from the original image
    # in parmeter2 (coin_image) only those pixels will be retained which coincides with mask image pixels, so when you use AND operator
    # between coin_image and mask_coin_image , you will extract the filled area from the original image
    filled_area = cv2.bitwise_and(coin_image, coin_image, mask=mask)
    cv2.imwrite("add_coin_to_image/coin_mask.jpg", filled_area)
