# Rappel conso chat application 

In this project, we create a GPT based chatbot  that interacts with a complex database using Langchain agents and tools. The chat application is deployed using Streamlit.

The data is provided by the RappelConso API, a French public service that shares information about product recalls in France.

For a step by step guide on how to run the application and to understand the concepts behind the chatbot, you can check the article I made about this project: https://medium.com/@hamzagharbi_19502/building-a-chat-application-with-langchain-llms-and-streamlit-for-complex-sql-database-7433245079f3
## Demo video

Here is a demo video about some example interactions that we can do with the chatbot: 

[![Watch the video](https://img.youtube.com/vi/1b0iC2akNsU/maxresdefault.jpg)](https://youtu.be/1b0iC2akNsU)


## Quick run 
If you are in a hurry, you can run the application in a few steps. 

First clone the github repo with the following command:
```
git clone https://github.com/HamzaG737/rappel-conso-chat-app.git
```
Next, you can navigate to the project root and install the packages requirements:
```
pip install -r requirements.txt
```
Then you need to setup the Postgres database. In a  [previous project](https://github.com/HamzaG737/data-engineering-project), I covered how to set up a data pipeline for streaming data from a source API directly into a Postgres database. 

However, if you want a simpler solution, I created a script that allows you to transfer all the data from the API straight to Postgres, bypassing the need to set up the entire pipeline.

First off, you need to install Docker. Next, get the Postgres server running with the docker-compose yaml file at the project's root:

```
docker-compose -f docker-compose-postgres.yaml up -d
```

After that, the script `database/stream_data.py` helps you create the rappel_conso_table table, stream the data from the API into the database, and do a quick check on the data by counting the rows. As of February 2024, you should see around 10400 rows, so expect a number close to that.

To run the script, use this command:

```
python database/stream_data.py
```
Please note that the data transfer might take around one minute, possibly a little longer, depending on the speed of your internet connection.

Next you need to set your `OPENAI_API_KEY` as environment variable.

After that everything is set to start the chat application. For that, you can execute the following command:

```
streamlit run streamlit_app/app.py
```

