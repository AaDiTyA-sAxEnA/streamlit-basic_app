import streamlit as st
import pandas as pd
import numpy as np

#adding a title
st.title('Uber pickups in NYC')

#fetching uber dataset for pickups and drop-offs in NYC
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data ##caching also
def load_data(nrows):
    data=pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data
#load_data is a plain old function that downloads some data,
#puts it in a Pandas dataframe, and converts the date column
#from text to datetime. The function accepts a single parameter
#(nrows), which specifies the number of rows that you want to
#load into the dataframe.

#Creating a text element and letting the user know the data is loading
data_load_state = st.text('Loading data...')
#Loading data into dataframe
data = load_data(10000)
#Notifying user that data was successfully loaded
data_load_state.text("Done! (using st.cache_data)")

#We can cache the data and avoid downloading and loading it at every update
#for cache to work properly be sure to have all the libraries and imp things
#that get updated inside the working directory

#cache does not work properly if it pulls data from external time-varying source

#using a toggle button to enable user to inspect raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

#making a histogram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

#plotting data on a map
st.subheader('Map of all pickups averaged over whole day')
st.map(data)

#pickup concentration at a specific hour
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)
#st.map is for simple maps to use more complex maps use st.pydeck_chart
#st.slider can be used to enable user to update the data in the app



