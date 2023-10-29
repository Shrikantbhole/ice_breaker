import streamlit as st
from llm_response import run_llm
import time
from streamlit_chat import message
from PIL import Image
from streamlit_cropper import st_cropper
import numpy as np
import cv2

from roboflow import Roboflow
rf = Roboflow(api_key="jPnk3SftEgcEmCcfhN0F")
project = rf.workspace().project("chirag-s3e7s/tshirt-evfwv")
model = project.version(4).model

st.header("Ice breaker Helper Bot")
#st.session_state.widget = ''
i = 45
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
def submit():
    with st.spinner("Generating response...."):
        print("Session State " + str(st.session_state))
        cust_query = st.session_state.widget
        generated_response = run_llm(query = cust_query)
        print(generated_response)
        st.session_state["user_prompt_history"].append(cust_query)
        st.session_state["chat_answers_history"].append(generated_response)


def get_scaled_cropped_img(raw_image, top, left, height, width, scale):
    img_height, img_width, img_channels = raw_image.shape
    top_2x = 0 if top - height < 0 else top - height
    bottom_2x = img_height if top + scale * height > img_height else top + scale * height
    left_2x = 0 if left - width < 0 else left - width
    right_2x = img_width if left + scale * width > img_width else left + scale* width
    cropped_image_2x = raw_image[top_2x:bottom_2x, left_2x:right_2x]
    return cropped_image_2x


st.text_input("Prompt", key = "widget", placeholder = "Enter your prompt here ..", on_change = submit)



st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes

img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'], key = 1)
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True, key = 2)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF',  key = 3)
stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)
aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"], key=4)
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]
return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
return_type_dict = {
    "Cropped image": "image",
    "Rect coords": "box"
}
return_type = return_type_dict[return_type_choice]

if img_file:

    img = Image.open(img_file)

    if not realtime_update:
        st.write("Double click to save crop")
    if return_type == 'box':
        rect = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width
        )
        raw_image = np.asarray(img).astype('uint8')
        left, top, width, height = tuple(map(int, rect.values()))
        print("left: " + str(left) + "top: " + str(top) + "width: " + str(width) + "height: " + str(height))
        st.write(rect)
        cv2.rectangle(raw_image, (left, top), (left + width, top + height), (0, 255, 0), thickness=2)
        masked_image_x = raw_image[top:top + height , left:left + width]
        masked_image_2x = get_scaled_cropped_img(raw_image, top, left, height, width, 2)
        masked_image_3x = get_scaled_cropped_img(raw_image, top, left, height, width, 3)
        #masked_image_x[top: top + height, left:left + width] = raw_image[top:top + height , left:left + width]
        st.image(Image.fromarray(raw_image), caption='raw image x')
        st.image(Image.fromarray(masked_image_x), caption='masked image x')
        st.image(Image.fromarray(masked_image_2x), caption='masked image 2x')
        cv2.imwrite('masked_image_2x.jpg', masked_image_2x)
        model.predict("masked_image_2x.jpg", confidence=40, overlap=30).save("prediction.jpg")
        st.image(Image.fromarray(masked_image_3x), caption='masked image 3x')
        cv2.imwrite('masked_image_3x.jpg', masked_image_3x)

    else:
        # Get a cropped image from the frontend
        cropped_img = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width
        )

        # Manipulate cropped image at will
        st.write("Preview")
        _ = cropped_img.thumbnail((150, 150))
        st.image(cropped_img,  width=250)







if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip( st.session_state["chat_answers_history"], st.session_state["user_prompt_history"]):
        i = i + 1
        message(user_query, is_user=True, key= i.__str__())
        i = i + 1
        message(generated_response, key= i.__str__())


