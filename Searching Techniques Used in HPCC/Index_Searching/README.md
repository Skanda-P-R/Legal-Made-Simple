# Indexed Searching

This method overcomes the disadvantages of all the other methods used, since this method takes very less time in searching the relavent case statements from the keywords provided.<br>
In this method, we use ```BUILDINDEX``` to build indexes for each record in both the datasets and use these indexed datasets in the ```Keyed JOIN``` function. <br>
Since indexes are built for each record, instead of sequencial access, we can do direct access, and fetch the matched keywords and the case statements in a very less time.

## Steps for running it on a cluster

1. Install the dataset from the link provided in this github repository. You can find the link in the ```RelaventLinks.txt``` file.
2. Clone this repository. Type this in your terminal: ```git clone https://github.com/ManvithLB/Legal-Assistance-HPCC.git```
3. Open ECL watch, and upload the case statement dataset with the text_id, and the extracted keywords dataset on the Landing Zone.
4. Now create a csv file with the following contents: ```Section 18,Civil Appeal,West Bengal,Central Commission,Article 16  4  and 16  4-A,Section 3 7  ,Schedule B,IPC,Section 34,Arms Act,Domicile```. These are also uploaded and sprayed to the cluster under the name ```legal::test_words```. These are used as test words.
5. Now, open the current folder in your ECL IDE or VSCode, and run ```lowercase_the_words.ecl``` to first convert all the extracted keywords to Lowercase, and this file is saved as a logical file of the name ```legal::words_lower```.
6. Next run ```Build_indexes.ecl``` to build the indexes for each record of both the datasets used.
7. You can run the ```Index_Search.ecl``` an verify if the searching is working correctly.
8. Then open ```roxie_search.ecl``` file, and compile the code using ROXIE. In your ECL watch, open the compiled workunit, and publish your query. You can name it whatever you like.
9. Next open your published ROXIE query, enter some test words separated by comma. These keywords will be searched, and the relavent case statements are provided as output.
