import streamlit as st
import datetime
import time
from PIL import Image
import sqlite3
from streamlit_lottie import st_lottie
import json
import requests
import pandas as pd

import functions as fu
import time_journal as tj
import chart 

#Connect to Database
#C:\Users\seren\OneDrive\Documents\Python project\Time Management app\tm_db.db
db = sqlite3.connect('./tm_db.db')
#Use this run sql statements
cur = db.cursor()

#Variables init
u_login=None
selected_start_time = None
selected_end_time = None 
duration = 0
t = 'Pre-set'
update = None
value = 0
time_output = 0
log_state = None

#'C:\Users\seren\OneDrive\Documents\Python project\Time Management app\timewise_logo.png
#logo & Setup
favicon =Image.open('./timewise_logo.png')
st.set_page_config(
    page_title="TimeWise",
    page_icon=favicon,
    initial_sidebar_state="expanded",
)

#log in info
with st.sidebar:
    global un   
    un = st.text_input("Username")
    pw = st.text_input("Password",type='password')
    
    b1, b2 = st.columns(2)
    
    #b1:sign up
    with b1:
        if st.button('Sign Up'):

            if fu.check_empty(un, pw):
                user_sql='select user_name from user'
                cur.execute(user_sql)
                #To obtain all data from the user_name column in [('x','y'),('a','b')] data structure
                u=cur.fetchall()
                #Convert original ds to a list
                user_list = fu.unpack(tup=u)
                #Check if user exist
                if un in user_list:
                    st.warning('User already exist!')
                else:
                #if user doesn't exist
                    insert_sql = "insert into user('user_name','password') values(?,?)"
                    cur.execute(insert_sql,(un,pw))
                    db.commit()
                    st.success('User is added successfully! Please log in.', icon="✅")
   
    #discription
    st.write('                           ')
    st.write('                            ')
    st.write('                            ')
    st.write('TimeWise is designed to make time management a breeze, ensuring users stay organized, make the most of their time, and achieve their goals efficiently. With its sleek design and powerful features, TimeWise empowers users to optimize their productivity and achieve a better work-life balance.')
    st.write('                            ')

    #C:\Users\seren\OneDrive\Documents\Python project\Time Management app\timewise_logo.png
    logo = Image.open('./timewise_logo.png')
    st.image(logo, caption=None, width=100)
         
    #b2:log in           
    with b2:
        if 'u_login' not in st.session_state:
            st.session_state.u_login = None
               
        if st.button('Log In'):

            if fu.check_empty(un, pw):

                user_password = "select * from user where user_name = ? and password = ?"
                # if can fetch data from db, user exist
                if cur.execute(user_password, (un,pw)).fetchone():
                    st.success('Log in successfully', icon="✅")
                    log_state = 'YES'
                    u_login=un
                    st.balloons()
                    st.session_state.u_login = un
                    
                else:
                    st.warning('Username or password is incorrect')

#Header
if st.session_state.u_login == None:
    st.header("Welcome to TimeWise!")

else:
    style = 'font-size: 30px; color:#518af0; font-family: Indie Flower, cursive; font-weight: bold;'
    st.markdown(f'<p style="{style}">Welcome to TimeWise {st.session_state.u_login}!</p>', unsafe_allow_html=True)


col1, col2 = st.columns(2)
# Task
with col1:
    selected_task = st.selectbox('Choose Your Task:', fu.task_list(un) , help="Select from list")

    if selected_task == "Add Custom Task":
        if st.session_state.u_login == None:
            st.warning('Please log in first')
        else:   
            custom_task = st.text_input("Enter Custom Task:")
            
            if custom_task: 
                insert_sql = "INSERT INTO task (type, username) VALUES (?, ?)"
                cur.execute(insert_sql, (custom_task,un ))
                db.commit()
                st.write('Success! Please select Add Custom Task again to see added Task ')
                selected_task = custom_task
            
#Choose today's date
with col2:
    selected_date = st.date_input("Date:", datetime.date.today())
    selected_date_string = selected_date.strftime("%Y-%m-%d")


current_time = datetime.datetime.now().strftime('%I:%M %p')
current_time2 = datetime.datetime.now()

hour3 = current_time2.hour
minute3 = current_time2.minute

t1, t2 = st.columns(2)

with t2:
    #variable init
    hour = 0    #start time
    minute = 0
    hour2 = 0  #end time
    minute2 = 0
    duration2 = None
    state2 = None
    if st.checkbox('Select your start time'):
        t = 'Pre-set'
        hour += st.slider("Select the hour", 0, 12, key='start_slider1')
        minute += st.slider("Select the minute", 0, 59, key='start_slider2')
        ap = ['AM', 'PM']
        option = st.radio('', ap, key='option1')
        selected_start_time = f"{hour:02d}:{minute:02d} {option}"
        if option == 'PM':
            hour += 12

    else:
        selected_start_time = current_time
        state2 = 'no change'

with t1:
    st.write(":clock1: Start time:", selected_start_time)

