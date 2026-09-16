import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging
from pathlib import Path

# ============================================================
# Path Configuration (works regardless of where script is run from)
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent  # Goes up from python/ to project root
DATA_DIR = BASE_DIR / "data"

# Configure logging for ITIL Incident Management tracking
log_file = BASE_DIR / "python" / "etl_pipeline.log"
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================
# Database Connection (matches docker-compose.yml)
# ============================================================
DB_URI = "postgresql+psycopg2://olist_user:olist_password@localhost:5433/olist_db"

# ============================================================
# ETL Functions
# ============================================================
def extract_data(file_path: Path) -> pd.DataFrame:
    """Extract raw data from CSV"""
    logging.info(f"Extracting data from {file_path.name}...")
    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")
    return pd.read_csv(file_path)

def transform_data(df: pd.DataFrame, table_type: str) -> pd.DataFrame:
    """Apply data quality and deduplication logic"""
    logging.info(f"Transforming {table_type} data: Deduplicating and cleaning...")
    initial_rows = len(df)
    
    # Drop exact duplicates
    df = df.drop_duplicates()
    
    # Table-specific cleaning
    if table_type == "customers":
        df['customer_city'] = df['customer_city'].fillna('Unknown')
        df['customer_state'] = df['customer_state'].fillna('Unknown')
    elif table_type == "orders":
        # Convert timestamp columns
        for col in ['order_purchase_timestamp', 'order_approved_at', 
                    'order_delivered_carrier_date', 'order_delivered_customer_date',
                    'order_estimated_delivery_date']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
    elif table_type == "order_items":
        # Ensure numeric columns are correct types
        for col in ['price', 'freight_value']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    final_rows = len(df)
    logging.info(f"Removed {initial_rows - final_rows} duplicate/invalid rows from {table_type}")
    return df

def load_data(df: pd.DataFrame, table_name: str, db_connection_string: str):
    """Load cleaned data into PostgreSQL staging schema"""
    logging.info(f"Loading data into staging table: {table_name}...")
    engine = create_engine(db_connection_string)
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info(f"Successfully loaded {len(df)} rows into {table_name}")
    except Exception as e:
        logging.error(f"Failed to load data into {table_name}: {str(e)}")
        raise

# ============================================================
# Main ETL Pipeline
# ============================================================
if __name__ == "__main__":
    logging.info("=" * 60)
    logging.info("ETL Pipeline Started")
    logging.info("=" * 60)
    
    # Define all tables to process
    tables = [
        {
            "file": "olist_customers_dataset.csv",
            "table": "stg_customers",
            "type": "customers"
        },
        {
            "file": "olist_orders_dataset.csv",
            "table": "stg_orders",
            "type": "orders"
        },
        {
            "file": "olist_order_items_dataset.csv",
            "table": "stg_order_items",
            "type": "order_items"
        }
    ]
    
    for config in tables:
        try:
            file_path = DATA_DIR / config["file"]
            raw_df = extract_data(file_path)
            clean_df = transform_data(raw_df, config["type"])
            load_data(clean_df, config["table"], DB_URI)
            logging.info(f"✓ Completed: {config['file']} -> {config['table']}")
        except Exception as e:
            logging.error(f"✗ Failed processing {config['file']}: {str(e)}")
            raise
    
    logging.info("=" * 60)
    logging.info("ETL Pipeline completed successfully.")
    logging.info("=" * 60)
    print("✓ ETL Pipeline completed. Check etl_pipeline.log for details.")