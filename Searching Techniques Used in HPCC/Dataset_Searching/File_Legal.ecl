EXPORT File_Legal := MODULE
 
 EXPORT Layout1 := RECORD
  STRING field1;
  UNSIGNED text_id;
  STRING text;
 END;
 
 EXPORT File1 := DATASET('~legal::ildc_multi_text_id',Layout1,CSV);
 
 EXPORT Layout2 := RECORD
  STRING field1;
  UNSIGNED text_id;
  STRING words;
 END;
 
 EXPORT File2 := DATASET('~legal::ildc_multi_words',Layout2,CSV);
 
 EXPORT Layout3 := RECORD
  STRING words;
 END;
 
 EXPORT File3 := DATASET('~legal::test_words',Layout3,CSV);
 
END;