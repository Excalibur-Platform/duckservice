from typing import Optional, List

import duckdb
from fsspec import filesystem
from datetime import datetime
import logging

from handler import Config, Mode

class Worker(object):

    def __init__(
        self,
        config: Config,
        dataset_name: str
    ) -> None:
        
        self.config = config
        self.dataset_name = dataset_name

        db_file_path = f"{config.MNT_DIR}/{dataset_name}.db"
        read_only = True

        if config.MODE == Mode.READ_WRITE:
            read_only = False

        logging.info( f"Init DB Connection : {db_file_path}" )

        try:
            client = duckdb.connect(database=db_file_path, read_only=read_only) 
            client.register_filesystem(filesystem('gcs'))
        except Exception as e:
            logging.error( f"Error Init DB Conenction - { str(e) }" )
            raise ValueError( f"Error Init DB Conenction - { str(e) }" )

        self.client = client
    
    def execute( self, query: str, is_result: bool ) -> Optional[ List[ dict ] ]:

        try:
            logging.info( query )
            self.client.execute( query )
        except Exception as e:
            logging.error( f"Error Execute Query - { str(e) }" )
            raise ValueError( f"Error Execute Query - { str(e) }" )

        if is_result:

            result = None

            try:
                result = self.client.fetch_arrow_table().to_pylist()
            except Exception as e:
                logging.error( f"Error Fetch Query Result - { str(e) }" )
                raise ValueError( f"Error Fetch Query Result - { str(e) }" )

            return result
    
        return None
    
    def close( self ) -> None:
        self.client.close()