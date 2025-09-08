from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def build_db_uri(
    DB_USER: str = None,
    DB_PW: str = None,
    DB_HOST: str = None,
    DB_PORT: int = None,
    DB_NAME: str = None,
    dialect: str = 'postgresql'
) -> str:
    """
    Build a PostgreSQL database URI with or without authentication.
    
    Args:
        DB_USER: Database username (optional for some configurations)
        DB_PW: Database password (optional for some configurations)
        DB_HOST: Database host address
        DB_PORT: Database port
        DB_NAME: Database name
        dialect: Database dialect (default: postgresql)
        
    Returns:
        str: Database connection URI
    """
    # Check that required parameters are provided
    if not all([DB_HOST, DB_PORT, DB_NAME]):
        raise ValueError("DB_HOST, DB_PORT, and DB_NAME are required")
    
    # If no user/password provided, create URI without authentication
    if not DB_USER or not DB_PW:
        return f"{dialect}://{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        return f"{dialect}://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
