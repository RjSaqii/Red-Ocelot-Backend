# RED-OCELOT
git clone https://github.com/RjSaqii/Red-Ocelot-Backend.git 

git clone  https://github.com/RjSaqii/Red-Ocelot-Frontend.git

### Frontend Details

## Content
* Introduction 
* Key Features
* Connection to the Backend

### Introduction
Our method to tackle the Red Ocelot project was to use GitHub API integration to dynamically load the charts. There are 4 charts the bubble chart, bar chart, histogram and the pie chart. Each one this chart will display different information. Also, there are different repositories from which you can change them, and it will dynamically load the data from that specific repository. 

### Key Features 
1. The first feature is to display the data in a graph which is accessed by a button when pressed. This is be done on the same page, when the button is pressed the text-container will disappear and a graph will replace it.
2. The graphs have the option to zoom in and see the data more accurately.
3. There is a dropdown which will allow you to select the repository you want, and it will change the data live.
4. Can input the users name and be able to select the graph they want from the repo they want, this will allows them to be able to compare the results from different users. This allows the users to see theirs and others productivity.


### Connection to the Backend
The frontend connects to the backend using the GitHub API integration. This allows it to load the graphs in dynamically, which will allow a smoother interaction with the interface.

### Backend Details

## Content
* Introduction
* Environment Variables
* Setup
* Connection to the Frontend

### Introduction
The backend used the data from the database or github repositories, converted it into plots using plotly, then the plots were sent to the frontend to be converted into visualisations.

### Environment Variables
Create .env 

GITHUB_ACCESS_TOKEN= {Your token} 

### Setup
1. On /Red-Ocelot-Backend open a terminal 
2. Ensure the Python version is under 3.13
3. pip install psycopg2 (make sure you have prebuilt c++ binaries up to date)
4. pip install plotly 
5. pip install python-decouple 
6. pip install httpx 
7. pip install config

### Connection to the Frontend
The backend connects to the frontend using endpoints, the plots are retrieved and converted into visualisations. 
