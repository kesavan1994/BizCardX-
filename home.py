
import mysql.connector
import streamlit as st

from PIL import Image
import easyocr

import numpy as np
import re
import os
import pandas as pd
st.set_page_config(layout='wide',
                    menu_items={
                            'Get Help': 'https://www.extremelycoolapp.com/',
                            'Report a bug': "https://www.extremelycoolapp.com/bug",
                            'About': "# This is a header. This is an *extremely* cool app!"
                        }
                   )
#mysql connection
mydb=mysql.connector.connect(
    host='localhost',
    username='kesavan',
    password='k7alpha',
    database='BizcardEx'
)
mycursor = mydb.cursor(buffered=True)

# mycursor.execute("CREATE DATABASE IF NOT EXISTS BizcardEx")
mycursor.execute("use BizcardEx")

mycursor.execute("""CREATE TABLE IF NOT EXISTS biz(
                        name varchar(10),
                        designation varchar(20),
                        company_name varchar(20),
                        mail varchar(20),
                        mobile_number varchar(20),
                        website varchar(20),
                        area varchar(20),
                        city varchar(20),
                        state varchar(20),
                        pincode varchar(20),
                        photo   LONGBLOB
                        
                        )
                        """)

# mydb.commit()
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData


def save_uploadedFile(uploaded_file):
    with open(os.path.join('tempDir', uploaded_file.name), 'wb') as file:
        file.write(uploaded_file.getbuffer())

col2, col3 = st.columns([1,1])
with col3:
   uploaded_file = st.file_uploader("upload your image",accept_multiple_files=False,type=['jpeg','jpg','png'],key="file_upload")


def load_model():
        reader = easyocr.Reader(['en'],model_storage_directory='.',gpu=False)
        return reader
reader=load_model()

if uploaded_file is not None:
         save_uploadedFile(uploaded_file)
         image = os.getcwd() + "\\" + 'tempDir' + "\\" + uploaded_file.name
         with col3:
            input_image = Image.open(uploaded_file)
            st.image(input_image, width=500)
            with st.spinner("AI is at work"):
                result_text=reader.readtext(image,detail=0)


try:
        name = (result_text[0])

        company = (result_text[-1])

        designation = (result_text[1])

        pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
        mail = [i for i in result_text if re.search(pattern, i)]
        mail = ' '.join(mail)

        mobile_number = [i for i in result_text if re.search("\d{2,3}-\d{3}-\d{4}", i)][0]
        mobile_number = ''.join(mobile_number)

        pattern1 = '(WWW.)+\\w[A-Za-z]+\\w(.com)$'
        website = [i for i in result_text if re.search(pattern1, i)]
        website = ''.join(website)

        a = [i.split(' ') for i in result_text if re.search('^(\\d{1,}) [a-zA-Z0-9\\s]', i)]
        a = [re.sub(r"[;',.]", '', string) for string in a[0]]

        if len(a) > 4:
            area = a[0:3]
            area = ' '.join(area)
            city = a[3]
            state = a[4]
            pincode = [i for i in result_text if re.search('[0-9]{5,7}$', i)]
            pincode = ''.join(pincode)
            # pincode.apply(lambda x: list2str(x))
        elif 3 > len(a) > 0:
            area = a[0:2]
            area = ' '.join(area)
            city = ''
            state = [i.split() for i in result_text if re.search('\\w[A-Za-z] [0-9]{5,7}$', i)][0][0]
            pincode = [i.split() for i in result_text if re.search('\\w[A-Za-z] [0-9]{5,7}$', i)][0][1]
            pincode = ''.join(pincode)

        elif 3 < len(a) < 5:
            area = a[0:3]
            area = ' '.join(area)
            city = a[3]
            state = [i.split() for i in result_text if re.search('\\w[A-Za-z] [0-9]{5,7}$', i)][0][0]
            pincode = [i.split() for i in result_text if re.search('\\w[A-Za-z] [0-9]{5,7}$', i)][0][1]
            pincode = ''.join(pincode)

except:
        st.warning("please upload image")



try:
    name_key = "Name"
    designation_key = 'Designation'
    company_key =  'Company name'
    mail_key ='Mail-id'
    mobile_key = 'Mobile_number'
    website_key='Website'
    area_key  ='Area'
    city_key= 'City'
    state_key='State'
    pincode_key='Pincode'
   
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked = False


    def callback():
        st.session_state.button_clicked = True
   
    with col2:
        name = st.text_input(name_key, value=name.lower(),key=name_key)
        company = st.text_input(company_key,value=company.lower(),key=company_key)
        designation = st.text_input(designation_key,value=designation.lower(), key=designation_key)
        mail = st.text_input(mail_key,value=mail.lower(), key=mail_key)
        mobile_number = st.text_input(mobile_key,value=mobile_number.lower(), key=mobile_key)
        website = st.text_input(website_key,value=website.lower(), key=website_key)
        area = st.text_input(area_key, value=area.lower(), key=area_key)
        city = st.text_input(city_key, value=city.lower(), key=city_key)
        state = st.text_input(state_key,value=state.lower(), key=state_key)
        pincode = st.text_input(pincode_key,value=pincode.lower(), key=pincode_key)
        submitted = st.button("Submit")
            

        if submitted:
            st.session_state.button_clicked = True
            image = os.getcwd() + "\\" + 'tempDir' + "\\" + uploaded_file.name

            photo = convertToBinaryData(image)
            data = {
             "Name": name,
             "designation": designation,
             "company": company,
             "mail-id": mail,
             "mobile_number": mobile_number,
             "website": website,
             "area": area,
             "city": city,
             "state": state,
             "pincode": pincode,
             "photo": photo
         }
            insert = """INSERT INTO biz(name,
                                   designation,
                                   company_name,
                                   mail,
                                   mobile_number,
                                  website,
                                   area,
                                  city,
                                   state,
                                   pincode,
                                   photo) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            insert_blob_tuple = (name,
                              designation,
                              company,
                              mail,
                              mobile_number,
                              website,
                              area,
                              city,
                              state,
                              pincode,
                              photo)
            result = mycursor.execute(insert, insert_blob_tuple)
            mydb.commit()
            st.success("sucessfully insert to db")
except:
    st.write('')
