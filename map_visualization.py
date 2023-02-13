from os import stat
import pandas as pd
import streamlit as st
import pydeck as pdk
import numpy as np

st.set_page_config(layout="centered")

tab1, tab2 = st.tabs(["Loan Detail View", "Loan Summary View"])
SUMMRY_FILE = 'summary_view.csv'
COLS = ["loan_amount", "lon", "lat", "pin_code","CD",	"CSR",	"EV",	"K12",	"Vocational",
        "ogl_status", "state","color_map", "loan_sqrt","coordinates","institute_count","protected","non_protected",
        "city", "deliquency(%)", "deliquency_amount", "sub_distname", "deliquency_in_decimal"]

table_cols = ["state", "city","deliquency_amount", "loan_amount", "sub_distname", "ogl_status",\
                        "institute_count","protected","non_protected","CD",	"CSR",	"EV",	"K12",	"Vocational"]

map_plot_params = {
        'auto_highlight':True,
        'pickable':True,
        'opacity':0.3,
        'radius_scale':6,
        'radius_min_pixels':2.5,
        'get_position':'coordinates',
        'get_radius': "loan_sqrt",
        'get_fill_color':"color_map",
        'get_line_color':[0, 0, 0]
        }

map_dflt_params = {
    'latitude':19.7515, 
    'longitude':75.7139, 
    'zoom':3.6, 
    'bearing':1, 
    'pitch':25
}

def clean_data(df):
    return (
                df.astype({'lon':'float64', 'lat':'float64'})\
                .assign(coordinates= lambda x : tuple(zip(x.lon, x.lat)),\
                        loan_sqrt=lambda val : np.sqrt(val.loan_amount),\
                        color_map=df.apply(lambda val:[235,64,52] if val.deliquency_in_decimal > 0.15 \
                                            else [52, 235, 82], axis=1))\
                .pipe(lambda ds: ds[COLS]).copy()
        )

class ListGenerator:
    def __init__(self):
        self.state_list = ''
        self.city_list = ''
        self.ogl_status = ''
    
    @classmethod
    def from_df(cls, df):
        cls.state_list = ['All']+sorted(df['state'].unique())
        cls.city_list = ['All']+sorted(df[df['state'].isin(cls.state_list)]["sub_distname"].unique())
        cls.ogl_status = ['All']+sorted(df['ogl_status'].unique())
        return cls
    
    
def create_filter(df, state_val, city_val, deliq_vals, ogl_val, deliq_prcnt_vals):
    return (
        
            (df["state"].isin(state_val)) & 
            (df["city"].isin(city_val)) &
            (df["ogl_status"].isin(ogl_val)) & 
            (df["deliquency_amount"] > float(deliq_vals[0])) &
            (df["deliquency_amount"] < float(deliq_vals[1])) &
            (df["deliquency_in_decimal"] > float(deliq_prcnt_vals[0]/100)) &
            (df["deliquency_in_decimal"] < float(deliq_prcnt_vals[1]/100))
            
        )
    

def get_summary_view(df):
    ui_params = ListGenerator.from_df(df)
    
    with st.container():
        with st.sidebar:
            state_val = st.multiselect(
                'Select State',
                ui_params.state_list,
                ['All'])
            # ui_params.state_list = state_val

            if 'All' in state_val:
                state_val = ui_params.state_list

            ogl_val = st.multiselect(
                'Select OGL Status',
                ui_params.ogl_status,
                ['All'])
                    
            if 'All' in ogl_val:
                ogl_val = ui_params.ogl_status


            ui_params.city_list = ['All']+sorted(df[df['state'].isin(state_val)]["sub_distname"].unique())
            city_val = st.multiselect(
                'Select City',
                ui_params.city_list,
                ['All' ])
                
            if 'All' in city_val:
                city_val = ui_params.city_list
                

            deliq_vals = st.slider(
                'Select a Deliquency Amount Range',
                0, 500000, (50000, 200000), step=50000)
            
            deliq_prcnt_vals = st.slider(
                'Select a Deliquency Percent Range (%)',
                1, 100, (1, 10), step=1)
            
            # print(deliq_vals)
                    
        filter = create_filter(df, state_val, city_val, deliq_vals, ogl_val, deliq_prcnt_vals)
                # print(filter)

        # print(city_val, state_val)
        
        legend_colors = ['red','green'];
        legend_titles = ['Deliquency percent > 15%', 'Deliquency percent < 15%'];

        st.write('<h4 style="text-align:center; text-decoration: underline;">Deliquency Spread: OGL Analysis</h4>' ,unsafe_allow_html=True)          
        for color, label in zip(legend_colors, legend_titles):
            html_str =f'<div style="display:flex;justify-content:space-between;align-items:baseline;width:35%">\
                            <div style="display:inline-block">{label}</a></div>\
                            <div style="width: 10px; height:10px; background:{color}; border-radius: 50%; display:inline-block"></div>\
                        </div>'
            
            st.write(html_str, unsafe_allow_html=True)
          
        if 'All' in state_val:
            df = df.loc[filter]
        
            st.write(plot_map(df))
            st.dataframe(df[table_cols])
            
        else:
            df = df.loc[filter]

            st.write(plot_map(df))
            st.dataframe(df[table_cols])
       
 
def plot_map(df):
    layer = pdk.Layer(
    "ScatterplotLayer",
    df,
    **map_plot_params
    )

    view_state = pdk.ViewState(**map_dflt_params)
    r = pdk.Deck(layers=[layer], initial_view_state=view_state, \
    tooltip={"text": "Pincode: {pin_code}\nLoan Amount: {loan_amount}\nDeliquency: {deliquency(%)}\nDeliquency Amount: {deliquency_amount}\n\
        City: {city}\nSub-District: {sub_distname}\n Institute Count: {institute_count}\n \
            Protected Count: {protected}\nNon-Protected Count:{non_protected}\
            \nCD-Segment Count: {CD}\nCSR-Segment: {CSR}\n \
            EV-Segment Count: {EV}\nK12-Segment Count: {K12}\nVocational-Segment Count: {Vocational}"})

    return r

raw_data = pd.read_csv(SUMMRY_FILE)
data = clean_data(raw_data)
get_summary_view(data)
