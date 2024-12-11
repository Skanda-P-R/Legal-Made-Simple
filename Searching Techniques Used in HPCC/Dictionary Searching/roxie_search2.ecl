IMPORT $,STD;
IMPORT PYTHON3 as PY;

DATASET($.File_Legal.Layout3) test1(STRING T) := EMBED(PY)
  
words_list = T.split(',')

tuple_result = tuple(words_list) 
 
return tuple_result;
  
ENDEMBED;

EXPORT roxie_search2() := FUNCTION

STRING Tex := '' : STORED('Enter_Words_with_comma');

rec1 := RECORD
UNSIGNED text_id;
UNSIGNED count_id;
STRING text;
END;

df2 := test1(Tex);

df1 := $.Build_Index_Words.df1;

idx1 := $.Build_Index_Words.idx;

final_rec := RECORD
STRING5 text_id;
STRING100 words;
END;

final_rec doJoin(df2 le, df1 ri) := TRANSFORM
 SELF := le;
 SELF := ri;
END;

final := JOIN(df2,df1,LEFT.words=RIGHT.words,doJoin(LEFT,RIGHT),KEYED(idx1));

new_rec := RECORD
final.text_id;
UNSIGNED4 count_id := COUNT(GROUP);
END;

final_tb := SORT(TABLE(final,new_rec,text_id),-count_id)[1..10];

base_df := $.File_Legal.File1;

DATASET(rec1) merge_df(DATASET(new_rec) final_tb) := EMBED(PY)
  
import csv
import sys

csv.field_size_limit(sys.maxsize)

final_tb = [(int(text_id), int(count_id)) for text_id, count_id in final_tb]

sentences_file = "/var/lib/HPCCSystems/mydropzone/ILDC_multi_text_id.csv"

text_id_to_text = {}

with open(sentences_file, 'r') as file:
  reader = csv.reader(file)
  next(reader)
  for row in reader:
    text_id = int(row[1])
    text = row[2]
    text_id_to_text[text_id] = text

merged_list = []

for text_id, count_id in final_tb:
  
  if text_id in text_id_to_text:
    merged_list.append((text_id, count_id, text_id_to_text[text_id]))
  else:
    pass

return merged_list

ENDEMBED;

out := merge_df(final_tb);

RETURN OUTPUT(out);

END;
