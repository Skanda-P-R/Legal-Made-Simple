IMPORT $,STD;
IMPORT PYTHON3 as PY;

DATASET($.File_Legal.Layout3) test1(STRING T) := EMBED(PY)
  
words_list = T.split(',')

tuple_result = tuple(words_list) 
 
return tuple_result;
  
ENDEMBED;

EXPORT roxie_search() := FUNCTION

STRING Tex := '' : STORED('Enter_Words_with_comma');

base_df := $.Build_Index_Text.df1;

df2 := test1(Tex);

df1 := $.Build_Index_Words.df1;

idx1 := $.Build_Index_Words.idx;

idx2 := $.Build_Index_Text.idx;

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

//Dictionary Method, but the problem is to build this dictionary everytime, it takes a lot of time

base_df_rec := RECORD
base_df.text_id;
base_df.text;
END;

tb := TABLE(base_df,base_df_rec,text_id,text);

dct := DICTIONARY(tb,{text_id => text});

Map_id_to_text(STRING text_id) := dct[text_id].text;

out_rec := RECORD
final_tb.text_id;
final_tb.count_id;
STRING text;
END;

out_rec doUpdate(final_tb le) := TRANSFORM
 SELF.text := Map_id_to_text(le.text_id);
 SELF := le;
END;

out := PROJECT(final_tb,doUpdate(LEFT));

RETURN OUTPUT(out);

END;
