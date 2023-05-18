import pandas as pd
import plotly.express as px
import streamlit as st
import os


# Get the directory path of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the Excel file
file_path = os.path.join(script_dir, 'supermarkt_sales.xlsx')


st.set_page_config(page_title = "Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout = "wide")

@st.cache_data
def get_data():

    df = pd.read_excel(io = file_path,
                   engine= 'openpyxl',
                   sheet_name= 'Sales',
                   skiprows = 3,
                   usecols = 'B:R',
                   nrows = 10000,
            
                   )
    df['Hour'] = pd.to_datetime(df['Time'], format= "%H:%M:%S").dt.hour
    return df


df = get_data()



#   side bar


st.sidebar.header('Please Filter Here:')
city = st.sidebar.multiselect(
    "Select the City:",
    options= df["City"].unique(),
    default= None
)


customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options= df["Customer_type"].unique(),
    default= None
)


gender = st.sidebar.multiselect(
    "Select the Gender:",
    options= df["Gender"].unique(),
    default= None
)




# df_selection  = df.query(

#     "City == @city & Customer_type == @customer_type & Gender == @gender"
# )



city = df["City"].unique() if city == [] else city
customer_type = df["Customer_type"].unique() if customer_type == [] else customer_type
gender = df["Gender"].unique() if gender == [] else gender

df_selection = df[
    df.City.isin(city) &
    df.Customer_type.isin(customer_type) &
    df.Gender.isin(gender)
]


st.dataframe(df_selection)

# ----- Main Page -----

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


# Top KIPs

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(average_rating)
average_sales_by_transaction = round(df_selection["Total"].mean(),2)


# Streamlit Columns
left_column, middle_column, right_column =  st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sales_by_transaction}")

st.markdown("---")

# # Sales by product line
sales_by_product_line = df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")

fig_product_sales = px.bar(

    sales_by_product_line,
    x = 'Total',
    y = sales_by_product_line.index,
    orientation = "h",
    title = "<b>Sales By Product Line<b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_product_line),
    template = "plotly_white"
)

# st.plotly_chart(fig_product_sales)

# Sales by hours
sales_by_hour = df_selection.groupby(by=["Hour"]).sum()[["Total"]]

fig_hourly_sales = px.bar(

    sales_by_hour,
    x = sales_by_hour.index,
    y = "Total",
    title = "<b>Sales By Hour<b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_hour),
    template = "plotly_white"
)
fig_hourly_sales.update_layout(

    xaxis= dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis= dict(showgrid=False)
)
st.plotly_chart(fig_hourly_sales)

left_column,right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales,use_container_width=True)
right_column.plotly_chart(fig_hourly_sales,use_container_width=True)

# Hide unwanted elements
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>      
    
                """
st.markdown(hide_st_style, unsafe_allow_html=True)