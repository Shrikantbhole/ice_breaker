import streamlit as st
from llm_response import run_llm
import time
from streamlit_chat import message
from PIL import Image, ImageOps
from streamlit_cropper import st_cropper
import numpy as np
import cv2

from roboflow import Roboflow
from roboflow_inference import model_img_prediction, model_json_prediction, Box, calculate_iou, \
    generate_response_based_upon_result, yolo_chirag, yolo_tushar, get_iou_input_and_iou_predicted


st.header("Ice breaker Helper Bot")
# st.session_state.widget = ''
i = 45
print("Hellooooooooo")
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []


def submit():
    with st.spinner("Generating response...."):
        print("Session State " + str(st.session_state))
        cust_query = st.session_state.widget
        generated_response = run_llm(query=cust_query)
        print(generated_response)
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
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True, key=2)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF', key=3)
stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)
scale = st.sidebar.number_input(label="Crop Scale", value=2, step=1)
model = st.sidebar.radio(label="Select Model", options=["blue", "green"], key=4)

# return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
# return_type_dict = {
#    "Cropped image": "image",
#    "Rect coords": "box"
# }
# return_type = return_type_dict[return_type_choice]

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
    if st.button('Submit'):
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
        scaled_cropped_img = get_scaled_cropped_img(raw_image, top, left, height, width, scale)
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
        scaled_cropped_img = get_scaled_cropped_img(raw_image, top, left, height, width, scale)
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
