// #OPTION('outputLimit',650);
IMPORT $,STD;

df1 := $.File_Legal.File2;

rec := RECORD
df1.text_id;
df1.words;
STRING100 words_lower := '';
END;

tb1 := TABLE(df1,rec);

tb1 doUpdate(tb1 le) := TRANSFORM
SELF.words_lower := STD.Str.ToLowerCase(le.words);
SELF := le;
END;

df2 := PROJECT(tb1,doUpdate(LEFT));

OUTPUT(df2,,'~legal::concat_words_lower',OVERWRITE);
