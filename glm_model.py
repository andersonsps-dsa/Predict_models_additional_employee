import streamlit as st
import pandas as pd
import calendar
import itertools
import pickle

############ 
def get_days_in_month():
    def get_date(mes_ano):
        mes, ano = map(int, mes_ano.split('/'))
        return calendar.monthrange(ano, mes)[1]

    data_calendar = {'month/year': ['1/2023', '2/2023', '3/2023', '4/2023', '5/2023', '6/2023', '7/2023',
                    '8/2023', '9/2023', '10/2023', '11/2023', '12/2023',
                    '1/2024', '2/2024', '3/2024', '4/2024', '5/2024', '6/2024', '7/2024']}

    dCaled = pd.DataFrame(data_calendar)
    dCaled['Dias_mensais'] = dCaled['month/year'].apply(get_date)
    return dCaled
dCalendar = get_days_in_month()

data_load_state = st.text('Data loading in progress... ⟳')
dataframe = pd.read_csv('AmountService.csv')

############ 
y_endog = dataframe['Mean_Serv_Duration_days']
model_ols = pickle.load(open('model_ols_file.pkl', 'rb'))
model_poisson = pickle.load(open('model_poisson_file.pkl', 'rb'))
fig_ols = pickle.load(open('grafico_ols.pkl', 'rb'))
fig_poisson = pickle.load(open('grafico_poisson.pkl', 'rb'))

model_ols_pred = model_ols.predict()
model_poisson_pred = model_poisson.predict()

########### 
st.title('Predictive Hiring Calculator for IT 💻')
st.write('➤ Filter calculator by IT Team Category:')
st.write('➤ Enter integers | From "Projects" to "Serv. Request": choose between 0 (no) or 1 (yes):')

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    Employee_ = st.number_input("Employee.", value =1,min_value=1, max_value=10,step = 1)
with col2:
    Amount_of_service_ = st.number_input("Amount Serv.",min_value=2, max_value=10,step = 1)       
with col3:
    Project_ =st.number_input("Project",min_value=0, max_value=1, value = 1)
with col4:
    Purchase_Request_ = st.number_input("Purc. Reques.",min_value=0, max_value=1)
with col5:
    Incident_ = st.number_input("Incident",min_value=0, max_value=1)
with col6:
    Layout_Change_ = st.number_input("Mud. Layout",min_value=0, max_value=1)
with col7:
    Service_Request_ =st.number_input("Serv. Reques.",min_value=0, max_value=1)

st.write('Filter by Department for calculator:')
col8, col9, col10 = st.columns(3)
with col8:
    Dashboard_ = st.slider("Dep_Dashboard",
                               value= 0,
                               min_value= 0,
                               max_value=1,
                               step = 1)
with col9:
    Infrastructure_ = st.slider("Dep. Infrastructure",
                               value= 0,
                               min_value= 0,
                               max_value= 1,
                               step = 1)
with col10:
    Systems_ = st.slider("Dep. Systems",
                               value= 1,
                               min_value= 0,
                               max_value=1,
                               step = 1)
###########
try:
    Employee_for_Amount_of_service_ = Amount_of_service_ / Employee_
except:
    Employee_for_Amount_of_service_ = 0

newTable = pd.DataFrame({
    'const': 1,
    'Employee_for_Amount_of_service': Employee_for_Amount_of_service_,
    'Incident' : [Incident_],
    'Layout_Change' : [Layout_Change_],
    'Project' : [Project_],
    'Service_Request' : [Service_Request_],
    'Purchase_Request' : [Purchase_Request_],
    'Dashboard' : [Dashboard_],
    'Infrastructure' : [Infrastructure_],
    'Systems' : [Systems_]
    }, 
    index=[0])

col11, col12 = st.columns(2)
with col11:
    model_choice = st.radio(
        'Choose calculation model:',
        ('OLS', 'Poisson'))

    if model_choice == 'OLS':
        Predict = model_ols.predict(newTable)
    else:
        Predict = model_poisson.predict(newTable)

with col12:
    st.markdown(
        f"""
        <div style="text-align: center; font-size:20px;">
            Results: A workforce of {Employee_} agents is required to complete Project {Amount_of_service_} within a period of {int(round(max(Predict), 0))} days
        </div>
        """, unsafe_allow_html=True)

data_load_state.text('Data uploaded successfully! ✅')

# fig_ols = grafico_ols(y_endog, model_ols_pred)
# fig_poisson = grafico_poisson(y_endog, model_poisson_pred)

if model_choice == "OLS":
    st.write('➲ You are using the OLS model: Data and Graphic.')
    st.plotly_chart(fig_ols, use_container_width=True)
else:
    st.write('➲ You are using the POISSON model:Data and Graphic.')    
    st.plotly_chart(fig_poisson, use_container_width=True)