# Dictionary Searching

In this method, the keyword matching is done using ```Keyed JOIN```, but, the mapping of the keywords to their repective case statements using the primary key ```text_id``` is done using dictionaries.<br>
In this method, a function called ```Map_id_to_text``` is created, which maps the provided text_id to its respective case statement. This is called each time in the ```TRANSFORM``` function, and this is applied to the matched keywords dataset, so each ```text_id``` are mapped to their corressponding case statement.<br><br>
The only disadvantage in this method is that, whenever the ROXIE query is called, each time, the dictionary gets created, and since the dataset is huge, it takes a lot of time creating the dictionary.<br><br>
Also, you can find the file ```roxie_search2.ecl```, where the same is implemented using Embedded Python, which also take somewhat the same time to execute.

## Steps for running it on a cluster

1. Install the dataset from the link provided in this github repository. You can find the link in the ```RelaventLinks.txt``` file.
2. Clone this repository. Type this in your terminal: ```git clone https://github.com/ManvithLB/Legal-Assistance-HPCC.git```
3. Open ECL watch, and upload the case statement dataset with the text_id, and the extracted keywords dataset on the Landing Zone.
4. Now create a csv file with the following contents: ```Section 18,Civil Appeal,West Bengal,Central Commission,Article 16  4  and 16  4-A,Section 3 7  ,Schedule B,IPC,Section 34,Arms Act,Domicile```. These are also uploaded and sprayed to the cluster under the name ```legal::test_words```. These are used as test words.
5. Now, open the current folder in your ECL IDE or VSCode, and run ```Build_index.ecl``` to build the indexe for the keywords dataset.
6. Then open ```roxie_search.ecl``` file, and compile the code using ROXIE. In your ECL watch, open the compiled workunit, and publish your query. You can name it whatever you like.
7. Next open your published ROXIE query, enter some test words separated by comma. These keywords will be searched, and the relavent case statements are provided as output.
8. You can also compile the ```roxie_search2.ecl``` file, and publish it to the ROXIE server. This query uses Embedded Python and does the exact same fuctionality.
