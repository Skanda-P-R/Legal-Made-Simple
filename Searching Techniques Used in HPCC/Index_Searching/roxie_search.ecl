IMPORT $;
IMPORT PYTHON3 as PY;

DATASET($.File_Legal.Layout3) test1(STRING T) := EMBED(PY)
  
words_list = T.split(',')

lower_case_list = [word.lower() for word in words_list]  

tuple_result = tuple(lower_case_list) 
 
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
STRING100 words_lower;
END;

final_rec doJoin(df2 le, df1 ri) := TRANSFORM
 SELF := le;
 SELF := ri;
END;

final := JOIN(df2,df1,LEFT.words_lower=RIGHT.words_lower,doJoin(LEFT,RIGHT),KEYED(idx1));

new_rec := RECORD
final.text_id;
UNSIGNED4 count_id := COUNT(GROUP);
END;

final_tb := SORT(TABLE(final,new_rec,text_id),-count_id)[1..10];

out_rec := RECORD
STRING text_id;
UNSIGNED2 count_id;
STRING text;
END;

out_rec doJoin2(final_tb le, base_df ri) := TRANSFORM
 SELF := le;
 SELF := ri;
END;

out := JOIN(final_tb,base_df,LEFT.text_id=RIGHT.text_id,doJoin2(LEFT,RIGHT),KEYED(idx2));

RETURN OUTPUT(out);

END;
