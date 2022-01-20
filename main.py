import streamlit as st
from PIL import Image
from itertools import cycle

header = st.container()
images = st.container()
col1, col4 = st.columns([7,1])
with header:
    st.title('Welcome to CAPTCHA!')
    st.text('Are you a human? Lets test it!')

with images:
    st.header('Select all pictures with UMBRELLA')
    st.text('Picture not clear? Refresh it')
    filteredImages = ['b1.jpg','b2.jpg','b3.jpg','b4.jpg','b5.jpg','b6.jpg','b7.jpg','b8.jpg']
cols = cycle(st.columns(4))
for idx, filteredImage in enumerate(filteredImages):
    next(cols).image(filteredImage, width=160)

with col1:
    st.button('Refresh')

with col4:
    st.button('Check')

user_input='airplane' #user selection

pred_path='C:/Users/Z004CCDD/Downloads/selectedclasses/pred' #images are stored

images_path=glob.glob(pred_path+'/*.jpg')

pred_dict={} #dictionary

def value(i,transformer,user_input):  
    if(prediction(i,transformer)==user_input):
        return user_input
    else:
        return 'user_input'

for i in images_path: #looping through the images and comparing it with the pred and user selection
    pred_dict[i[i.rfind('/')+1:]]=value(i,transformer,user_input)

print(pred_dict)


        
        

