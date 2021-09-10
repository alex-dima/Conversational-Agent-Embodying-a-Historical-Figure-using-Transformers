## Introduction
This is the repo for the application detailed in the paper <insert_link_when_available>

## Dependencies
To be able to run everything in this project you will need the following:
* elasticsearch software and python package both need to be installed
* jdk 8 or 11 needs installed and configured
* The following python packages need to be installed: nltk, transformers, openpyxl, pandas, Flask, flask_cors, pytorch (preferably with GPU), sentencepiece
* nodejs and the following npm packages need to be installed: React, react-router-dom, axios, sweetalert2 

## Workflow
* After the previously mentioned packages have been installed, you firstly need to open the elasticsearch executable. 
* After elasticsearch successfully opened, you will run ./Project/backend/app.py, and wait until for about 30 seconds (until the second "App Sucessfully Started" message in the console)
* Next you need to open the ./Project/frontend directory and run the command "npm run start". When completed the page will be automatically opened. If it doesn't automatically open, you can access localhost:3001 manually.

* If everything went accordingly you should see a page similar to this:
<p align="center">
  <img src="https://github.com/alex-dima/Conversational-Agent-Embodying-a-Historical-Figure-using-Transformers/blob/master/Images/Home.png" width="75%"/>
</p>

However the page should not contain the personalities since these are stored in elasticsearch.
To add a personality press the "Add Historical Figure" Button to reach this page:
<p align="center">
  <img src="https://github.com/alex-dima/Conversational-Agent-Embodying-a-Historical-Figure-using-Transformers/blob/master/Images/Add_Personality.png" width="75%"/>
</p>

Here you need to pass the URL to the English wikipedia page of the desired personality. After adding a personality you will be redirected back to the Home page.
To change the transformer model or the retrieval options you can use the two dropdowns from the configurations menu.
The chat menu for a personality looks like this:
<p align="center">
  <img src="https://github.com/alex-dima/Conversational-Agent-Embodying-a-Historical-Figure-using-Transformers/blob/master/Images/Chat.png" width="75%"/>
</p>

## Interaction with the model
To interact with a transformer model for a personality you need to be on that figure's page and write questions in the input box. It is best for the question to use either third person pronouns, either the name of the personality.
After sending a question, the transformer will try giving the best answer.

## Extra Information
In the backend directory there are two files that aren't used when running the application, these are evaluate_questions and compute_scores. These are the scripts used to assess the accuracy of the models. To use them they need to be customised for your own use case.

