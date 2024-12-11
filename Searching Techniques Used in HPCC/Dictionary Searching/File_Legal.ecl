EXPORT File_Legal := MODULE
 
 EXPORT Layout1 := RECORD
  STRING2 field1;
  STRING8 text_id;
  STRING3000 text;
 END;
 
 EXPORT File1 := DATASET('~legal::ildc_multi_text_id',Layout1,CSV);
 
 EXPORT Layout2 := RECORD
  STRING2 field1;
  STRING8 text_id;
  STRING500 words;
 END;
 
 EXPORT File2 := DATASET('~legal::ildc_multi_words',Layout2,CSV);
 
 EXPORT Layout3 := RECORD
  STRING100 words;
 END;
 
 EXPORT File3 := DATASET('~legal::test_words',Layout3,CSV);
 
 EXPORT File4 := DATASET('~legal::idlc_multi_words_lower',Layout2,THOR);
 
END;
