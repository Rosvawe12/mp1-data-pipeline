# data_processor.py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    original_len = len(df)
    new = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {original_len} -> {len(new)} rows")
    return new

def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        new = df.dropna()
        logger.debug(f"handle_missing: {before} -> {len(new)} rows")
    elif axis == "columns":
        before = len(df.columns)
        new = df.dropna(axis=1)
        logger.debug(f"handle_missing: {before} -> {len(new.columns)} columns")
    else:
        logger.error(f"Unsupported axis: {axis}")
        raise ValueError(f"Unsupported axis: {axis}")
    return new


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")
    
    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column is not numeric: {col}")
            continue
        before = len(df)

        if method == "iqr":
            q1 = df[col].quantile(.25)
            q3 = df[col].quantile(.75)
            iqr = q3-q1
            lower = q1 - (threshold * iqr)
            upper = q3 + (threshold * iqr)
            df = df[(df[col] >= lower) & (df[col] <= upper)]

        elif method == "zscore":
            mean = df[col].mean()
            std = df[col].std()
            z_scores = ((df[col] - mean) / std)
            df = df[z_scores.abs() <= threshold]

        logger.debug(f"{col}: method={method}, threshold={threshold}, removed={before - len(df)}")

    return df



def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]
    if settings["remove_duplicates"]:
        df = remove_duplicates(df)
    if settings["missing"]["enabled"]:
        df = handle_missing(df, settings["missing"]["axis"])
    if settings["outliers"]["enabled"]:
        df = remove_outliers(
            df,
            settings["outliers"]["columns"],
            settings["outliers"]["method"],
            settings["outliers"]["threshold"],
        )
    return df



def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    report = {
    "rows_before": len(df_before),
    "rows_after": len(df_after),
    "rows_removed": len(df_before) - len(df_after),
    "columns_before": len(df_before.columns),
    "columns_after": len(df_after.columns),
    "columns_removed": len(df_before.columns) - len(df_after.columns)
    }
    return report