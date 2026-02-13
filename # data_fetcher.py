# data_fetcher.py

import pandas as pd

def normalize_crypto_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize raw cryptocurrency data to a consistent schema:
    - Rename columns to standardized names
    - Parse timestamps to pd.Timestamp (UTC)
    - Normalize volume units to base unit (e.g., units of the crypto, not in USD)
    
    Expected input columns might vary by source, examples include:
    - 'time', 'timestamp', 'date' => 'datetime' (pd.Timestamp)
    - 'vol', 'volume' => 'volume'
    - 'open', 'open_price', 'price_open' => 'open'
    - 'high', 'high_price' => 'high'
    - 'low', 'low_price' => 'low'
    - 'close', 'close_price' => 'close'
    - 'market_cap' (optional)
    
    Volume unit normalization:
    - If volume is in USD or other currency, convert to crypto units if possible
      (Assuming volume is in units of crypto for simplicity, as direct inference
      is often not possible without metadata; if volume in USD, user should provide 
      conversion rate externally.)
    
    Returns a DataFrame with columns:
    ['datetime', 'open', 'high', 'low', 'close', 'volume', 'market_cap' (optional)]
    """
    # Make a copy to avoid changing original DataFrame
    df = df.copy()

    # Define possible column mappings for each standard column
    column_map = {
        'datetime': ['time', 'timestamp', 'date', 'datetime'],
        'open': ['open', 'open_price', 'price_open'],
        'high': ['high', 'high_price'],
        'low': ['low', 'low_price'],
        'close': ['close', 'close_price'],
        'volume': ['vol', 'volume', 'volume_traded'],
        'market_cap': ['market_cap', 'marketcap', 'mkt_cap']
    }

    # Rename columns to the standard names if present
    rename_dict = {}
    for std_col, possible_cols in column_map.items():
        for col in possible_cols:
            if col in df.columns:
                rename_dict[col] = std_col
                break  # Only map the first found column

    df.rename(columns=rename_dict, inplace=True)

    # Ensure required columns
