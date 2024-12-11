# Sequencial Searching

This method uses the default ```JOIN``` function, where the keywords are mapped to the original dataset and the frequency of each keyword with respect to the ```text_id``` is calculated.<br>
Next, the matched keywords are mapped to the original case statement using the primary key ```text_id```, and the final result is obtained.<br><br>
The problem with this model is that, the entire dataset has to be sequencially searched, which takes a lot of time, even for ROXIE service.

## Steps for running it on a cluster

1. Install the dataset from the link provided in this github repository. You can find the link in the ```RelaventLinks.txt``` file.
2. Clone this repository. Type this in your terminal: ```git clone https://github.com/ManvithLB/Legal-Assistance-HPCC.git```
3. Open ECL watch, and upload the case statement dataset with the text_id, and the extracted keywords dataset on the Landing Zone.
4. Spray both the files using delimited spray, and name the file ``` legal::ildc_multi_text_id``` and ```legal::ildc_multi_words``` respectively.
5. Now create a csv file with the following contents: ```Section 18,Civil Appeal,West Bengal,Central Commission,Article 16  4  and 16  4-A,Section 3 7  ,Schedule B,IPC,Section 34,Arms Act,Domicile```. These are also uploaded and sprayed to the cluster under the name ```legal::test_words```. These are used as test words.
6. Now, open the current folder in your ECL IDE or VSCode, and you can run ```View_Data.ecl``` to view the dataset uploaded.
7. You can run the ```Search_Words.ecl``` an verify if the searching is working correctly.
8. Then open ```roxie_search.ecl``` file, and compile the code using ROXIE. In your ECL watch, open the compiled workunit, and publish your query. You can name it whatever you like.
9. Next open your published ROXIE query, enter some test words separated by comma. These keywords will be searched, and the relavent case statements are provided as output.
