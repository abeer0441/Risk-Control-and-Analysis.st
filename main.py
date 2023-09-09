import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import streamlit.components.v1 as components
from streamlit import session_state as state
from types import SimpleNamespace
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from numerize.numerize import numerize
import os
from PIL import Image
import subprocess

st.set_page_config(page_title="Risk Control and Analysis", page_icon="📊",layout='wide', initial_sidebar_state='expanded')
st.set_option('deprecation.showPyplotGlobalUse', False)

response = requests.post('https://risk-control-and-analysis-0974368b9653.herokuapp.com//get_data')
data = response.json()

# Process and display the data
df = pd.read_json(data["df"])

st.markdown("<h1 style='text-align: center; font-size: 60px;'>Analysis and Control Risks</h1>", unsafe_allow_html=True)

fieldset_style = "border: 1px dashed gray; align-items: center; padding: 10px; border-radius: 10px; width: 1100px; box-shadow: 2px 2px 5px black; background-color: #f7f7f7;"
input_style = "border: none; padding: 5px; margin-left: 20px; margin-bottom: 5px; background-color: #f7f7f7; color: darkred; font-weight: bold;"
label_style = "font-weight: bold; margin: 5px; padding: 10px"

components.html(f'''<form action="info" method="post">
    <fieldset style = "{fieldset_style}">
        <label for="Name" style = "{label_style}"> Sector name: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["sector_name"] if data["info"]["sector_name"] else ''} disabled="disabled" />
        <label for="Name" style = "{label_style}"> Project name: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["project_name"] if data["info"]["project_name"] else ''} disabled="disabled" />
        <label for="Name" style = "{label_style}"> Business unit: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["business_unit"] if data["info"]["business_unit"] else ''} disabled="disabled" />
        <br />
        <label for="Name" style = "{label_style}"> Contractore: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["contractor"] if data["info"]["contractor"] else ''} disabled="disabled" />
        <label for="Name" style = "{label_style}"> Project's cost: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["project_cost"] if data["info"]["project_cost"] else ''} disabled="disabled" />
        <label for="Name" style = "{label_style}"> Project duration: </label>
        <input type="text" maxlength="12" style = "{input_style}" {"value="+data["info"]["project_duration"] if data["info"]["project_duration"] else ''} disabled="disabled" />
    </fieldset></form>''')
    
   
tab1, tab2, tab3 = st.tabs(["General", "High risk", "Response plan"])
    
