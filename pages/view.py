import streamlit as st
import mysql.connector
import pandas as pd

#Mysql Db
mydb=mysql.connector.connect(
    host='localhost',
    username='kesavan',
    password='k7alpha',
    database='BizcardEx'
)
mycursor = mydb.cursor(buffered=True)

# database name bizcard
mycursor.execute("use BizcardEx")

col2,col3=st.columns([1,1])

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

def callback():
    st.session_state.button_clicked=True

with col2:
   def local_css(file_name):
            with open(file_name) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

   def remote_css(url):
            st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

   def icon(icon_name):
            st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

   local_css("style.css")
   remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

   icon("search")
   selected = st.text_input('',placeholder="Enter company Name")


   button_1 = st.button("OK",on_click=callback)
   selected = selected.lower()


col4,col5,col6,col7,col8,=st.columns((2,2,2,2,2))
# def view_form():
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked=False

def callback():
    st.session_state.button_clicked =True

try:
    if (button_1 or st.session_state.button_clicked):
        with col2:
            mycursor.execute(f"SELECT * FROM biz where company_name='{selected}'")
            result1 = mycursor.fetchall()
            name1 = st.text_input('Name', result1[0][0], key='Name1')
            company1 = st.text_input('Company Name', result1[0][2], key="company1")
            designation1 = st.text_input('Designation', result1[0][1], key='designation1')
            mail1 = st.text_input("Mail-ID", result1[0][3], key='mail1')
            mobile_number1 = st.text_input("Mobile_Number", result1[0][4], key='mobil_number1')
            website1 = st.text_input("Offical site", result1[0][5], key='website1')
            area1 = st.text_input("Area", result1[0][6], key='area1')
            city1 = st.text_input("City", result1[0][7], key='city1')
            state1 = st.text_input("State", result1[0][8], key='state1')
            pincode1 = st.text_input("Pincode", result1[0][9], key='pincode1')
            bin_img = result1[0][10]
            with open("bin2img.jpg", 'wb') as f1:
                img = f1.write(bin_img)
            with col3:
                photo = st.image("bin2img.jpg")
            #
        with col4:
                update = st.button("Update")
        with col5:
                delete = st.button("Delete")

        if update:
                    st.session_state.button_clicked = True
                    st.progress(99)
                    mycursor.execute("SET sql_safe_updates=0")
                    mycursor.execute(f"""UPDATE biz SET name='{name1}',
                                                                  designation='{designation1}',
                                                                  company_name='{company1}',
                                                                  mail='{mail1}',
                                                                  mobile_number='{mobile_number1}',
                                                                  website='{website1}',
                                                                  area='{area1}',
                                                                  city='{city1}',
                                                                  state='{state1}',
                                                                  pincode='{pincode1}'
                                                      WHERE company_name='{selected}'
                                            """)
                    mydb.commit()
                    st.balloons()

        if delete:
                    st.session_state.button_clicked = True
                    mycursor.execute("SET sql_safe_updates=0")
                    mycursor.execute(f"""DELETE FROM biz WHERE company_name='{selected}' """)
                    mydb.commit()
                    st.balloons()

    mycursor.execute("""SELECT * from biz""")
    result = mycursor.fetchall()
    df=pd.DataFrame(result,columns=['name','designation','company','mail','mobile_number','website','area','city','state','pincode','photo'])
    st.empty()
    df.drop('photo',axis=1,inplace=True)
    st.dataframe(df)
except:
    st.write('')