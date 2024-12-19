from modules.data.dim_hist_load import load_to_dim_hist
from modules.data.dim_load import load_tables_to_dim
from modules.data.staging_load import load_data_into_staging
from modules.db.utils import engine
from modules.models import create_tables

if __name__ == "__main__":
    create_tables(engine=engine)
    load_data_into_staging()
    load_tables_to_dim()
    load_to_dim_hist()
