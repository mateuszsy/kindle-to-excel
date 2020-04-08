# Kindle to Excel
Extract vocabulary builder and clipping's data located on Kindle and create an Excel file out of that in a desired form. 

## Extractions
For now script extracts vocabulary builder data which consists of words that have been searched throughout a book read.

## Arguments

| Argument         | Type    | Default      | Help  | 
| ---------------- | ------- | ------------ | ----- |
| -n, --name       | String  | kindle_vocab | File name for spreadsheet | 
| -f, --format     | -       | False        | Extract with omitted columns and tables | 
| -p, --partition  | String  | E            | Kindle (removable) partition name | 
| -h               | -       | -            | Show help | 


## TODO
* extractor for vocabulary builder
* extractor for clippings