with tab1:

        outer_cols = st.columns([1.5,1])
        with outer_cols[0]:

            st.subheader("Count of Risk types")
            count = df.groupby('Risk type ')['Risk type '].count()

            fig_count = go.Figure(go.Indicator(
                mode="gauge+number",
                value=count.sum(),
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Risks Count"},
                gauge={
                    'shape': 'bullet',
                    'bar': {'color': "black"},
                    'threshold': {
                        'line': {'color': "gray", 'width': 4},
                        'thickness': 0.70,
                        'value': count.sum(), 
                    }, 
                }
            ))
            fig_count.update_layout(
                width=240,
                height=105,
                paper_bgcolor='#f7f7f7',
                margin=dict(t=0, b=0, l=0, r=0),
            )
            st.plotly_chart(fig_count, use_container_width=True)

            inner_cols = st.columns([0.5,0.5])
            with inner_cols[0]:
                opportunity_count = df['Risk type '].value_counts().get('Opportunity', 0)

                fig_opportunity = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=opportunity_count,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Opportunity Count"},
                    gauge={
                            'bar': {'color': "darkgreen"},
                            'threshold': {
                                'line': {'color': "gray", 'width': 4},
                                'thickness': 0.75,
                                'value': opportunity_count, 
                            }, 
                    }
                ))
                fig_opportunity.update_layout(
                    width=200,
                    height=330,
                    paper_bgcolor='#f7f7f7',
                )
                st.plotly_chart(fig_opportunity, use_container_width=True)

            with inner_cols[1]:
                threat_count = df['Risk type '].value_counts().get('Threat', 0)

                fig_threat = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=threat_count,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Threat Count"},
                    gauge={
                            'bar': {'color': "darkred"},
                            'threshold': {
                                'line': {'color': "gray", 'width': 4},
                                'thickness': 0.75,
                                'value': opportunity_count, 
                            }, 
                    }
                ))
                fig_threat.update_layout(
                    width=200,
                    height=330,
                    paper_bgcolor='#f7f7f7',
                )
                st.plotly_chart(fig_threat, use_container_width=True)
                
        with outer_cols[1]:
            st.subheader("Risk situation")
            department_counts = df['Risk situation'].value_counts()
            fig = px.pie(
                names=department_counts.index,
                values=department_counts.values,
                color_discrete_sequence=px.colors.sequential.PuBuGn_r,
            )
            fig.update_layout(
                        width=500,
                        height=450,
                        paper_bgcolor='#f7f7f7',
                        margin=dict(l=20, r=20, t=20, b=20),
                        #title={
                                #'text': "Risk situation",
                                #'x': 0.2,  
                                #'y': 0.95, 
                                #'xanchor': 'center',
                                #'yanchor': 'top',
                                #'font': {'size': 16 }
                        #}
            ) 
            st.plotly_chart(fig)
                                
        # Risk classification,  Risk situation, Deptartment responsible of danger
        with st.container():
            col1, col2, col3 = st.columns(3)
    
            with col1:
                counts = df['Risk classification'].value_counts()
                fig = px.pie(counts, names=counts.index, values=counts,
                    color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.5,
                    title='Risk classification')
                fig.update_traces(textinfo='percent', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                fig.update_layout(
                    width=420,
                    height=350,
                    paper_bgcolor='#f7f7f7',
                    margin=dict(l=20, r=20, t=20, b=10),
                    title={
                        'text': "Risk classification",
                        'x': 0.3,  
                        'y': 0.95,  
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 16 }
                    }
                )
                st.plotly_chart(fig)      

            with col2:
                counts = df['Department responsible'].value_counts()
                fig = px.pie(counts, names=counts.index, values=counts,
                    color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.5,
                    title='Department responsible')
                fig.update_traces(textinfo='percent', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                fig.update_layout(
                    width=420,
                    height=350,
                    paper_bgcolor='#f7f7f7',
                    margin=dict(l=20, r=20, t=20, b=10),
                    title={
                        'text': "Department responsible",
                        'x': 0.3,  
                        'y': 0.95,  
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 16 }
                    }
                )
                st.plotly_chart(fig)      

            with col3:
                counts = df['Source of risk'].value_counts()
                fig = px.pie(counts, names=counts.index, values=counts, template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Blues_r, hole= 0.5,
                                                    title='Source of risk')
                fig.update_traces(textinfo='percent', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                fig.update_layout(
                    width=420,
                    height=350,
                    paper_bgcolor='#f7f7f7',
                    margin=dict(l=20, r=20, t=20, b=10),
                    title={
                        'text': "Department responsible",
                        'x': 0.3,  
                        'y': 0.95,  
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 16 }
                    }
                )
                st.plotly_chart(fig)

        # Reasons
        with st.container():
            col1, col2 = st.columns([15,1])
            with col1:

                reason_counts = df['Reasons'].value_counts().reset_index()
                reason_counts.columns = ['Reason', 'Count']

                fig = px.bar(
                    reason_counts,
                    x='Count',
                    y='Reason', 
                    template="plotly_dark",
                    orientation='h',
                    color_discrete_sequence=px.colors.sequential.Viridis,
                )
                fig.update_layout(
                    width=1300,
                    height=400,
                    paper_bgcolor='#f7f7f7',
                    title={
                        'text': "Reasons",
                        'x': 0.1,  
                        'y': 0.95, 
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {'size': 30 , 'family': 'Arial', }
                    }
                )
                st.plotly_chart(fig)

