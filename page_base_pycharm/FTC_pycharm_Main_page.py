# Libraries

from streamlit_folium import folium_static
from folium.map       import LayerControl
from PIL              import Image
from folium.plugins   import MarkerCluster

import folium
import base64
import streamlit            as st
import pandas               as pd
import plotly.graph_objects as go

# Functions

def get_popup_content( row ):
    # Define a function to generate popup content
    return f"""<b>{row['restaurant_name']}</b><br>
               Price: {row['average_cost_for_two']} {row['currency']}<br>
               Type: {row['cuisines']}<br>
               Aggregate Rating: {row['aggregate_rating']}/5.0"""

#--------------------------#---------------------------#----------------------------------------#------------

# Read the Treated CSV

st.set_page_config( page_title='Home', page_icon='👽' )

df = pd.read_csv( "C:/Users/gabre/DS IN PROGRESS/DS_2023/Ciclo_Basico/FTC Analisando dados com Python"
                  "/FTC_student_project/dataset/zomato_treated_13-02-2024.csv" )

# Because of the modeling and filtering take so long I decided to add the CSV filtered

df1 = df.copy()

# Company's View

# =============================
# Sidebar
# =============================

st.header( "Zomato's" )
st.subheader( 'Find out your next favorite Restaurant!' )
st.markdown( """___""" )

image_path = 'restaurant_page.jpg'

image = Image.open( image_path )
st.sidebar.image( image, width=250, use_column_width=True )

st.sidebar.markdown( '# Zomato Restaurants' )
st.sidebar.markdown( '## Your next meal is here!!' )

st.sidebar.markdown( """___""" )

st.sidebar.markdown( '### Treated Data' )

# Add a download button below the markdown sections

if st.sidebar.button( 'Download Treated Data' ):

    # Trigger file download when the button is clicked
    csv = df1.to_csv( index=False )
    b64 = base64.b64encode( csv.encode() ).decode()  # Convert DataFrame to base64 encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="treated_data.csv">Zomato CSV</a>'
    st.sidebar.markdown( href, unsafe_allow_html=True )

st.sidebar.markdown( """___""" )

image_path = 'restaurant_home.jpg'
image = Image.open( image_path )
st.sidebar.image( image, width=250, use_column_width=True )

st.sidebar.markdown( "Powered by Gabri7sc")
st.sidebar.markdown( "©Comunidade DS")

# =============================
# Layout Streamlit
# =============================

# Create tabs to insert pages inside the home page

tab1, tab2, tab3 = st.tabs( ['World Map Restaurants', "Countries' View", 'Most Voted Countries'] )

with tab1:
    with st.container():

        st.title( 'Get to Know our portfolio of clients' )

        col1, col2, col3, col4, col5 = st.columns( [1, 1, 1, 2, 1] )  # Adjust column widths

        with col1:
            registered_restaurants = df1["restaurant_id"].nunique()
            col1.metric( 'Restaurants', registered_restaurants )

        with col2:
            countries = df1["country_code"].nunique()
            col2.metric( 'Countries', countries )

        with col3:
            cities = df1["city"].nunique()
            col3.metric( 'Cities', cities )

        with col4:
            votes = df1["votes"].sum()
            col4.metric('Reviews', f'{votes:,}')

        with col5:
            cuisines = df1["cuisines"].nunique()
            col5.metric( 'Cuisines', cuisines )

    with st.container():

        # Create a map with a specific zoom level
        map = folium.Map( location=[0, 0], zoom_start=1 )

        # Create a MarkerCluster object
        marker_cluster = MarkerCluster().add_to( map )

        # Create a LayerControl object
        layer_control = LayerControl().add_to( map )

        # Iterate through each restaurant
        for index, row in df1.iterrows():
            # Determine the popup content
            popup_content = get_popup_content( row )

            # Create a marker with detailed popup content
            folium.Marker( location=[row['latitude'], row['longitude']],
                           popup=popup_content ).add_to( marker_cluster )
        folium_static( map, width=800, height=500 )

