# Libraries

from PIL      import Image

import base64
import streamlit            as st
import pandas               as pd
import plotly.graph_objects as go
import plotly.express       as px

# Functions

def four_stars_restaurant( df1 ):
    with st.container():
        # The Chart Headline
        st.title( "Let's find a City for your next meal?" )

        q13 = ( df1.loc[df1['aggregate_rating'] > 4, :][['city', 'country_code', 'restaurant_id']]
               .groupby(['city'] ).agg( {'country_code': 'first', 'restaurant_id': 'count'} )
               .sort_values( 'restaurant_id', ascending=False ).reset_index() )
        q13 = q13.head( 20 )

        fig = px.bar( q13, x='city', y='restaurant_id', color='country_code',
                     title='Top 20 Cities with more Restaurants over 4 Stars',
                     labels={'restaurant_id': 'Restaurants'} )

        fig.update_layout(xaxis_title='City', yaxis_title='Restaurants', title_font=dict(size=20))
        st.plotly_chart(fig, use_container_width=True)

    return fig

def delivery_online_service( df1 ):

    with st.container():
        st.subheader( 'Cities with more Delivery and Online Ordering Service' )

        col1, col2 = st.columns( 2 )

        with col1:
            q18 = df1.loc[df1['is_delivering_now'] == 1, :][['city', 'restaurant_id']].groupby(
                'city' ).count().sort_values( 'restaurant_id', ascending=False ).reset_index()
            q18 = q18.head( 10 )

            fig = go.Figure( data=[go.Bar(
                x=q18['city'],
                y=q18['restaurant_id'],
                text=q18['restaurant_id'],  # Add total as text inside bars
                textposition='auto',  # Position text inside bars
                marker=dict( color='green', line=dict( color='green', width=1.5 ) ),
                opacity=0.6 )] )

            fig.update_layout( title='Number of Restaurants with Delivery Service', xaxis_title='City',
                              yaxis_title='Restaurants' )
            st.plotly_chart( fig, use_container_width=True )

        with col2:
            q19 = df1.loc[df1['has_online_delivery'] == 1, :][['city', 'restaurant_id']].groupby(
                'city' ).count().sort_values( 'restaurant_id', ascending=False ).reset_index()
            q19 = q19.head( 10 )

            fig = go.Figure( data=[go.Bar(
                x=q19['city'],
                y=q19['restaurant_id'],
                text=q19['restaurant_id'],  # Add total as text inside bars
                textposition='auto',  # Position text inside bars
                marker=dict( color='green', line=dict( color='green', width=1.5 ) ),
                opacity=0.6 )] )

            fig.update_layout( title='Number of Restaurants with Online Ordering', xaxis_title='City',
                              yaxis_title='Restaurants' )
            st.plotly_chart( fig, use_container_width=True )

    return col1, col2

def cuisine_variety( df1 ):
    with st.container():
        q16 = ( df1[['city', 'country_code', 'cuisines']].groupby( ['city', 'country_code'] )
               .nunique().sort_values( 'cuisines', ascending=False ).reset_index() )
        q16 = q16.head( 10 )

        fig = go.Figure( data=[go.Bar(
            x=q16['city'],
            y=q16['cuisines'],
            text=q16['cuisines'],  # Add total as text inside bars
            textposition='auto',  # Position text inside bars
            marker=dict( color='green', line=dict( color='green', width=1.5 ) ),
            opacity=0.6 )] )

        fig = px.bar( q16, x='city', y='cuisines', color='country_code',
                     title='Top 20 Cities with more Restaurants over 4 Stars',
                     labels={'cuisines': 'cuisines'} )

        fig.update_layout( title='Cities with the most Variety of Cuisines', xaxis_title='City',
                          yaxis_title='Number of Restaurants', title_font=dict( size=30 ), title_x=0.1 )
        st.plotly_chart( fig, use_container_width=True )

    return fig

def average_price_city( df1 ):

    with st.container():
        st.subheader( 'Average Price for Two Dishes in $ USD' )

        col1, col2 = st.columns( 2 )

        with col1:
            q15 = ( df1[['city', 'dollar_usd_value']].groupby( 'city' )
                   .mean().sort_values( 'dollar_usd_value', ascending=False ).reset_index() )
            q15 = q15.round( 2 ).head( 10 )
            fig = go.Figure( data=[go.Bar(
                x=q15['city'],
                y=q15['dollar_usd_value'],
                text=q15['dollar_usd_value'],  # Add total as text inside bars
                textposition='auto',  # Position text inside bars
                marker=dict( color='green', line=dict( color='green', width=1.5 ) ),
                opacity=0.6 )] )

            fig.update_layout( title='Top 10 most Expensive Cities', xaxis_title='City',
                              yaxis_title='Price in USD Dollar' )
            st.plotly_chart( fig, use_container_width=True )

        with col2:
            q15 = ( df1[['city', 'dollar_usd_value']].groupby( 'city' )
                   .mean().sort_values( 'dollar_usd_value', ascending=True ).reset_index() )
            q15 = q15.round( 2 ).head( 10 )
            fig = go.Figure( data=[go.Bar(
                x=q15['city'],
                y=q15['dollar_usd_value'],
                text=q15['dollar_usd_value'],  # Add total as text inside bars
                textposition='auto',  # Position text inside bars
                marker=dict( color='green', line=dict( color='green', width=1.5 ) ),
                opacity=0.6 )] )

            fig.update_layout( title='Top 10 Cheapest Cities', xaxis_title='City',
                              yaxis_title='Price in USD Dollar' )
            st.plotly_chart( fig, use_container_width=True )

    return col1, col2

def average_dollar_scatter( df1 ):
    with st.container():
        test_scatter = df1[['city', 'dollar_usd_value']].groupby( 'city' ).mean().sort_values(
            'dollar_usd_value', ascending=False ).reset_index()

        fig = px.scatter( test_scatter, x='city', y='dollar_usd_value',
                         title='Average Dollar USD Value by city',
                         labels={'country_code': 'Country Code', 'dollar_usd_value': 'Average Dollar USD Value'}
                          )

        st.plotly_chart( fig, use_container_width=True )

    return fig

# Read the Treated CSV

df = pd.read_csv( 'zomato_treated_15-04-2024.csv' )

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

# Filters

st.sidebar.markdown( '## Choose the countries you want to see' )

country_options = st.sidebar.multiselect( 'Select Countries',
                                          df1['country_code'].unique(),
                                          default=['Philippines', 'Brazil', 'Australia', 'United States of America',
                                          'Canada', 'Singapure', 'United Arab Emirates', 'England', 'Qatar'] )

cuisines_options = st.sidebar.multiselect( 'Select Cuisines',
                                    df1['cuisines'].unique(),
                                    default=df1['cuisines'].unique() )

min_price, max_price = st.sidebar.slider( "Select Price Range (USD)", df1['dollar_usd_value'].min(),
                                         df1['dollar_usd_value'].max(), ( 0.0, df1['dollar_usd_value'].max() ) )


st.sidebar.markdown( """___""" )

st.sidebar.markdown( '### Treated Data' )

# Add a download button below the markdown sections

if st.sidebar.button('Download Treated Data'):

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

four_stars_restaurant( df1 )

st.markdown( """___""" )

delivery_online_service( df1 )

st.markdown( """___""")

cuisine_variety( df1 )

st.markdown( """___""")

average_price_city( df1 )

st.markdown("""___""")

average_dollar_scatter( df1 )