with tab2:

        st.header("High Risk")
        with st.container():
            col1, col2 = st.columns([1,1]) 
            with col1:
            
                threat_df = df[(df['Risk type '] == 'Threat') & (df['Level'] >= 15) & (df['Level'] <= 25)]
                risk_count = len(threat_df)
                fig_threat = go.Figure()

                fig_threat.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=risk_count,
                    title={'text': "Threat High risk count"},
                    gauge={
                        'bar': {'color': "darkred"},
                        'threshold': {
                            'line': {'color': "gray", 'width': 4},
                            'thickness': 0.75,
                            'value': risk_count,
                        },
                    }
                ))
                fig_threat.update_layout(
                    width=400,
                    height=330,
                )

                st.plotly_chart(fig_threat, use_container_width=True)

            with col2:
            
                opportunity_df = df[(df['Risk type '] == 'Opportunity') & (df['Level'] >= 15) & (df['Level'] <= 25)]
                risk_count = len(opportunity_df)
                fig_opportunity = go.Figure()

                fig_opportunity.add_trace(go.Indicator(
                    mode="gauge+number",
                    value=risk_count,
                    title={'text': "Opportunity High risk count"},
                    gauge={
                        'bar': {'color': "darkgreen"},
                        'threshold': {
                            'line': {'color': "gray", 'width': 4},
                            'thickness': 0.75,
                            'value': risk_count,
                        },
                    }
                ))
                fig_opportunity.update_layout(
                    width=400,
                    height=330,
                )

                st.plotly_chart(fig_opportunity, use_container_width=True)

        tab1, tab2 = st.tabs(["Threat", "Opportunity"])

        with tab1:

            with st.container():    
                
                st.write("The number of high risks based on:")
                col1, col2, col3 = st.columns([1,1,1])

                with col1:    
                    threat_count = df[df['Risk type '] == 'Threat']
                    count_df = threat_count.groupby('Source of risk').size().reset_index(name='Threat Count')
                    fig = px.pie(count_df, names='Source of risk', values='Threat Count', template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                                    title='Source of risk')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=380,
                    height=350,
                    margin=dict(l=0, r=0, t=40, b=0),
                    )
                    st.plotly_chart(fig)

                with col2:
                    threat_count = df[df['Risk type '] == 'Threat']
                    count_df = threat_count.groupby('Department responsible').size().reset_index(name='Threat Count')
                    fig = px.pie(count_df, names='Department responsible', values='Threat Count', template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                                    title='Departement responsible')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=478,
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=0),
                    )
                    st.plotly_chart(fig)
                    

                with col3:
                    threat_count = df[df['Risk type '] == 'Threat']
                    count_df = threat_count.groupby('Risk classification').size().reset_index(name='Threat Count')
                    fig = px.pie(count_df, names='Risk classification', values='Threat Count', template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                                    title='Risk classification')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=380,
                    height=350,
                    margin=dict(l=20, r=20, t=40, b=0),
                    )
                    st.plotly_chart(fig)


            with st.container():

                col1,col2 = st.columns(2)
                with col1:
                    count_df = df[df['Risk type '] == 'Threat'].groupby('Reasons').size().reset_index(name='Threat Count')
                    fig = px.bar(count_df, x='Threat Count', y='Reasons', template="plotly_dark",
                                width=1200, height=500, text='Threat Count', color_discrete_sequence=px.colors.sequential.Viridis)
                    fig.update_traces(textposition='outside')
                    fig.update_layout(yaxis_tickformat=',')
                    fig.update_yaxes(range=[0, count_df['Threat Count'].max() + 1]) 

                    st.plotly_chart(fig)

        with tab2:

            with st.container():    
                st.write("The number of opportunity based on:")
                col1, col2, col3 = st.columns([1,1,1])

                with col1:    
                    threat_count = df[df['Risk type '] == 'Opportunity']
                    count_df = threat_count.groupby('Source of risk').size().reset_index(name='Opp Count')
                    fig = px.pie(count_df, names='Source of risk', values='Opp Count', template="plotly_dark",
                                                                color_discrete_sequence=px.colors.sequential.Viridis,
                                                                title='Source of risk')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=380,
                    height=350,
                    margin=dict(l=0, r=0, t=40, b=0),
                    )
                    st.plotly_chart(fig)

                with col2:
                    threat_count = df[df['Risk type '] == 'Opportunity']
                    count_df = threat_count.groupby('Department responsible').size().reset_index(name='Opp Count')
                    fig = px.pie(count_df, names='Department responsible', values='Opp Count', template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                                    title='Departement responsible')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=470,
                    height=350,
                    margin=dict(l=10, r=10, t=40, b=0),
                    )
                    st.plotly_chart(fig)

                with col3:
                    threat_count = df[df['Risk type '] == 'Opportunity']
                    count_df = threat_count.groupby('Risk classification').size().reset_index(name='Opp Count')
                    fig = px.pie(count_df, names='Risk classification', values='Opp Count', template="plotly_dark",
                                                    color_discrete_sequence=px.colors.sequential.Viridis,
                                                    title='Risk classification')
                    fig.update_traces(textinfo='percent+label', pull=[0.01,0.01,0.01,0.01,0.01,0.01,0.01])
                    fig.update_layout(
                    width=380,
                    height=350,
                    margin=dict(l=0, r=0, t=40, b=0),
                    )
                    st.plotly_chart(fig)

            with st.container():

                col1,col2 = st.columns([20,1])
                with col1:
                    count_df = df[df['Risk type '] == 'Opportunity'].groupby('Reasons').size().reset_index(name='Opportunity Count')
                    fig = px.bar(count_df, x='Opportunity Count', y='Reasons', template="plotly_dark",
                                width=1200, height=500, text='Opportunity Count', color_discrete_sequence=px.colors.sequential.Viridis)
                    fig.update_traces(textposition='outside')
                    fig.update_layout(yaxis_tickformat=',')
                    fig.update_yaxes(range=[0, count_df['Opportunity Count'].max() + 1]) 

                    st.plotly_chart(fig)

