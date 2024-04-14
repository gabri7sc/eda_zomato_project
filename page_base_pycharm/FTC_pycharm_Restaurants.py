# Libraries

from PIL              import Image
from folium.plugins   import MarkerCluster
from streamlit_folium import folium_static
from folium.map       import LayerControl

import folium
import base64
import streamlit            as st
import pandas               as pd
import plotly.express       as px
import plotly.graph_objects as go

# Functions

def get_popup_content( row ):
    return f"""<b>{row['restaurant_name']}</b><br>
               Price: {row['average_cost_for_two']} {row['currency']}<br>
               Type: {row['cuisines']}<br>
               Aggregate Rating: {row['aggregate_rating']}/5.0"""

# Read the Treated CSV

df = pd.read_csv( "C:/Users/gabre/DS IN PROGRESS/DS_2023/Ciclo_Basico/FTC Analisando dados com Python"
                  "/FTC_student_project/dataset/zomato_treated_13-02-2024.csv" )

# Because of the modeling and filtering take so long I decided to add the CSV filtered

df1 = df.copy()

# Restaurants and Cuisines' View

# =============================
# Sidebar
# =============================

st.header( "Zomato's" )
st.subheader( 'Find out your next favorite Restaurant!' )
st.markdown( """___""" )

image_path = 'C:/Users/gabre/DS IN PROGRESS/DS_2023/Ciclo_Basico/FTC Analisando dados com Python' \
             '/FTC_student_project/restaurant_page.jpg'
image = Image.open( image_path )

st.sidebar.image( image, width=250, use_column_width=True )

st.sidebar.markdown( '# Zomato Restaurants' )
st.sidebar.markdown( '## Your next meal is here!!' )

st.sidebar.markdown( """___""" )

# Filters

st.sidebar.markdown( '## Choose the countries you want to see' )

country_options = st.sidebar.multiselect( 'Select Countries',
                                          df1['country_code'].unique(),
                                          default=['Philippines', 'Brazil', 'Australia', 'United States of America',
                                          'Canada', 'Singapure', 'United Arab Emirates', 'England', 'Qatar'] )

st.sidebar.markdown( '## Choose the cuisines you want to see' )

cuisines_options = st.sidebar.multiselect( 'Select Cuisines',
                                    df1['cuisines'].unique(),
                                    default=['American', 'Indian', 'Italian', 'Cafe', 'Chinese',
                                             'French', 'Mexican', 'Brazilian'] )

min_price, max_price = st.sidebar.slider( "Select Price Range (USD)", df1['dollar_usd_value'].min(),
                                         df1['dollar_usd_value'].max(), ( 0.0, df1['dollar_usd_value'].max() ) )

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

image_path = 'C:/Users/gabre/DS IN PROGRESS/DS_2023/Ciclo_Basico/FTC Analisando dados com Python' \
             '/FTC_student_project/restaurant_home.jpg'
image = Image.open( image_path )
st.sidebar.image( image, width=250, use_column_width=True )

st.sidebar.markdown( "Powered by Gabri7sc" )
st.sidebar.markdown( "©Comunidade DS" )

# Country filter

selected_countries = df1['country_code'].isin( country_options )
df1 = df1.loc[selected_countries, :]

# Cuisine filter

selected_cuisines = df1['cuisines'].isin( cuisines_options )
df1 = df1.loc[selected_cuisines, :]

# Price Filter

df1 = df1[( df1['dollar_usd_value'] >= min_price ) & ( df1['dollar_usd_value'] <= max_price )]

# =============================
# Layout Streamlit
# =============================

tab1, tab2, tab3 = st.tabs( ["Restaurants' View", "Cuisine' View", 'Choose your Restaurant'] )

