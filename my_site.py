import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS





st.set_page_config(
    page_title="Nina Moisienko•portfolio",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded")


st.markdown(
    """
    <style>
    .main {
    background-color: #FFF7F7;
    }
    </style>
    """, unsafe_allow_html=True)



with st.sidebar:
    
    selected = st.selectbox("Select a project", ["Analysis of world religions", "Analysis of space travelers"])

    

if selected =="Analysis of world religions":
    

    st.title("Analysis of world religions")
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write(' ')
    with col2:
        st.image("stock-religions.jpeg")
    with col3:
        st.write(' ')
        
    st.write("")
    st.write("")
    
    st.subheader("The goals of the analysis:")
    st.write("* *To determine the percentage of people who identify themselves as belonging to a particular religion and those who do not identify with any religion*")
    st.write("* *To analyse trends in the development and distribution of each category*")
    st.write("* *To track trends in the proportion of religions every 10 years around the world*")
    st.write("* *To explore the dominant religions of our future in 2050*")
    st.write("* *To investigate the distribution of world religions around the world, their largest and smallest concentrations*")
    
    st.write("#### About Dataset")
    st.write("This dataset contains the estimated religious composition of 198 countries and territories for 2010 to 2050")
    st.write("#### Where did i find the data?")
    st.write("I found this dataset on ***Kaggle.com***")
    st.write("#### Why did i choose this Dataset?")
    st.write("I selected this dataset to analyse the global spread of religions and forecast changes over the next 30 years. The aim is to examine the evolution of the global religious composition over time")

    
    df = pd.read_csv("rounded_population.csv")
    st.write(df)
    st.subheader("To start, we filtered the data and selected rows where Region equals World")
    
    df_world = df.loc[df["Region"].str.contains("World")] #The contains() method helps us to define rows that contain the world "World"
    st.write(df_world)
    
    st.subheader("Add new column called Affiliated, where we sum up all categories of religion except the category of Unaffiliated")
    unaffiliated_column = df_world.pop('Unaffiliated')  # we use pop() method to remove the 'Unaffiliated' column from df_world
    df_world.insert(3, 'Unaffiliated', unaffiliated_column) #using the insert() method to add a column Unaffiliated at a specific position
    # df_world
    
    df_world["Affiliated"] = df_world.iloc[:, 4:11].sum(axis=1) 
    st.write(df_world)
    
    unaffiliated_column = df_world.pop('Affiliated')
    df_world.insert(3, 'Affiliated', unaffiliated_column)
    
    by_year = df_world.groupby("Year")[["Affiliated", "Unaffiliated"]].sum().reset_index()

    fig = go.Figure(data=[
        go.Bar(name="Affiliated", x=by_year["Year"], y=by_year["Affiliated"], marker_color="#A1DB8A"),
        go.Bar(name="Unaffiliated",x=by_year["Year"], y=by_year["Unaffiliated"], marker_color="#08746D")
    ])

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        title="Population of Affiliated and Unaffiliated to Religion by Year",
        width=1100,
        height=500,
    )
    fig.update_traces(hovertemplate="%{y}", selector=dict(type='bar'))
    st.plotly_chart(fig)
    st.write("#### Make conclusion to graph")
    st.write("On the graph above we see that **number of Affiliated category is quite big compared to Unffiliated**, and tendency of Affiliated is increasing every 10 years compared to the tendency of Unffiliated, which does not change.")
    
    st.write("")
    category = df_world.iloc[:, 4:12]
    category_names = category.columns 
    
    selected_category = st.selectbox("**You can select a Category**", category_names)

    # Create a Plotly figure for the selected category
    fig = go.Figure(data=[
        go.Bar(x=df_world["Year"], y=df_world[selected_category], marker_color="#144448")
    ])

    # Customize the layout of the chart
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        title=f"{selected_category} Population Over Years",
        width=600,
        height=600)    
    
    st.plotly_chart(fig, use_container_width=True)
    st.write("#### Make conclusion to this part")
    st.write("On the graph above we see:")
    st.write("* The tendency of the unffiliated category **does not change much**, from 2020 to 2030 we observe a small increase, from 2030 to 2040 we observe that numbers don't change much, from 2040 to 2050 we observe a decrease.")
    
    st.write("* The tendency of **the category of Christians increases significantly every 10 years**, with **300 - 400 millions people** every 10 years.")
    
    st.write("* The tendency of **the category of Muslims increases significantly every 10 years**, with **300 - 400 millions people** every 10 years.")
    
    st.write("* The tendency of **the category of Hindus increases consistency every 10 years**,but to compare with Christians and Muslims does't very much, with **100 - 200 millions people** every 10 years.")
    
    st.write("* The tendency of **the Buddhist category doesn't increase significantly**, but we also observe a slight decrease in 2040 and 2050.")
    
    st.write("* The tendency of the **Folk Religions category has a small step increase** by 2040 and a small decrease in 2050.")
    
    st.write("* The tendency of **the Other Religions category has a small step increase** by 2040 and a small decrease in 2050.")
    
    st.write("")
    
    
    st.subheader("Trend comparison of categories by year in pie diagram")
    
    category = df_world.iloc[:, 4:12]
    category_names = category.columns
 
    selected_year = st.selectbox("**You can select a Year**", df_world["Year"])

    data_for_year = df_world[df_world["Year"] == selected_year]
    total_count = data_for_year[category_names].sum()


    pie_data = pd.DataFrame({
        "values": total_count.values,
        "names": category_names
    })

    fig = px.pie(pie_data, values="values", names="names", title=f"Category Distribution in {selected_year}",
                 color_discrete_sequence=px.colors.qualitative.Bold)
    fig.update_layout(width=900, height=800)
    fig.update_traces(textinfo='percent+label')
    fig.update_traces(hovertemplate="%{value}")

    st.plotly_chart(fig, use_container_width=True)

    st.write("#### Make conclusion to this part")
    st.write("On the graph above we see:")
    st.write("* 1 diagram 2010 - the **most piece has Christians category 32% than Muslims 23%**")
    
    st.write("* 2 diagram 2020 - the most piece has Christians category 31% than Muslims 25% - we can see that **in 2020 the percentage of Christians is lower at 1%** and the **percentage of Muslims is higher at 2%** - other categories didn't change.")
    
    st.write("* 3 diagram 2030 - the most piece has Christians category 31% than Muslims 27% - we can see that **in 2030 the percentage of Christians doesn't change**, but **for Muslims categore became higher at 2%** - also percentage of **Unaffiliated category is lower at 1%(from 16% to 15%)**, percentage of **Folk Religions become lower at 1%(from 6% to %5)** and percentage of **Buddhists became lower also at 1%(from 7% to 6%)**, others catogories don't change.")
    
    st.write("* 4 diagram 2040 - the most piece has Christians category 31% than Muslims 28% - we can see that **in 2040 the percentage of Christians doesn't change**, but for** Muslims categore became higher at 1%** - also percentage of **Unaffiliated category is lower at 1%(from 15% to 14%)**, others catogories don't change.")
    
    st.write("* 5 diagram 2050 - the most piece has Christians category 31% than Muslims 30% - we can see that **in 2050 the percentage of Christians doesn't change**, but **for Muslims categore became higher at 2%** - also **percentage of Unaffiliated category is lower at 1%(from 14% to 13%)**, the percentage of **Buddhists became lower at 1%(from 6% to 5%)others catogories don't change.**")


    st.subheader("Comparison of 2 the most big categories - Christians and Muslims -  by year in Bar graph")
    by_year = df_world.groupby("Year")[["Christians", "Muslims"]].sum()
    fig = go.Figure(data=[
        go.Bar(name="Christians", x=by_year.index, y=by_year["Christians"]),
        go.Bar(name="Muslims", x=by_year.index, y=by_year["Muslims"], marker_color="#0CC0DF")
    ])

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Population",
        title="Population of Christians and Muslims by Year",
        width=1100,
        height=600
    )

    fig.update_traces(hovertemplate="%{y}")

    st.plotly_chart(fig, use_container_width=True)
    
    st.write("#### Make conclusion to graph")
    st.write("We can observe that the number of Christians and Muslims increases significantly every 10 years, and in 2050 the **number of Christians will be slightly higher than that of Muslims**.")
    st.write("")
    
    st.subheader("Remove rows that contain \"All Countries\" in column Country")
    df_country_delete = df[df["Country"].str.contains("All Countries")].index
    df_country = df.drop(index=df_country_delete)
    # st.write(df_country)
    
    df_country.columns = list(map(str, df_country.columns))
    
    move_column = df_country.pop('Unaffiliated')
    df_country.insert(3, 'Unaffiliated', move_column) #replace Unaffiliated column

    move_column = df_country.pop('All Religions')
    df_country.insert(4, 'All Religions', move_column) #replace All Religions column

    df_country["Affiliated"] = df_country.iloc[:, 5:].sum(axis=1) #add column named Affiliated
    move_column = df_country.pop('Affiliated')
    df_country.insert(4, 'Affiliated', move_column)
    st.write(df_country)
    
    st.subheader("Put 2 categories - Affiliated and Unaffiliated - to visualize on map")
    categories = list(df_country.iloc[:, 3:5])
    for i in categories:
        fig = px.choropleth(df_country,
                                locations='Country', locationmode='country names',
                                color = i,hover_name="Country",
                                animation_frame="Year",
                                title = i,
                                color_continuous_scale='Rainbow')
        

        fig.update_layout(width=1000, height=800)
        st.plotly_chart(fig, use_container_width=True)
    
    st.write("#### Conclusion to this part:")
    st.write("* Affiliated map - we can see that countries such as ***China, USA, Japan have the highest rates around the world*** - and this picture saving upon 2050 year.")
    st.write("* Unaffiliated map - we can see that countries such as ***India, Indonesia, USA, Brazil, China, Nigeria, Russia, Mexico, Pakistan have the highest rates around the world*** - and this picture saving upon 2050 year - but the count among Affiliated population,except India, lower each 10 years.")
    st.write("")
    
    st.subheader("Put all categories, except Affiliated and Unaffiliated, to visualize on maps")
    categories_1 = list(df_country.iloc[:, 6:])
    sel_category = st.selectbox("**You can select a Category to visualize**", categories_1)
    
    fig = px.choropleth(df_country,
                                locations='Country', locationmode='country names',
                                color = sel_category,hover_name="Country",
                                animation_frame="Year",
                                title = f'{sel_category}',
                                color_continuous_scale='Rainbow')
        

    fig.update_layout(width=1000, height=800)
    st.plotly_chart(fig, use_container_width=True)

    st.write("#### Conclusion to this part:")
    st.write("* Christians category map - Most Christians are concentrated in the United States, Brazil, Mexico and Russia. The situation has changed significantly in Russia over the past 10 years, with the number of Christians decreasing, while the number of Christians has increased in some African countries such as Congo and Nigeria, and in the Philippines.")
    
    st.write("* Muslims category map - Most Muslims are concentrated around Asia, Indonesia, and northern Africa, which is not the case with other regions. In 2010, most Muslims were concentrated in Indonesia, and in 2050, India, Pakistan, Bangladesh, and Nigeria will join Indonesia.")
    
    st.write("* Hindus category map - Hindus are most concentrated in India , a situation that has not changed since 2010.")

    st.write("* Buddhists category map - Buddhists are most concentrated in China, Japan, and Thailand. The situation will not change over the next 10 years until 2050.")
    
    st.write("* Folk Religions category map - Folk religions are most prevalent in China and Vietnam.")
    
    st.write("* Other Religions category map -The category of Other religions is most common in China, the USA, Japan, North Korea and India. The situation will not change over the next 10 years until 2050.")

    st.write("* Jews category map -Jews are most concentrated in the United States and Israel.By 2050, these countries will be joined by Canada.")

    st.write("")
    
    
    with open('Religios.txt', 'r') as f:
        religios_text = f.read()
        
    stopwords = set(STOPWORDS)
    religios_cw = WordCloud(
    background_color='white',
    max_words=7000,
    stopwords=stopwords)

    # generate the word cloud
    religios_cw.generate(religios_text)
    #st.image(religios_cw.to_image(), use_column_width=True)
    stopwords.add('countries')
    stopwords.add('religious')
    stopwords.add('s')
    stopwords.add('religions')
    stopwords.add('major')
    stopwords.add('people')
    stopwords.add('many')
    stopwords.add('population')
    stopwords.add('million')
    stopwords.add('number')
    stopwords.add('billion')
    stopwords.add('around')
    stopwords.add('live')
    stopwords.add('include')
    stopwords.add('country')
    stopwords.add('world')

    religios_cw.generate(religios_text)
    st.subheader("**Generating Word Cloud based on article about world religions**")
    st.write("")
    # re-generate the word cloud
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.write(" ")
    with col2:
        st.image(religios_cw.to_image(), width=700, caption="Word Cloud")

    with col3:
        st.write(" ")
    
    st.subheader("General Conclusion to Dataset:")
    
    st.write("* The number of people who identify themselves with a particular category of religion is far greater than the number of so-called agnostics and atheists. The difference is around 80 per cent. There is also a tendency for the number of believers to increase every 10 years, while the number of atheists does not increase by more than 1 million;")
    
    st.write("* From the data, we can see that Muslims and Christians are the biggest and most influential religious groups. Over a 10-year period, their numbers have grown substantially. Looking ahead, the dataset predicts that by 2050, both groups will have similar numbers, but Christianity is expected to be ahead;") 
    
    st.write("* Interestingly, the majority of Hindus worldwide are concentrated in India, with over 1 billion people identifying themselves as Hindus. In contrast, China has the highest proportion of atheists, with almost 70% of the population not identifying with any category;")


    st.write("* If we consider other religions, like Buddhism, folk religions, and Judaism, it's important to note that they have fewer followers in general. The majority of the population identifies as Buddhist, with this percentage ranging between 5 and 8; ")
   
    st.write("* Among all the categories, the smallest percentage of the population identifies themselves as Jews.")




