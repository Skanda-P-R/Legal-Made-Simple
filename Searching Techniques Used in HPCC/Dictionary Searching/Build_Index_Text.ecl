EXPORT Build_Index_Text := MODULE

base_df := $.File_Legal.File1;

base_df_rec := RECORD
base_df.text_id;
base_df.text;
END;

EXPORT df1 := DATASET('~legal::text_with_id',{base_df_rec,UNSIGNED8 recpos {VIRTUAL(fileposition)}},THOR);

EXPORT idx := INDEX(df1,{text_id,text,recpos},'~idx::legal::text_with_key_4');

EXPORT build_idx := BUILDINDEX(idx);

END;