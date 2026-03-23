"""
SQL Query API - FastAPI Server on Port 8001
Handles DuckDB SQL queries with table validation and error handling.

Author: Amit Nahum
Date: 2026-03-23
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import duckdb
import nest_asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable async support in Jupyter-like environments
nest_asyncio.apply()

app = FastAPI(
    title="DuckDB SQL API",
    description="Execute read-only SQL queries against DuckDB database",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DB_FILE: str = os.getenv("DB_FILE", "my_database.duckdb")
DEFAULT_TABLE: str = "users"


class SQLQuery(BaseModel):
    """Request model for SQL query execution"""
    query: str


class QueryResponse(BaseModel):
    """Response model for query results"""
    columns: List[str]
    data: List[Dict[str, Any]]
    row_count: int


def get_connection() -> duckdb.DuckDBPyConnection:
    """
    Establish connection to DuckDB database.
    
    Returns:
        duckdb.DuckDBPyConnection: Database connection
    """
    return duckdb.connect(DB_FILE, read_only=True)


def table_exists(conn: duckdb.DuckDBPyConnection, table_name: str) -> bool:
    """
    Check if table exists in DuckDB database.
    
    Args:
        conn: DuckDB connection
        table_name: Name of table to check
        
    Returns:
        bool: True if table exists, False otherwise
    """
    try:
        result = conn.execute("SHOW TABLES").fetchall()
        tables = [row[0] for row in result]
        return table_name in tables
    except Exception:
        return False


@app.get("/")
async def root() -> Dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "DuckDB SQL Query API",
        "port": "8001"
    }


@app.post("/query/", response_model=QueryResponse)
async def run_query(sql: SQLQuery) -> Dict[str, Any]:
    """
    Execute SQL query against DuckDB database.
    
    Args:
        sql: SQL query object containing query string
        
    Returns:
        QueryResponse: Query results with columns, data, and row count
        
    Raises:
        HTTPException: If query execution fails or table doesn't exist
    """
    try:
        conn = get_connection()
        
        # Validate that default table exists
        if not table_exists(conn, DEFAULT_TABLE):
            conn.close()
            raise HTTPException(
                status_code=400,
                detail=f"Table '{DEFAULT_TABLE}' does not exist in database. "
                       "Upload a CSV file via the Upload API first."
            )
        
        # Execute query
        df = conn.execute(sql.query).fetchdf()
        conn.close()
        
        return {
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient="records"),
            "row_count": len(df)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"SQL execution error: {str(e)}"
        )


@app.get("/schema/")
async def get_schema() -> Dict[str, Any]:
    """Get schema information for the users table.
    
    Returns:
        Dictionary with table schema details
    """
    try:
        conn = get_connection()
        
        if not table_exists(conn, DEFAULT_TABLE):
            conn.close()
            raise HTTPException(
                status_code=400,
                detail=f"Table '{DEFAULT_TABLE}' does not exist."
            )
        
        # Get column information
        schema = conn.execute(f"PRAGMA table_info({DEFAULT_TABLE})").fetchall()
        conn.close()
        
        columns = [
            {
                "column_name": row[1],
                "data_type": row[2],
                "nullable": not row[3],
                "default": row[4],
                "primary_key": bool(row[5])
            }
            for row in schema
        ]
        
        return {
            "table_name": DEFAULT_TABLE,
            "columns": columns,
            "column_count": len(columns)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Schema retrieval error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("SQL_API_PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)