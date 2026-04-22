import aiomysql
from contextlib import asynccontextmanager
from typing import Any, List, Optional, Dict

from app.config import Settings


class Database:
    """Async MySQL database connection pool manager."""
    
    def __init__(self, settings: Settings):
        """Initialize database with settings."""
        self.settings = settings
        self.pool: Optional[aiomysql.Pool] = None
    
    async def connect(self) -> None:
        """Create an async MySQL connection pool with autocommit enabled."""
        try:
            self.pool = await aiomysql.create_pool(
                host=self.settings.db_host,
                port=self.settings.db_port,
                user=self.settings.db_user,
                password=self.settings.db_password,
                autocommit=True,
                minsize=1,
                maxsize=10,
            )
        except aiomysql.Error as e:
            raise ConnectionError(f"Failed to create database connection pool: {e}") from e
    
    async def disconnect(self) -> None:
        """Close the connection pool."""
        if self.pool:
            try:
                self.pool.close()
                await self.pool.wait_closed()
            except aiomysql.Error as e:
                raise ConnectionError(f"Error closing database connection pool: {e}") from e
    
    async def execute(self, query: str, args: tuple = ()) -> None:
        """Execute a query without returning results."""
        try:
            async with self.pool.aquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
        except aiomysql.Error as e:
            raise RuntimeError(f"Error executing query: {e}") from e
    
    async def insert(self, query: str, args: tuple = ()) -> int:
        """
        Insert a record and return the last inserted row id.
        
        Args:
            query: INSERT query string
            args: Query parameters
            
        Returns:
            Last inserted row id
        """
        try:
            async with self._get_connection() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute(query, args)
                    return cursor.lastrowid
        except aiomysql.Error as e:
            raise RuntimeError(f"Error inserting record: {e}") from e
    
    async def fetch_one(self, query: str, args: tuple = ()) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row as a dictionary.
        
        Args:
            query: SELECT query string
            args: Query parameters
            
        Returns:
            Dictionary of the first row or None if no rows found
        """
        try:
            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    result = await cursor.fetchone()
                    return result
        except aiomysql.Error as e:
            raise RuntimeError(f"Error fetching one record: {e}") from e
    
    async def fetch_all(self, query: str, args: tuple = ()) -> List[Dict[str, Any]]:
        """
        Fetch all rows as a list of dictionaries.
        
        Args:
            query: SELECT query string
            args: Query parameters
            
        Returns:
            List of dictionaries for all matching rows
        """
        try:
            async with self.pool.aquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    results = await cursor.fetchall()
                    return results
        except aiomysql.Error as e:
            raise RuntimeError(f"Error fetching all records: {e}") from e
