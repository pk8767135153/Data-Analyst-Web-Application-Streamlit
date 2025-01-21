import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st

st.set_page_config(page_title="Data Analysis Project", page_icon="📊", layout="wide", initial_sidebar_state="expanded", menu_items=None)

# Back Ground Color
page_bg_img = """
<style> 
[data-testid="stAppViewContainer"]{background-color:#232121}
</style>"""
st.markdown(page_bg_img,unsafe_allow_html=True)
st.sidebar.title(":rainbow[Data Analyst Web Application]")

 
st.sidebar.markdown(":red[**Pravinsingh Korekar**]")
st.sidebar.markdown("*Contact Number : 8767135153*")
st.sidebar.markdown("*pravinkorekar6@gmail.com*")

 


# Main Section 
st.sidebar.write("Project : Streamlit Data Analysis Web Application")

# Primary Section 
user_name = st.sidebar.text_input(f":orange[**Enter the Name Here**]")
 
if st.sidebar.button(f":red[**Submit**]") == True:
     st.title(f"❤️!!! :red[ Welcome {user_name}] !!!❤️")
st.sidebar.markdown(f"-----------")
    
# 2ed Section 
# Load Data Set in the web app
data = pd.DataFrame()

def load_data():
    with st.expander("Load Data"):
        st.info("Upload The Dataset")
        file = st.file_uploader(f"*Drop The File Here*",type=['csv','xlsx'])


# Read Data Function 
        if file!=None:
            # If Display Process bar when file is not null
            st.progress(100,text="")
            if file.name.endswith("csv"):
                # read csv file
                data = pd.read_csv(file)
                st.success("Data is uploaded")
            else :
                # Read excel file
                data = pd.read_excel(file)
                st.success("Data is uploaded")
        else : 
            # If data is not Uploaded display warning
            st.warning("Data is Not Uploaded")
        return data

data = load_data()
    
    
# Main Section 
st.subheader("Business Analytics Dashboard")

# Display Data Function 
def table():
    with st.expander("My Database Table"):
        # Select the Feature 
        showdata = st.multiselect("Filter Dataset",data.columns)
        # To select how many data point you want to see
        no_of_datapoint= st.slider(f"*Number Of Data Points*",1,data.shape[0])
        # display original data in the from of dataframe 
        st.dataframe(data[showdata].head(no_of_datapoint),use_container_width=True)
table()

# make the branch/ subsession 
tab1, tab2, tab3, tab4, tab5 = st.tabs(["**Summary**","**Visualization**","**Two Features Visualization**","**Unique Value**","**Statistics**"])
tab_col_1,tab_col_2,tab_col_3,tab_col_4,tab_col_5 = st.columns(5)
# style of each tab
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {
gap: 2px;
}
.stTabs [data-baseweb="tab"] {
height: 50px;
width : 3000px;

white-space: pre-wrap;
background-color:#EC2BDC;
border-radius: 4px 20px 30px 30px;
gap: 1px;
padding-top: 10px;
padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
background-color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)


# start summary subsession
def summary(): 
    # Object features
    obj_feature = [i for i in data.columns if data[i].dtype =="O"]
    # floating Features 
    float_feature =  [i for i in data.columns if data[i].dtype =="float64"]
    # Intger Features
    int_feature =  [i for i in data.columns if data[i].dtype =="int64"]
    
    # import style_metric_cards
    from streamlit_extras.metric_cards import style_metric_cards
    
    # Make the 3 column which look better
    col1, col2, col3 = st.columns(3)
    col4,col5, col6 = st.columns(3)
    
    # Display total Data Point
    col1.metric("***Total Data Point***",value=data.shape[0],delta="All")
    
    # Display Total Features 
    col2.metric("***All Features***",value=data.shape[1], delta="Total Columns")
    
    # Display Duplicate Data Point
    col3.metric("***DUPLICAT DATA POINT***",value=data.duplicated().sum(),delta="Total Repeted Row")

    
    # Display Total Object Features
    col4.metric("***Total Object Features***",value=len(obj_feature),delta="Number Of Object Features")
    
    # Display Total Integer Features
    col5.metric("***Total Integer Features***",value=len(int_feature),delta="Number Of Integer Features")
    
    # Display Total Floating Features 
    col6.metric("***Total Float Features***",value=len(float_feature),delta="Number Of Float Features")
    
    # Gives the Style of each metric_cards
    style_metric_cards(background_color="#071021",border_color="#1f66bd")
    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Display Null Value inside the dataset
    with st.expander("**How Many Null Value Conation Data Set**"):
        no_of_features = st.slider("No Of Features",1,data.shape[1])
        st.dataframe(data.isnull().sum().head(no_of_features))
        pass
    
    # Display Data Types Of Each Features
    with st.expander("***To Data types Each Features***"):
        no_of_features = st.slider("No Of features",1,data.shape[1])
        st.dataframe(data.dtypes.head(no_of_features))
        
