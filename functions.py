import streamlit as st
import sqlite3
import time

def unpack(tup):
    t_list=[]
    for i in tup:
        t_list.append(i[0])
    return t_list

def check_empty(un, pw):
    if un.strip() == '' and pw.strip() == '':
                st.warning('Please enter a username and a password')
                return False
    elif un.strip() == '':
        st.warning('Please enter a username')
        return False
    elif pw.strip() == '':
            st.warning('Please enter a password')
            return False
    else:
        return True

def task_list(un):  
    #Connect to Database
    db = sqlite3.connect('./tm_db.db')
    #Use this run sql statements
    cur = db.cursor()  
    #Display public and customize tasks
    task_sql = "SELECT type FROM task WHERE username = 'Public' or username = ?"
    t=cur.execute(task_sql,(un,)).fetchall()
    task_list = unpack(tup=t)
    # Append the "Add Custom Task" option to the task_list
    task_list.append('Add Custom Task')
    return task_list

def unit(time_output):
    unit = "Second(s)"
    if time_output < 60:
        time_string = "Time Elapsed: " + str(time_output) + " " + unit
        time_string2 = str(time_output) + " " + unit
        st.write(time_string)
        st.write("Press 'Start' again to Restart")
        st.session_state.duration = time_string2
    elif time_output < 3600:
        unit = "Minute(s)"
        value3 = time_output // 60
        time_string = "Time Elapsed: " + str(value3) + " " + unit
        time_string2 = str(value3) + " " + unit
        st.write(time_string)
        st.write("Press 'Start' again to Restart")
        st.session_state.duration = time_string2
    else:
        unit = "Hour(s)"
        value2 = time_output // 3600
        time_string = "Time Elapsed: " + str(value2) + " " + unit
        time_string2 = str(value2) + " " + unit
        st.write(time_string)
        st.write("Press 'Start' again to Restart")
        st.session_state.duration = time_string2
