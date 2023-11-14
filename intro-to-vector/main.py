import base64
import os

import streamlit as st

from add_mobile_to_image import add_mobile_to_image
from crawler import build_t_shirt_key_points
from llm_response import run_llm
from streamlit_chat import message
from PIL import Image, ImageOps
from streamlit_cropper import st_cropper
import numpy as np
import cv2
from zipfile import ZipFile
from add_coin_to_image import add_coin_to_image


from rf_sizing_pre_processing import correct_class_for_sleeves, get_corner_coordinates_for_tshirt
from roboflow_inference import model_img_prediction, Box, generate_response_based_upon_result, \
    get_iou_input_and_iou_predicted, model_json_prediction_for_sizing_issue, get_prediction_using_YOLO

st.header("Ice breaker Helper Bot")
# st.session_state.widget = ''
i = 45

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "issue" not in st.session_state:
    st.session_state.issue = 'sizing'


def submit(elseif=None):
    with st.spinner("Generating response...."):
        print("Session State " + str(st.session_state))
        cust_query = st.session_state.widget
        generated_response = run_llm(query=cust_query)
        print(generated_response)
        if "Sizing Issue" in str(generated_response):
            st.session_state.issue = 'sizing'
            print("Session State: " + str(st.session_state.issue))
        elif "Quality Issue" in str(generated_response):
            st.session_state.issue = 'quality'
            print("Session State: " + str(st.session_state.issue))
            
        st.session_state["user_prompt_history"].append(cust_query)
        st.session_state["chat_answers_history"].append(generated_response)


def get_scaled_cropped_img(raw_image, top, left, height, width, scale):
    img_height, img_width, img_channels = raw_image.shape
    top_2x = 0 if top - height < 0 else top - height
    bottom_2x = img_height if top + scale * height > img_height else top + scale * height
    left_2x = 0 if left - width < 0 else left - width
    right_2x = img_width if left + scale * width > img_width else left + scale * width
    cropped_image_2x = raw_image[top_2x:bottom_2x, left_2x:right_2x]
    return cropped_image_2x


st.text_input("Prompt", key="widget", placeholder="Enter your prompt here ..", on_change=submit)

st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes

img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'], key=1)
img_folder = st.sidebar.file_uploader(label = "Upload a folder of images", type = "zip", key = "zipfile")
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True, key=2)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF', key=3)
stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)
scale_input = st.sidebar.number_input(label="Crop Scale", value=2, step=1)
model = st.sidebar.radio(label="Select Model", options=["blue", "green"], key=4)
selected_folder = st.sidebar.selectbox("Select a folder: ", ["images", "images_2"])
check_images = st.sidebar.button(label = "Check Images")
download_images = st.sidebar.button(label = "Download Images")


# return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
# return_type_dict = {
#    "Cropped image": "image",
#    "Rect coords": "box"
# }
# return_type = return_type_dict[return_type_choice]

if st.button('Add Coin'):
    add_mobile_to_image.add_mobile_to_image()

if img_folder:
    with open("temp.zip", "wb") as f:
        f.write(img_folder.read())
    # Extract all contents of zip folder to a temporary folder
    with  ZipFile("temp.zip", "r") as zip_ref:
        zip_ref.extractall("predict")
    st.success("Folder uploaded and extracted successfully")


IMAGE_CHECKED = False
if check_images:
    # Display the list of images in the uploaded folder
    print(selected_folder)
    directory = "samples/" + selected_folder
    image_files = [f for f in os.listdir(directory )]
    for image_file in image_files:
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)
        st.image(image, use_column_width=True)
    IMAGE_CHECKED = True
    #st.write("List of images in  the uploaded folder:")
    #print(image_files)
    #st.write(image_files[0])

if download_images:
    directory = "samples/" + selected_folder
    image_files = [f for f in os.listdir(directory)]
    zip_file_name = f"{selected_folder}_images.zip"

    with st.spinner(f"Creating {zip_file_name}.... "):
        st.write("Downloading...")
        with ZipFile(zip_file_name, 'w') as zipf:
            for image_file in image_files:
                image_path = os.path.join(directory, image_file)
                zipf.write(image_path, os.path.basename(image_file))
        with open(zip_file_name, "rb") as f:
            zip_contents = f.read()

        # Encode the zip file as base64
        zip_b64 = base64.b64encode(zip_contents).decode()
        href = f'<a href="data:application/zip;base64,{zip_b64}" download="{zip_file_name}">Click here to download</a>'
        st.markdown(href, unsafe_allow_html=True)

