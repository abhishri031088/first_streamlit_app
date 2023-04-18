import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new Healty Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣  Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗  Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔  Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
# Display only selected Fruits or all fuits if nothing selected
if not fruits_selected :
  fruits_to_show = my_fruit_list
else :
  fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

#Create a function
def get_fruityvice_data(this_fruit_choice)
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" +this_fruit_choice)  
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice) 
    # Output in screen as table?
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()
#dont run anything after this
streamlit.stop()


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The Fruit Load List contains :")
streamlit.dataframe(my_data_row)

#Allow end user to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you to add ?','Kiwi')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")


