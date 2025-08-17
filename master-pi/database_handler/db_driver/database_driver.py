import logging
from contextlib import contextmanager
import psycopg2
import json

class DatabaseDriver:
    def __init__(self, db_info):
        """
        Initialize the DatabaseDriver with the specified database info file.
        """
        self._db_info = db_info
        self._setup_logging()
        self._config = self._load_connection_info()
        

    def _setup_logging(self):
        """
        Set up logging configuration for the class.
        """
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def _load_connection_info(self):
        """
        Load database connection info from a configuration file.
        """
        try:
            with open(self._db_info, 'r', encoding='utf-8') as file:
                config = json.load(file)
            
            required_keys = ['host', 'database', 'user', 'password', 'port']
            
            # Check for missing keys
            for key in required_keys:
                if key not in config:
                    raise ValueError(f"Missing required configuration value: {key}")

            self.logger.info("Database connection info loaded successfully.")
            # Return the connection info as a dictionary
            return config
        except Exception as e:
            self.logger.error(f"Error loading connection info: {e}")
            raise

    @contextmanager
    def _get_connection(self):
        """
        Context manager to open and close a PostgreSQL connection.
        """
        config = self._config
        connection = None
        try:
            # Establish a connection to the PostgreSQL database
            connection = psycopg2.connect(
                host=config['host'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                port=config['port']
            )
            self.logger.info("Connection to the PostgreSQL database established successfully.")
            yield connection
        except Exception as e:
            self.logger.error(f"Error connecting to the PostgreSQL database: {e}")
            raise
        finally:
            if connection:
                connection.close()
                self.logger.info("PostgreSQL database connection closed.")

    def execute_query(self, query, params=None):
        """
        Execute a given query on the database.
        
        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for the SQL query.
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                self.logger.info(f"Executing query: {query} with params: {params}")
                cursor.execute(query, params)
                
                # Check if it's a SELECT statement
                if query.strip().upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    self.logger.info("Query executed successfully and results fetched.")
                    return results
                else:
                    conn.commit()  # Commit changes for INSERT, UPDATE, DELETE queries
                    
                    # Check if there is a RETURNING clause in the query
                    if "RETURNING" in query:
                        result = cursor.fetchone()  # Fetch the first result after INSERT with RETURNING
                        self.logger.info("Query executed successfully with RETURNING clause.")
                        return result  # Return the result from RETURNING clause
                    else:
                        self.logger.info("Query executed successfully.")
                        return None
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            raise