if img_file:

    img = Image.open(img_file)
    img = ImageOps.exif_transpose(img)
    width, height = img.size

    if width > 200.0:
        new_height = height / width * 200.0
        new_width = 200.0
        img = img.resize((int(new_width), int(new_height)))

    elif height > 200.0:
        new_width = width / height * 200.0
        new_height = 200.0
        img = img.resize((int(new_width), int(new_height)))



    if not realtime_update:
        st.write("Double click to save crop")

    rect = st_cropper(
        img,
        realtime_update=realtime_update,
        box_color=box_color,
        aspect_ratio=(1, 1),
        return_type="box",
        stroke_width=stroke_width
    )
    CHEST = []
    SHOULDER = []
    TSHIRT = []
    if st.button('Submit'):
        print("Session State: " + str(st.session_state))
        if st.session_state.issue == "sizing":
            directory = "predict/images"
            image_files = [f for f in os.listdir(directory)]
            for image_file in image_files:
                img = Image.open(os.path.join(directory,image_file))
                raw_image = np.asarray(img).astype('uint8')
                bgr_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite('sizing_img.jpg', bgr_image)
                predictions = model_json_prediction_for_sizing_issue("sizing_img.jpg")
                predictions = get_corner_coordinates_for_tshirt(predictions)
                corrected_predictions = correct_class_for_sleeves(predictions)
                #print("Corrected Predictions")
                #print(corrected_predictions)
                chest_length, shoulder_length, tshirt_length = build_t_shirt_key_points(corrected_predictions)
                CHEST.append(chest_length)
                SHOULDER.append(shoulder_length)
                TSHIRT.append(tshirt_length)

            print(f"chest: " + str(sum(CHEST)/len(CHEST)))
            print(f"shoulder: " + str(sum(SHOULDER) / len(SHOULDER)))
            print(f"tshirt: " + str(sum(TSHIRT) / len(TSHIRT)))



        if st.session_state.issue == "quality":
            print("Session State: " + str(st.session_state))
            st.session_state["user_prompt_history"] = []
            st.session_state["chat_answers_history"] = []
            st.write('We are working on your query. Please wait.')

            raw_image = np.asarray(img).astype('uint8')
            left, top, width, height = tuple(map(int, rect.values()))
            input_box = Box(
                x=left,
                y=top,
                width=width,
                height=height
            )
            scaled_cropped_img = get_scaled_cropped_img(raw_image, top, left, height, width, scale_input)
            bgr_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite('scaled_cropped_img.jpg', bgr_image)
            model = yolo_tushar()
            iou_input, iou_predicted = get_iou_input_and_iou_predicted(model, input_box)
            result, generated_response = generate_response_based_upon_result(iou_input, iou_predicted)
            message(generated_response, key=i.__str__())

    if st.button('Retry'):
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_answers_history"] = []
        st.write('We are working on your query. Please wait.')

        raw_image = np.asarray(img).astype('uint8')
        left, top, width, height = tuple(map(int, rect.values()))
        input_box = Box(
            x=left,
            y=top,
            width=width,
            height=height
        )
        scaled_cropped_img = get_scaled_cropped_img(raw_image, top, left, height, width, scale_input)
        bgr_image = cv2.cvtColor(raw_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite('scaled_cropped_img.jpg', bgr_image)
        model = yolo_chirag()
        iou_input, iou_predicted = get_iou_input_and_iou_predicted(model, input_box)
        result, generated_response = generate_response_based_upon_result(iou_input, iou_predicted)
        if result == True:
            generated_response = "Apologies for my earlier reply. " + generated_response
        message(generated_response, key=i.__str__())

if st.button('Check result'):
    if model == "blue":
        model = yolo_tushar()
    else:
        model = yolo_chirag()

    st.write('We are working on your query. Please wait.')
    predicted_image_file = model_img_prediction(model, 'scaled_cropped_img.jpg')
    predicted_image = Image.open(predicted_image_file)
    predicted_image = np.asarray(predicted_image).astype('uint8')
    st.image(Image.fromarray(predicted_image), caption='Predicted Image')

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(st.session_state["chat_answers_history"],
                                              st.session_state["user_prompt_history"]):
        i = i + 1
        message(user_query, is_user=True, key=i.__str__())
        i = i + 1
        message(generated_response, key=i.__str__())