with tab3:
        st.title("Response plans")

        tab1, tab2 = st.tabs(["Threat", "Opportunity"])
        with tab1:
                with st.container():
                    col1 , col2, col3 = st.columns([1 , 1 , 1])
                    with col1:

                        count_df = df[df['Risk type '] == 'Threat'].groupby('Response plan').size().reset_index(name='Threat Count')
                        fig = px.bar(count_df, x='Response plan', y='Threat Count', color='Response plan', template="plotly_dark",
                                    width=370, height=600, text='Threat Count', color_discrete_sequence=px.colors.sequential.Reds_r)
                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Threat Count'].max() + 1]) 

                        st.plotly_chart(fig)

                    with col2:

                        count_df = df[df['Risk type '] == 'Threat'].groupby('Response plan officer').size().reset_index(name='Threat Count')
                        fig = px.bar(count_df, x='Response plan officer', y='Threat Count', color='Response plan officer', template="plotly_dark",
                                    width=370, height=600, text='Threat Count', color_discrete_sequence=px.colors.sequential.Reds_r)
                        
                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Threat Count'].max() + 1]) 

                        st.plotly_chart(fig)

                    with col3:

                        count_df = df[df['Risk type '] == 'Threat'].groupby('Procedure type').size().reset_index(name='Threat Count')
                        fig = px.bar(count_df, x='Procedure type', y='Threat Count', color='Procedure type', template="plotly_dark",
                                    width=370, height=600, text='Threat Count', color_discrete_sequence=px.colors.sequential.Reds_r)
                        
                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Threat Count'].max() + 1]) 

                        st.plotly_chart(fig)

        
        with tab2:
                with st.container():
                    col1, col2, col3 = st.columns([1,1,1])

                    with col1:

                        count_df = df[df['Risk type '] == 'Opportunity'].groupby('Response plan').size().reset_index(name='Opportunity Count')
                        fig = px.bar(count_df, x= 'Response plan', y='Opportunity Count', color='Response plan', template="plotly_dark",
                                    width=370, height=600, text='Opportunity Count', color_discrete_sequence=px.colors.sequential.Greens_r)

                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Opportunity Count'].max() + 1]) 

                        st.plotly_chart(fig)
                    
                    with col2:
                        count_df = df[df['Risk type '] == 'Opportunity'].groupby('Response plan officer').size().reset_index(name='Opportunity Count')
                        fig = px.bar(count_df, x='Response plan officer' , y='Opportunity Count', color='Response plan officer', template="plotly_dark",
                                    width=370, height=600, text='Opportunity Count', color_discrete_sequence=px.colors.sequential.Greens_r)
                                    
                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Opportunity Count'].max() + 1]) 
                        st.plotly_chart(fig)
            
                    with col3:

                        count_df = df[df['Risk type '] == 'Opportunity'].groupby('Procedure type').size().reset_index(name='Opportunity Count')
                        fig = px.bar(count_df, x= 'Procedure type', y='Opportunity Count', color='Procedure type', template="plotly_dark",
                                    width=370, height=600, text='Opportunity Count', color_discrete_sequence=px.colors.sequential.Greens_r)
                                    
                        fig.update_traces(textposition='outside')
                        fig.update_layout(yaxis_tickformat=',')
                        fig.update_yaxes(range=[0, count_df['Opportunity Count'].max() + 1]) 

                        st.plotly_chart(fig)                