# Working with tab1
with tab_col_1:
    with tab1:
        summary()
 


def visualization():
    
    st.title('Select The Features') 
    # Options for the selectbox 
    options = [i for i in data.columns] 
    # Prompt the user to select an option 
    feature = st.selectbox("",options,)
        # Display the selected option 
    st.info(f'You selected: {feature}')

    if feature != None:
         
        # Display Plot
        with st.expander("Show The Plot"):
            col1, col2 = st.columns(2)
            with col1:
                
                count = data[feature].value_counts()
                fig,ax = plt.subplots(figsize=(3,3))
                ax.pie(count,labels=count.index,autopct='%1.2f%%',startangle=90)
                st.pyplot(fig)
                
                
                pass
            with col2:
                if data[feature].dtype == "object":
                    # Value Count Plot
                    value_count = data[feature].value_counts().reset_index()
                    value_count.columns = ["Category","Count"]
                    if value_count.shape[0]<15:
                        fig = px.histogram(value_count,x="Category",y="Count",color="Category",height=400,width=500)
                        st.write(fig)
        
                
                elif data[feature].dtype == "int64" or data[feature] =="float64":
                    fig,ax = plt.subplots()
                    fig = sns.displot(data = data[feature],kind="kde",ax=ax )
                    ax.set_title("Distribution")
                    st.pyplot(fig)
                else: 
                    st.write(data[feature].dtypes)
                    st.warning("So Sorry I Am Features")
    else:
        st.warning("Data Not Uploaded!")
    
with tab_col_2:            
    with tab2:
        visualization()

def Two_features_visualization():
    with st.expander("Select Features"):
        # Options for the selectbox 
        options = [i for i in data.columns] 
        col1,col2 = st.columns(2)         
        with col1:
            st.info("Select First Features")
            feature_1 = st.selectbox(" ",options)
            st.success(f"{feature_1} : {data[feature_1].dtypes}")
        with col2:
            st.info("Select Second Features")
            feature_2 = st.selectbox("  ",options)
            st.success(f"{feature_2} : {data[feature_2].dtypes}")
       
    with st.expander("Show Figure"):
        col1,col2,col3 = st.columns(3)
        if (data[feature_1].dtypes == "float64")or(data[feature_1].dtypes == "int64")and ((data[feature_2].dtypes == "float64")or(data[feature_2].dtypes == "int64")):
            with col2:
                fig,ax = plt.subplots(figsize=(7,5))
                ax = plt.scatter(x=data[feature_1], y=data[feature_2],color="skyblue")
                plt.title(f"{feature_1} vs {feature_2}")
                plt.xlabel(feature_1)
                plt.ylabel(feature_2)
                st.write(fig)
        elif (data[feature_1].dtypes == "object" and (data[feature_2].dtypes == "float64"or data[feature_2].dtypes == "int64")):
            with col2:
                fig,ax = plt.subplots(figsize=(7,5))
                ax = plt.bar(data[feature_1], data[feature_2],color="skyblue")
                plt.title(f"{feature_1} vs {feature_2}")
                plt.xlabel(feature_1)
                plt.ylabel(feature_2)
                st.write(fig)
        elif (data[feature_2].dtypes == "object" and (data[feature_1].dtypes == "float64"or data[feature_1].dtypes == "int64")):
            with col2:
                fig,ax = plt.subplots(figsize=(7,5))
                ax = plt.bar(data[feature_2],data[feature_1],color="skyblue")
                plt.title(f"{feature_1} vs {feature_2}")
                plt.xlabel(feature_1)
                plt.ylabel(feature_2)
                st.write(fig)
        else :
            st.warning(f"Sorry! Data Types Of {feature_1} and {feature_2} Does Not Support")
        pass
        
with tab_col_3:
    with tab3:
        Two_features_visualization()
        
def unique_value_of_each_feature():
    l = [i for i in data.columns if data[i].dtypes != "object"]
    features_multi = st.multiselect("Select Options :",options=l,default=l[0:3])
    for i in features_multi:
        st.write(f"{i} : {data[i].unique()}")
    pass

with tab_col_4:
    with tab4:
        unique_value_of_each_feature()
    
def describe_fun():
    # sns.heatmap(data.corr())
    st.write(data.describe(),object=True)
    pass

with tab_col_5:
    with tab5:
        describe_fun()
 