with tab2:
    with st.container():

        q11 = ( df1[['country_code', 'dollar_usd_value']].groupby( 'country_code' )
                .mean().sort_values( 'dollar_usd_value', ascending=True ).reset_index() )
        q11 = q11.round( 2 )

        fig = go.Figure( data=[go.Bar(
            x=q11['country_code'],
            y=q11['dollar_usd_value'],
            text=q11['dollar_usd_value'],  # Add total as text inside bars
            textposition='outside',  # Position text inside bars
            marker=dict( color='blue', line=dict( color='blue', width=1.5 ) ),
            opacity=0.6 )] )
        fig.update_layout( title='Average Price for two people in USD $ in each country',
                           xaxis_title='Country Name',
                           yaxis_title='Average Price', height=600, title_font=dict( size=20 ) )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():

        q1 = ( df1[['country_code', 'city']].groupby( 'country_code' )
               .nunique().sort_values( 'city', ascending=False ).reset_index() )
        fig = go.Figure( data=[go.Bar(
            x=q1['country_code'],
            y=q1['city'],
            text=q1['city'],  # Add total as text inside bars
            textposition='auto',  # Position text inside bars
            marker=dict( color='darkblue', line=dict( color='darkblue', width=1.5 ) ),
            opacity=0.6 )] )

        fig.update_layout( title='Number of Cities by Country', xaxis_title='Country Name',
                           yaxis_title='Number of Cities', title_font=dict( size=20 ) )
        st.plotly_chart( fig, use_container_width=True )

        st.markdown( """___""")

    with st.container():

        q2 = ( df1[['country_code', 'restaurant_id']].groupby( 'country_code' )
               .count().sort_values( 'restaurant_id', ascending=False ).reset_index() )

        fig = go.Figure( data=[go.Bar(
            x=q2['country_code'],
            y=q2['restaurant_id'],
            text=q2['restaurant_id'],  # Add total as text inside bars
            textposition='auto',  # Position text inside bars
            marker=dict( color='darkblue', line=dict(color='darkblue', width=1.5 ) ),
            opacity=0.6 )] )

        fig.update_layout( title='Number of Restaurants by Country', xaxis_title='Country Name',
                           yaxis_title='Number of Restaurants', title_font=dict( size=20 ) )
        st.plotly_chart( fig, use_container_width=True )

with tab3:
    with st.container():

        q5 = ( df1[['country_code', 'votes']].groupby( 'country_code' )
               .sum().sort_values( 'votes', ascending=False ).reset_index() )

        fig = go.Figure( data=[go.Bar(
            x=q5['country_code'],
            y=q5['votes'],
            text=q5['votes'],  # Add total as text inside bars
            textposition='outside',  # Position text inside bars
            marker=dict( color='blue', line=dict( color='blue', width=1.5 ) ),
            opacity=0.6 )] )

        fig.update_layout( title='Number of Reviews by Country', xaxis_title='Country Name',
                           yaxis_title='Number of Votes', height=600, title_font=dict( size=20 ) )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():

        q9 = ( df1[['country_code', 'aggregate_rating']].groupby( 'country_code' )
            .mean().sort_values( 'aggregate_rating', ascending=False ).reset_index() )
        q9 = q9.round(2)

        fig = go.Figure (data=[go.Bar(
            x=q9['country_code'],
            y=q9['aggregate_rating'],
            text=q9['aggregate_rating'],  # Add total as text inside bars
            textposition='inside',  # Position text inside bars
            marker=dict( color='darkblue', line=dict( color='darkblue', width=1.5 ) ),
            opacity=0.6 )] )

        fig.update_layout( title='Best Reviewed Countries', xaxis_title='Country Name',
                           yaxis_title='Average Review by Country', title_font=dict( size=20 ) )
        fig.update_traces( textfont=dict( size=12 ) )
        st.plotly_chart( fig, use_container_width=True )