with tab1:
    with st.container():

        # The Chart Headline
        st.header( "Cuisines and Restaurants' View" )
        st.markdown( "#### Check out the Restaurants and the Cuisines Variety" )

        col1, col2, col3, col4, col5 = st.columns( 5 )

        with col1:

            q20 = ( df1[['restaurant_id', 'restaurant_name', 'votes']].groupby( ['restaurant_id'] )
                    .sum().sort_values( 'votes', ascending=False ).reset_index() )

            col1.metric( "Most Reviewed ", q20['votes'].max() )

        with col2:

            q21 = df1[['restaurant_name', 'restaurant_id', 'aggregate_rating']].groupby( 'restaurant_name' ).agg(
                {'restaurant_id': 'first', 'aggregate_rating': 'mean'} )
            q21 = q21.sort_values( by=['aggregate_rating', 'restaurant_id'], ascending=[False, True] ).reset_index()

            col2.metric( f"Best Evaluation", f"{q21.loc[0, 'aggregate_rating']}/5.0" )

        with col3:

            q21 = df1.loc[df1['votes'] >= 1, :][['restaurant_name', 'restaurant_id', 'aggregate_rating']]

            col3.metric( f"Worst Evaluation", f"{q21['aggregate_rating'].min()}/5.0" )

        with col4:

            q22 = df1[['restaurant_name', 'restaurant_id', 'dollar_usd_value']].sort_values( 'dollar_usd_value',
                                                                                              ascending=False )
            col4.metric( "Most Expensive (USD)", f"${q22['dollar_usd_value'].max()}" )

        with col5:

            q22 = df1.loc[df1['dollar_usd_value'] > 0, :]
            q22 = q22[['restaurant_name', 'restaurant_id', 'dollar_usd_value']].sort_values( 'dollar_usd_value',
                                                                                              ascending=False )

            col5.metric( "Cheapest (USD)", f"${q22['dollar_usd_value'].min()}" )

    with st.container():

        st.subheader( "The Best 10 Restaurants" )

        aux = ( df1[['restaurant_id', 'restaurant_name', 'country_code', 'city', 'cuisines', 'dollar_usd_value',
                     'aggregate_rating', 'votes']]
                .sort_values( by=['aggregate_rating', 'votes'], ascending=[False, False] ).reset_index( drop=True ) )
        aux = aux.head( 10 )

        st.dataframe( aux, use_container_width=True, hide_index=True )

    with st.container():

        col1, col2 = st.columns( 2 )

        with col1:

            st.subheader( 'Top Best Restaurants' )

            q21_best = df1[['restaurant_name', 'restaurant_id', 'aggregate_rating']].groupby( 'restaurant_name' ).agg(
                {'restaurant_id': 'first', 'aggregate_rating': 'mean'} )
            q21_best = q21_best.sort_values( by=['aggregate_rating', 'restaurant_id'],
                                             ascending=[False, True] ).reset_index()
            q21_best.columns = ['restaurant_name', 'restaurant_id', 'agg_rating']

            st.dataframe( q21_best[['restaurant_name', 'agg_rating']], use_container_width=True )

        with col2:

            st.subheader( 'Top Worst Restaurants' )

            q21_worst = ( df1.loc[df1['votes'] >= 1, :][['restaurant_name', 'restaurant_id', 'aggregate_rating']]
            .groupby( 'restaurant_name' ).agg(
                {'restaurant_id': 'first', 'aggregate_rating': 'mean'} ) )
            q21_worst = q21_worst.sort_values( by=['aggregate_rating', 'restaurant_id'],
                                               ascending=[True, True] ).reset_index()
            q21_worst.columns = ['restaurant_name', 'restaurant_id', 'agg_rating']

            st.dataframe( q21_worst[['restaurant_name', 'agg_rating']], use_container_width=True )

    st.markdown( """___""" )

    with st.container():

        q20 = ( df1[['restaurant_id', 'restaurant_name', 'city', 'votes']].groupby( ['restaurant_id', 'city'] )
            .sum().sort_values( 'votes', ascending=False ).reset_index() )
        q20 = q20.head( 10 )

        fig = go.Figure( data=[go.Bar(
            x=q20['restaurant_name'],
            y=q20['votes'],
            marker=dict( color='yellow', line=dict( color='yellow', width=1.5 ) ),
            opacity=0.6 )] )

        fig.update_layout( title="Top 10 most Visited Restaurants by their Reviews", xaxis_title='Restaurant',
                           yaxis_title='Visits', title_font=dict( size=20 ), height=600 )
        st.plotly_chart( fig, use_container_width=True )

    with st.container():

        q20 = ( df1[['restaurant_name', 'votes']].groupby( ['restaurant_name'] )
            .sum().sort_values( 'votes', ascending=False ).reset_index() )
        q20 = q20.head( 10 )

        fig = go.Figure( data=[go.Bar(
            x=q20['restaurant_name'],
            y=q20['votes'],
            text=q20['votes'],  # Add total as text inside bars
            textposition='auto',  # Position text inside bars
            marker=dict( color='yellow', line=dict( color='yellow', width=1.5 ) ),
            opacity=0.6)] )

        fig.update_layout( title="Top 10 most Visited Restaurant Franchise by their Reviews",
                           xaxis_title='Franchise',
                           yaxis_title='Visits', title_font=dict( size=20 ) )
        st.plotly_chart( fig, use_container_width=True )

with tab2:
    with st.container():

        st.header( "Cuisines and Restaurants' View" )

        st.markdown( '### The 20 Most Common Cuisines Distribution' )

        aux = df1[['restaurant_id', 'cuisines']].groupby( 'cuisines' ).count().reset_index()
        aux = aux[( aux['cuisines'] != 'NaN' )]
        aux['percentage_cuisine'] = aux['restaurant_id'] / aux['restaurant_id'].sum()
        aux = aux.sort_values( 'percentage_cuisine', ascending=False ).head( 20 )

        fig = px.pie( aux, values='percentage_cuisine', names='cuisines')
        st.plotly_chart( fig, use_container_width=True )

        st.markdown( """___""")

    with st.container():

        st.markdown( "### Top 20 Average Rating by Cuisine and their STD" )

        aux = ( df1[['cuisines', 'aggregate_rating']].groupby( 'cuisines' )
            .agg( {'aggregate_rating': ['mean', 'std']} ) )
        aux = aux.reset_index()
        aux.columns = ['cuisines', 'avg_rating', 'std_rating']
        aux = aux.sort_values( 'avg_rating', ascending=False ).head( 20 )

        fig = go.Figure()
        fig.add_trace( go.Bar( name='Control', x=aux['cuisines'], y=aux['avg_rating'],
                               error_y=dict( type='data', array=aux['std_rating'], color='red' ),
                               marker_color='pink' ) )
        fig.update_layout( barmode='group' )
        st.plotly_chart( fig, use_container_width=True )

with tab3:

    with st.container():

        st.markdown( '### You can filter your restaurant in the map' )

        # Create a map with a specific zoom level
        map = folium.Map( location=[0, 0], zoom_start=2 )

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