t3, t4 = st.columns(2)
seconds = 0
with t4:
    if st.checkbox('Select your end time'):
        hour2 += st.slider("Select the hour", 0, 12, key='end_slider1')
        minute2 += st.slider("Select the minute", 0, 59, key='end_slider2')
        ap2 = ['AM', 'PM']
        option2 = st.radio('', ap2, key='option2')
        selected_end_time = f"{hour2:02d}:{minute2:02d} {option2}"
        s_e_t = hour2+minute2/60
        if option2 == 'PM':
            hour2 += 12
        if st.button('Record'):
            if st.session_state.u_login == None:
                st.warning('Please login first')
            else:
                st.success('Success!', icon="✅")           
                t = 'Pre-set'
                hour_interval = abs(hour2 - hour)
                minute_interval = abs(minute2 - minute)               
                # convert to seconds for pichart
                seconds += int(hour_interval * 3600 + minute_interval*60)

                if hour_interval == 0:
                    duration2 = f"{minute_interval}Min(s)"
                    insert_date_sql = "insert into journal(username, task, date, start, end, duration, type, seconds) values(?,?,?,?,?,?,?,?)"
                    cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t,seconds))
                    db.commit()
                if minute_interval == 0:
                    duration2 = f"{hour_interval}Hour(s)"
                    insert_date_sql = "insert into journal(username, task, date, start, end, duration, type, seconds) values(?,?,?,?,?,?,?,?)"
                    cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t,seconds))
                    db.commit()
                else:
                    duration2 = f"{hour_interval}Hour(s) {minute_interval}Min(s)"
                    insert_date_sql = "insert into journal(username, task, date, start, end, duration, type, seconds) values(?,?,?,?,?,?,?,?)"
                    cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t, seconds))
                    db.commit()
                if state2 == 'no change':
                    hour_interval = abs(hour2 - hour3)
                    minute_interval = abs(minute2 - minute3)
                    if hour_interval == 0:
                        duration2 = f"{minute_interval}Min(s)"
                        insert_date_sql = "insert into journal(username, task, date, start, end, duration, type) values(?,?,?,?,?,?,?)"
                        cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t, seconds))
                        db.commit()
                    if minute_interval == 0:
                        duration2 = f"{hour_interval}Hour(s)"
                        insert_date_sql = "insert into journal(username, task, date, start, end, duration, type) values(?,?,?,?,?,?,?)"
                        cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t, seconds))
                        db.commit()
                    else:
                        duration2 = f"{hour_interval}Hour(s) {minute_interval}Min(s)"
                        insert_date_sql = "insert into journal(username, task, date, start, end, duration, type) values(?,?,?,?,?,?,?)"
                        cur.execute(insert_date_sql, (un, selected_task,selected_date_string,selected_start_time,selected_end_time,duration2,t, seconds))
                        db.commit()
        
    else:
        selected_end_time = current_time

if update == "True":
    last_row_sql = "SELECT * FROM journal WHERE username = ? ORDER BY username DESC LIMIT 1"
    cur.execute(last_row_sql, (un,))
    last_row = cur.fetchone()

with t3:
    st.write(":alarm_clock: End time:", selected_end_time)

#Stopwatch 
col3, col4 = st.columns([3, 1])
col5, col6 = st.columns(2)
with col3:
    st.write(':hourglass_flowing_sand: OR You Can Use a Stopwatch :point_down:')
    with st.form('OR You Can Use a Stopwatch'):
        if 'start_time' not in st.session_state:
            st.session_state.start_time = 0
            st.session_state.duration = 0
            st.session_state.time_elapsed = 0

        if st.form_submit_button('Start'):
            t = 'Stopwatch'
            st.session_state.start_time = time.time()  # Get the current time in seconds
            if selected_task != "Add Custom Task":
                st.write('Stopwatch Started! Go ' + selected_task.lower() + ":smile:")
            else:
                st.write('Stopwatch Started! :smile:')
            
        if st.form_submit_button('Check how much time has passed'):
            end_time = time.time()  # Get the current time in seconds
            st.session_state.time_elapsed = end_time - st.session_state.start_time

            unit = "Second(s)"
            time_output += int(st.session_state.time_elapsed)
            fu.unit(time_output)

        if st.form_submit_button('Stop & Record'):
            if st.session_state.u_login == None:
                st.warning('Please login first')
            else:
                if st.session_state.duration == 0:
                    st.warning('Please start the stopwatch')
                else:
                    end_time = time.time()  # Get the current time in seconds
                    st.session_state.time_elapsed = end_time - st.session_state.start_time
                    unit = "Second(s)"
                    time_output += int(st.session_state.time_elapsed)
                    fu.unit(time_output)
                    st.success('Success!', icon="✅")
                    t = 'Stopwatch'
                    seconds += int(st.session_state.time_elapsed)
                    duration = st.session_state.duration if st.session_state.duration else "N/A"
                    insert_date_sql = "INSERT INTO journal (username, task, date, start, end, duration, type, seconds) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    cur.execute(insert_date_sql, (un, selected_task, selected_date_string, selected_start_time, selected_end_time, duration, t, seconds))
                    db.commit()
        
        if st.form_submit_button('Clear'):
            st.session_state.duration = 0


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:  
        return None  
    return r.json()

with col4:
    image = Image.open('./Stopwatch.png')
    st.image(image, caption=None, width=100)
    url = "https://assets1.lottiefiles.com/private_files/lf30_ohuluwv5.json"
    animation_data = load_lottieurl(url)
    st_lottie(animation_data)

if st.button("See Time Journal"):
    if st.session_state.u_login == None:
        st.warning('Please login first')
    else:
        log = tj.read_data(u=un)
        log_df = log[['task', 'date', 'start', 'end', 'duration', 'type']]
        st.dataframe(log_df)
        task_list1 = log['task'].tolist()
        second_list2 = log['seconds'].tolist()
        fig = chart.pie_chart(task_list1, second_list2)
        st.plotly_chart(fig)

#change button color to blue
st.write('<style>div.stButton > color: black; button:first-child {background: linear-gradient(to right,#c5e6fc, #8ad0ff);}</style>', unsafe_allow_html=True)






