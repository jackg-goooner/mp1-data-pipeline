# MP1 Data Pipeline

This command-line pipeline loads CSV, JSON, or YAML input and follows validation and cleaning rules stored in a YAML configuration file. The `src/data_loaders.py` module reads supported input formats, and `src/data_validator.py` checks required columns and removes rows with invalid configured numeric values. The `src/data_processor.py` module removes duplicates, handles missing values, filters outliers, and creates a cleaning report. The `src/data_output.py` module saves the cleaned DataFrame as a CSV without an index, while `src/utils.py` configures logging and checks input paths. The top-level `pipeline.py` coordinates these modules, and `config/` and `fixtures/` hold pipeline settings and example inputs. With the included 100-row sample dataset, validation removes two invalid ratings and the remaining cleaning steps produce 92 rows.

Run the complete pipeline from this directory:

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

The sample run prints this final cleaning report:

```text
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```