if selected == "Analysis of space travelers":
    
    
    st.title("Analysis of space travellers")
    
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.write(' ')
    with col2:
        st.image("astronauts.jpeg", width=600)
    with col3:
        st.write(' ')
        
    st.write("")
    st.write("")
    
    st.subheader("The goals of the analysis:")
    st.write("* *Analyze the number of flights per country*")
    st.write("* *Find out in which year there were the most flights*")
    st.write("* *Investigate the number of successful, failed, and ongoing flights*")
    st.write("* *Research the percentage of men and women who have been in space*")
    st.write("* *To study the total number of tourists in space, to compare the percentage of men and women among tourists*")
    st.write("* *Investigate the total time spent in space in hours, compare the 5 largest intervals and the smallest, and investigate the age of each person who has been in space and their nationality*")

    
    st.write("#### About Dataset")
    st.write("Consists of all humans to have visited space by going beyond the Kármán Line (100 Kilometers above mean sea level). Consists of Astronauts to have gone in Space, along with any space tourists to have visited Space by going beyond the Kármán line")
    st.write("#### Where did i find the data?")
    st.write("I found this dataset on ***Kaggle.com***, but add to it own columns, such as: Successful or failed or upcoiming, Time in space(generally for person), Gender, Status, Years of a person during the flight")
    st.write("#### Why did i choose this Dataset?")
    st.write("I chose this dataset because I was interested in analyzing the number of space flights, people who have been in space, their total time in space, the leading countries in space")



    dataset_space = pd.read_csv("dataset_anls.csv", delimiter=";")
    st.write(dataset_space)
    st.write("")
    st.write("")
    
    dataset_space["Date"] = pd.to_datetime(dataset_space["Date"], format="%d.%m.%Y")

    dataset_space["Year"] = dataset_space["Date"].dt.year
    new_dataframe_1 = dataset_space.drop(columns=["Date"]).copy()
    new_dataframe_1 = new_dataframe_1.rename(columns={"Year": "Date"})
    
    with st.sidebar:
        st.write("")
  
        st.write('**Selecting a range of years**')
        min_year = new_dataframe_1['Date'].min()
        max_year = new_dataframe_1['Date'].max()
        start_year, end_year = st.slider('Select the start and end years',
                                        min_value=min_year,
                                        max_value=max_year,
                                        value=(min_year, max_year))


    new_dataframe = new_dataframe_1[(new_dataframe_1['Date'] >= start_year) & (new_dataframe_1['Date'] <= end_year)]
    
    
    st.subheader("Create interactive graph for count of flights for each country")
    country_flight_count = new_dataframe.groupby("Launching Country")["Flight "].nunique() # nunique() - return the number of these unique values
    sorted_data = country_flight_count.sort_values(ascending=False) #sort values from higher to lower





    data = {
    'Launching Country': country_flight_count.index,
    'Flight Count': country_flight_count.values
}
    df_flight_counts = pd.DataFrame(data)

    print(df_flight_counts)


    chart = px.bar(sorted_data, x=sorted_data.index, y='Flight ', color_discrete_sequence=["#023271"]) #create bar
    chart.update_xaxes(tickangle=0) #rotation of country for convinient reading
    chart.update_layout(width=1170, height=600) #set width and height
    chart.update_yaxes(title_text='Number of Flights')
    chart.update_traces(
    text=sorted_data.values, # Додаємо кількість польотів як текст на стовпці
    textposition="outside",
    insidetextanchor="end",
    textfont=dict(color='red', size=20) 
)
    chart.update_layout(height=600)
    st.write(chart)
    
    
    
    
    new_dataframe_2 = new_dataframe
    if end_year <= 1991:
        century_20 = new_dataframe_2[new_dataframe_2["Date"].between(1961, 1991)]

        # Group and count unique nationalities
        new_df_2 = century_20.groupby("Launching Country")["Flight "].nunique().reset_index(name="Count")


        map_1 = px.choropleth(new_df_2, 
                            locations='Launching Country', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Launching Country',
                            title=f'Dominant countries by flights to space ({start_year} to {end_year})',
                            color_continuous_scale='plasma',
                            labels={'Launching Country': 'Country Name'})
        map_1.update_layout(width=1000, height=500)
        st.plotly_chart(map_1, use_container_width=True)
    
    elif start_year >= 1992 and end_year <= 2023:

    # Filter data for the second time period (1992-2023)
        century_2021 = new_dataframe[new_dataframe_1["Date"].between(1991, 2023)]

        # Group and count unique nationalities
        new_df_3 = century_2021.groupby("Launching Country")["Flight "].nunique().reset_index(name="Count")

        # Create a choropleth map for the second time period
        map_2 = px.choropleth(new_df_3, 
                            locations='Launching Country', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Launching Country',
                            title=f'Dominant countries by flights to space ({start_year} to {end_year})',
                            color_continuous_scale='plasma',
                            labels={'Launching Country': 'Country Name'})
        map_2.update_layout(width=1000, height=500)
        st.plotly_chart(map_2, use_container_width=True)
        
    else:
        century_20 = new_dataframe_2[new_dataframe_2["Date"].between(1961, 1991)]

        # Group and count unique nationalities
        new_df_2 = century_20.groupby("Launching Country")["Flight "].nunique().reset_index(name="Count")


        map_1 = px.choropleth(new_df_2, 
                            locations='Launching Country', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Launching Country',
                            title=f'Dominant countries by flights to space ({start_year} to 1991)',
                            color_continuous_scale='plasma',
                            labels={'Launching Country': 'Country Name'})
        map_1.update_layout(width=1000, height=500)
        st.plotly_chart(map_1, use_container_width=True)
        
        
        century_2021 = new_dataframe[new_dataframe_1["Date"].between(1991, 2023)]

        # Group and count unique nationalities
        new_df_3 = century_2021.groupby("Launching Country")["Flight "].nunique().reset_index(name="Count")

        # Create a choropleth map for the second time period
        map_2 = px.choropleth(new_df_3, 
                            locations='Launching Country', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Launching Country',
                            title=f'Dominant countries by flights to space (1992 to {end_year})',
                            color_continuous_scale='plasma',
                            labels={'Launching Country': 'Country Name'})
        map_2.update_layout(width=1000, height=500)
        st.plotly_chart(map_2, use_container_width=True)
    
    
    
    st.write("#### Conclusion:")
    st.write("From graph above we can see that max count of unique flights have United States - 166, Russia - 74 and Soviet Union - 62, China - 11, US and SU - 1. ")
    
    st.write("")
    st.write("")   
    st.subheader("Create graph grouped flights by years")
    dataset_space["Date"] = pd.to_datetime(dataset_space["Date"], format="%d.%m.%Y")

    dataset_space["Year"] = dataset_space["Date"].dt.year
    new_dataframe_1 = dataset_space.drop(columns=["Date"]).copy()
    new_dataframe_1 = new_dataframe_1.rename(columns={"Year": "Date"})
    
    
    


    years_flight_count = new_dataframe.groupby("Date")["Flight "].nunique()
    sorted_data = years_flight_count.sort_values(ascending=False)

    chart = px.bar(sorted_data, x=sorted_data.index, y='Flight ', color_discrete_sequence=["#0C19CB"])

    chart.update_xaxes(tickangle=45, title_text='Year') #set title on axis x
    chart.update_yaxes(title_text='Number of Flights')
    chart.update_traces(

    text=sorted_data.values, # Додаємо кількість польотів як текст на стовпці
    textposition="outside",
    insidetextanchor="end",
    textfont=dict(color='red', size=12)
    )
    
    
    

    st.plotly_chart(chart, use_container_width=True)
    st.write("#### Conclusion:")
    st.write("We can observe that the highest number of flights occurred in 1985, 1992, 1994, 1995, 2009, 2021 and 2022. The lower number of flights occurred in the period from 2011 to 2020 to compare with others.")

    st.write("")
    st.write("")    
    st.subheader("Create graph grouped flights to determine which one successful or failed or upcoiming")
    
    yearly_data_state = new_dataframe.groupby(["Date", "Successful or failed or upcoiming"])["Flight "].nunique().unstack(fill_value=0) #use unstack to fill empty gaps

    color_discrete_map = {'failed': 'red', 'successful': 'orange', 'upcoming': '#0074d9'}

    fig = px.bar(yearly_data_state, x=yearly_data_state.index, y=yearly_data_state.columns,
                labels={'value': 'Number of Flights', "x": "Year", "variable": "State"},
                color_discrete_map=color_discrete_map)

    # Налаштування осей та відображення графіка
    fig.update_xaxes(tickangle=45, title_text='Year')
    fig.update_yaxes(title_text='Number of Flights')

    # Відобразіть результати аналізу
    st.plotly_chart(fig, use_container_width=True)


    st.write("#### Conclusion:")
    st.write("The graph above shows that there were many failed space launches in the early years. Now there are many more successful launches, which shows that the rocket industry is developing successfully and technology is constantly improving.")
    st.write("")
    st.write("")   
    st.subheader("Create pie graph to display difference of genders")
    
    total_men = len(new_dataframe[new_dataframe['Gender'] == 'M'])  # Sum of men
    total_women = len(new_dataframe[new_dataframe['Gender'] == 'F'])  # Sum of women

    data = pd.DataFrame({'Gender': ['Men', 'Women'], 'Count': [total_men, total_women]})  # Create a new DataFrame

    chart = px.pie(data, values='Count', names='Gender', title='Percentage of gender in space', 
                color_discrete_sequence=['#0074d9', 'fuchsia'])

    st.plotly_chart(chart, use_container_width=True)
    
    st.write("#### Conclusion:")
    
    st.write("According to the pie chart, men make up a larger percentage than women, suggesting that men may be more resilient in space due to their prior training and greater physical resistance.The difference between them is almost 90%.")
    st.write("")
    st.write("")
    st.subheader("Create bar graph to display tourists by gender")
    
    if end_year < 2001:
        st.write("")
        st.write("")
        st.markdown("<p style='color:red'> !! There are no tourists during this period !! </p>", unsafe_allow_html=True)

        
    else:
        df = new_dataframe.loc[new_dataframe["Status"] == "tourist"]

        status_by_gender = df.groupby("Gender")["Status"].count()
        status_by_gender.index = status_by_gender.index.map({'F': 'Women', 'M': 'Men'})
        data = pd.DataFrame({'Gender': status_by_gender.index, 'Count': status_by_gender})
        chart = px.bar(data, x='Gender', y='Count', title='Count of Tourists in Space by Gender',
                    text='Count', color='Gender', color_discrete_sequence=['fuchsia', '#0074d9'])

        st.plotly_chart(chart, use_container_width=True)
        st.write("#### Conclusion:")
        st.write("Based on the bar chart, the majority of space tourists were male. Out of a total of 36 tourists, 29 were male and only 7 were female.")


        st.write("")
        st.write("")
        st.subheader("Create bar graph to display tourist flights")
        

    
        # dt = df.groupby(["Flight ", "Date"])["Launching Country"].count()
        # st.write(dt)
        
        flights = df["Flight "].unique()
        # st.write(flights)
        
        dt = df.groupby("Launching Country")["Flight "].nunique()
        # st.write(dt)
        dt = dt.reset_index()
        dt = dt.rename(columns={"Flight ": "Count"})

        # Побудова графіку
        chart = px.bar(dt, x='Launching Country', y='Count', title='Count of flights',
                        text='Count')
        chart.update_traces(textfont_size=35)
        chart.update_layout(height=350) 
        st.plotly_chart(chart, use_container_width=True)
        


        st.write("")
        st.write("")
        st.subheader("Create bar graph to display tourists by years")
    
  
        sorted_df = df.sort_values(by='Years of a person during the flight', ascending=True)

        chart = px.bar(sorted_df, x='Years of a person during the flight', y='Name', orientation='h', text='Years of a person during the flight',
                    title='Tourists by age (oldest to youngest)', hover_data=['Nationality', 'Flight ', "Gender", "Time in space(generally for person) DD:HH:MM ",
                                                                            "Date"], color_discrete_sequence=["#0074d9"])

        chart.update_layout(xaxis_title='Years of a Person During the Flight',
                        yaxis_title='Name')
        
        chart.update_traces(textangle=0)


        # st.plotly_chart(chart, use_container_width=True)
        chart.update_layout(height=800 , width=1130)
        st.write(chart)
        st.write("#### Conclusion:")
        st.write("The majority of tourists who go into space are elderly people aged 50 to 60. Among the oldest tourists: William Shatner - 90 years old and Wally Funk - 82 years old. Among the youngest: Oliver Daemen - 18 years old and Anissa Melanie - 23 years old.")
        st.write("")
        st.write("")
        
        st.subheader("TOP-5 oldest tourists in space")

        sorted_df = df.sort_values(by='Years of a person during the flight', ascending=True)
        df_k = sorted_df.tail(5)
        chart = px.bar(df_k, x='Years of a person during the flight', y='Name', orientation='h', text='Years of a person during the flight',
                    title='Oldest tourists by age', hover_data=['Nationality', 'Flight ', "Gender", "Time in space(generally for person) DD:HH:MM ",
                                                            "Date"], color_discrete_sequence=["#0074d9"])

        chart.update_layout(xaxis_title='Years of a Person During the Flight',
                        yaxis_title='Name', width=1000, height=400)
        st.plotly_chart(chart, use_container_width=True)

        st.write("")
        st.write("")
        st.subheader("TOP-5 youngest tourists in space")

        sorted_df = df.sort_values(by='Years of a person during the flight', ascending=True)
        df_k = sorted_df.head(5)
        chart = px.bar(df_k, x='Years of a person during the flight', y='Name', orientation='h', text='Years of a person during the flight',
                    title='Youngest tourists by age', hover_data=['Nationality', 'Flight ', "Gender", "Time in space(generally for person) DD:HH:MM ",
                                                                "Date"], color_discrete_sequence=["#0074d9"])

        chart.update_layout(xaxis_title='Years of a Person During the Flight',
                        yaxis_title='Name', width=1000, height=400)

        st.plotly_chart(chart, use_container_width=True)

    st.write("")
    st.write("")
    
    st.subheader("Create bar graph to display people with the longest time in space")
    
    
    def convert_time_to_hours(time): #convert our time in hours
        parts = time.split(':')
        if len(parts) == 3:
            days, hours, minutes = map(int, parts)
            total_hours = days * 24 + hours + minutes / 60
            return total_hours
        else:
            return 0 

    new_dataframe['Time_in_space_hours'] = new_dataframe['Time in space(generally for person) DD:HH:MM '].apply(convert_time_to_hours) #add new column
    dk = pd.DataFrame(new_dataframe) #create new DF
    dk = dk.sort_values(by='Time_in_space_hours', ascending=False) 
    dk_head = dk.head(30) #display first 30

    chart = px.bar(dk_head, x='Name', y='Time_in_space_hours', title='People with the longest time in space',
                labels={'Time_in_space_hours': 'Time in Space (hours)'}, 
                hover_data=['Nationality', "Gender", "Time in space(generally for person) DD:HH:MM ", "Status", "Years of a person during the flight", 
                        "Date"])

    chart.update_layout(xaxis_title='Name', yaxis_title='Time in space (hours)', xaxis_tickangle=45)
    st.plotly_chart(chart, use_container_width=True)


    dk_head = dk.tail(40) #display last 40

    chart = px.bar(dk_head, x='Name', y='Time_in_space_hours', title='People with the smallest time in space',
                labels={'Time_in_space_hours': 'Time in Space (hours)'}, 
                hover_data=['Nationality', "Gender", "Time in space(generally for person) DD:HH:MM ", "Status", "Years of a person during the flight",
                        "Flight ", "Date"])

    chart.update_layout(xaxis_title='Name', yaxis_title='Time in space (hours)', xaxis_tickangle=45)
    st.plotly_chart(chart, use_container_width=True)
    
    
    st.write("#### Conclusion:")
    st.write("From the first graph above, we can see the people who have been in space the longest, and it is worth noting that they have been in space for more than a year, and some of them even more than two. These people are mostly from Russia and America. The second graph shows the people who were in space for the shortest amount of time, mostly tourists who flew for 10 minutes, mostly from America.")

    st.write("")
    st.write("")
    st.subheader("Nationallity of people that in space")
    
    new_dataframe_1 = new_dataframe
    if end_year <= 1991:
        century_20 = new_dataframe_1[new_dataframe_1["Date"].between(1961, 1991)]

        # Group and count unique nationalities
        new_df_1 = century_20.groupby("Nationality").size().reset_index(name="Count")


        map_1 = px.choropleth(new_df_1, 
                            locations='Nationality', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Nationality',
                            title=f'Number of people that were in space by Nationality ({start_year} to {end_year})',
                            color_continuous_scale='plasma')
        map_1.update_layout(width=1000, height=800)
        st.plotly_chart(map_1, use_container_width=True)
    elif start_year > 1991 and end_year <= 2023:
        # Filter data for the second time period (1992-2023)
        century_2021 = new_dataframe[new_dataframe_1["Date"].between(1992, 2023)]

        # Group and count unique nationalities
        new_df_2 = century_2021.groupby("Nationality").size().reset_index(name="Count")

        # Create a choropleth map for the second time period
        map_2 = px.choropleth(new_df_2, 
                            locations='Nationality', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Nationality',
                            title=f'Number of people by Nationality that were in space ({start_year} to {end_year})',
                            color_continuous_scale='plasma')
        map_2.update_layout(width=1000, height=800)
        st.plotly_chart(map_2, use_container_width=True)

    else:
        century_20 = new_dataframe_1[new_dataframe_1["Date"].between(1961, 1991)]

        # Group and count unique nationalities
        new_df_1 = century_20.groupby("Nationality").size().reset_index(name="Count")

        gap_year = 1991
        map_1 = px.choropleth(new_df_1, 
                            locations='Nationality', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Nationality',
                            title=f'Number of people that were in space by Nationality ({start_year} to {gap_year})',
                            color_continuous_scale='plasma')
        map_1.update_layout(width=1000, height=800)
        st.plotly_chart(map_1, use_container_width=True)
        
        century_2021 = new_dataframe[new_dataframe_1["Date"].between(1992, 2023)]

        # Group and count unique nationalities
        new_df_2 = century_2021.groupby("Nationality").size().reset_index(name="Count")

        # Create a choropleth map for the second time period
        map_2 = px.choropleth(new_df_2, 
                            locations='Nationality', 
                            locationmode='country names',
                            color='Count',
                            hover_name='Nationality',
                            title=f'Number of people by Nationality that were in space (1992 to {end_year})',
                            color_continuous_scale='plasma')
        map_2.update_layout(width=1000, height=800)
        st.plotly_chart(map_2, use_container_width=True)
    st.write("#### Conclusion:")
    st.write("On the first map, we can see that most of the people by nationality who have been in space are from the United States and the Soviet Union. From the second map we can see that most of the people who have been in space by nationality are from the United States, Russia, Canada, China and Japan.")
