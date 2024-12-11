# Different Searching Methods
This Folder contains the different methods used for searching the relevant case statements from the keywords provided. We have used different approaches, and the ```Indexed Searching``` takes the shortest time in providing the result.<br><br>
All the methods give the same output for a given set of keywords.
## Base Dataset for Searching
[![Open Spacy Word Extract in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tQbkiYx5rRIXy0kVZ2UcUgD9rdBsBtFM?usp=sharing)<br>This Google Colab file is used to extract all the required keywords from the original ```ILDC Multi Dataset```, and this is saved as a csv file named ```ILDC_multi_concatinated_words.csv```, which has 12,44,044 extracted keywords.
## Steps for running it on a cluster

1. Install the dataset from the link provided in this github repository. You can find the link in the ```RelaventLinks.txt``` file.
2. Clone this repository. Type this in your terminal: ```git clone https://github.com/Skanda-P-R/Legal-Made-Simple.git```
3. Open ECL watch, and upload the case statements dataset, and the extracted keywords dataset on the Landing Zone.
4. Spray both the files using delimited spray, and name the logical files as ``` legal::ildc_multi_text_id``` and ```legal::ildc_multi_concat_words``` respectively.
5. Now create a csv file with the following contents: ```Section 18,Civil Appeal,West Bengal,Central Commission,Article 16  4  and 16  4-A,Section 3 7  ,Schedule B,IPC,Section 34,Arms Act,Domicile```. These are also uploaded and sprayed to the cluster under the name ```legal::test_words```. These are used as test words.
