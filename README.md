# Legal Made Simple
The legal system is based on precedents, with earlier court rulings serving as models for current cases. Finding analogous cases and spotting hidden relationships becomes essential in this situation for deciphering legal nuances and gathering pertinent data. But as legal professionals sift through the massive collection of cases, they frequently find intricate patterns and relationships that aren't always obvious. Graph-based solutions are useful in the legal field because they make it possible to depict complex relationships. The ideal choice for this application is to use HPCC systems because they can manage the large-scale data processing and storage needs of creating and querying a legal ontology on a legal data corpus, allowing for effective retrieval of context-aware information.

## Steps to Reproduce the Project
### 1. Clone this project
``` git clone https://github.com/Skanda-P-R/Legal-Made-Simple.git ```
### 2. Install the Huggingface NER model
The NER model is trained on	17485 annotated Case statements, and the model can extract 14 types of Named Entities. They are:<br>
<center>

| Named Entity             |    Extract From    | Description                                                                                                                                               |
|:---------------:|:------------------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| COURT          | Preamble, Judgment | Name of the court which has delivered the current judgement if extracted from Preamble. Name of any court mentioned if extracted from judgment sentences. |
| PETITIONER  | Preamble, Judgment | Name of the petitioners / appellants /revisionist  from current case                                                                                      |
| RESPONDENT | Preamble, Judgment | Name of the respondents / defendents /opposition from current case                                                                                        |
| JUDGE |      Premable, Judgment      | Name of the judges from current case  if extracted from preamble. Name of the judges of the current as well as previous cases if extracted from judgment sentences.       |                                                                                        |
| LAWYER |      Preamble      | Name of the lawyers from both the parties                                                                                                                 |
| DATE |      Judgment      | Any date mentioned in the judgment                                                                                                                        |
| ORG |      Judgment      | Name of organizations mentioned in text apart from court. E.g. Banks, PSU, private companies, police stations, state govt etc.                            |
| GPE |      Judgment      | Geopolitical locations which include names of countries,states,cities, districts and villages                                                             | 
| STATUTE |      Judgment      | Name of the act or law mentioned in the judgement                                                                                                         |
| PROVISION |      Judgment      | Sections, sub-sections, articles, orders, rules under a statute                                                                                           |
| PRECEDENT |      Judgment      | All the past court cases referred in the judgement as precedent. Precedent consists of party names + citation(optional) or case number (optional)         |
| CASE\_NUMBER |      Judgment      | All the other case numbers mentioned in the judgment (apart from precedent) where party names and citation is not provided                                |
| WITNESS    |      Judgment      | Name of witnesses in current judgment                                                                                                                     |
| OTHER_PERSON    |      Judgment      | Name of the all the person that are not included in petitioner,respondent,judge and witness                                                               |     

</center>

To install the model, run this command:<br> ```pip install https://huggingface.co/opennyaiorg/en_legal_ner_trf/resolve/main/en_legal_ner_trf-any-py3-none-any.whl```

### 3. Install the python libraries
Create a virtual environment, or you can directly install the python libraries globally. Run this to install the dependencies:<br> ``` pip install -r requirements.txt ```
### 4. Run the Flask Backend
Run this command to start the flask backend on 127.0.0.1:5000.<br>```python app.py```<br><br>The command promt screen will be something like this:<br><br>![image](https://github.com/user-attachments/assets/876e5457-887e-46b6-b10a-7b07ae50bee4)

### 5. Open the Webpage
Open your prefered browser and go to the link where the Flask Backend is running. By default, it will be "http://127.0.0.1:5000/". If you have done correctly, you should see the webpage like this:<br><br>![image](https://github.com/user-attachments/assets/41f70ddd-def6-47e3-91ae-60cec1d88c7b)
<br><br>Now, you can enter anything related to legal in the **Sample Case Textbox** and the Named Entities extracted from the statement is shown below, along with the **Relevant Case Statements** which matches with the sample text provided.<br>
A Llama model is trained on these extracted case statements, and the user can ask any prompt he likes, and the model will generate relevant answers.<br><br><br>
An example is shown in the below image:<br><br>![image](https://github.com/user-attachments/assets/73fca1ba-36b0-456a-9652-e3ae5f2d3b7a)

## Acknowledgments
* [HPCC Systems](https://hpccsystems.com/) for scalable data processing solutions.
* Hugging Face for providing the NER model infrastructure.
* OpenNYAI for creating the ```en_legal_ner_trf``` legal [NER model](https://huggingface.co/opennyaiorg/en_legal_ner_trf).
* [Groq Cloud](https://groq.com/) for the Llama model.

### PS, if you want to learn how the Application works, please read the "AppWorking.md" file. If you want to read how the case statements are fetched from HPCC System, please click on the "Searching Techniques used in HPCC" folder.
