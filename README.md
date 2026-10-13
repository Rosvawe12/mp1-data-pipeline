This pipeline works in a structured way by taking a CSV file and giving a cleaned version. First, the input and config files go through utils, which sets up logging and checks that the files exist. Then, data loaders opens each file based on its type (CSV/ JSON/ YAML). After that, data validator checks that all required columns exist and removes rows with non-numeric values in numeric columns. Then, data processor cleans the data by removing duplicates, missing values, and outliers. Finally, data output saves the cleaned DataFrame as a CSV.  These modules are organized in src and pipeline.py runs them in order. The cleaning steps and settings are controlled by config.yaml, so the pipeline has reusability.


example command : 

```
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```


output : 

```
20:40:44 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
20:40:44 INFO     src.utils — Input file validated: fixtures/sample_data.csv
20:40:44 INFO     src.utils — Input file validated: config/config.yaml
20:40:44 INFO     src.data_loaders — The loaded CSV file: fixtures/sample_data.csv and length of rows in df is: 100
20:40:44 INFO     src.data_loaders — The loaded YAML file: config/config.yaml
20:40:44 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
20:40:44 DEBUG    src.data_validator — Validation: 100 -> 98 rows
20:40:44 INFO     __main__ — Validation complete: 100 -> 98 rows
20:40:44 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
20:40:44 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
20:40:44 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, removed=2
20:40:44 INFO     __main__ — Processing complete: 98 -> 92 rows
20:40:44 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
20:40:44 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```