EXPORT Build_Index_Words := MODULE

df := $.File_Legal.File4;

rec := RECORD
df.text_id;
df.words_lower;
END;

EXPORT df1 := DATASET('~legal::concat_words_lower',{rec,UNSIGNED8 recpos {VIRTUAL(fileposition)}},THOR);

EXPORT idx := INDEX(df1,{text_id,words_lower,recpos},'~legal::words_with_key_11');

EXPORT build_idx := BUILDINDEX(idx);

END;
