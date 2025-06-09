# config/database.py

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st
import os
from contextlib import contextmanager

class DatabaseConfig:
    """Konfigurasi database PostgreSQL"""
    
    @staticmethod
    def get_connection_params():
        """
        Mendapatkan parameter koneksi database
        Bisa dari environment variables atau hardcode untuk development
        """
        return {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'kosbudget_db'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'your_password'),
            'port': os.getenv('DB_PORT', '5432')
        }
    
    @staticmethod
    @contextmanager
    def get_db_connection():
        """
        Context manager untuk koneksi database
        Otomatis close connection setelah selesai
        """
        conn = None
        try:
            params = DatabaseConfig.get_connection_params()
            conn = psycopg2.connect(**params)
            yield conn
        except psycopg2.Error as e:
            st.error(f"Database connection error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    @contextmanager
    def get_db_cursor(connection):
        """
        Context manager untuk cursor database
        Menggunakan RealDictCursor untuk hasil dalam format dictionary
        """
        cursor = None
        try:
            cursor = connection.cursor(cursor_factory=RealDictCursor)
            yield cursor
        except psycopg2.Error as e:
            st.error(f"Database cursor error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()

class DatabaseManager:
    """Manager untuk operasi database umum"""
    
    @staticmethod
    def test_connection():
        """Test koneksi database"""
        try:
            with DatabaseConfig.get_db_connection() as conn:
                with DatabaseConfig.get_db_cursor(conn) as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return True, "Database connection successful"
        except Exception as e:
            return False, f"Database connection failed: {str(e)}"
    
    @staticmethod
    def execute_query(query, params=None, fetch=False):
        """
        Execute query dengan parameter
        
        Args:
            query (str): SQL query
            params (tuple): Parameter untuk query
            fetch (bool): True jika ingin fetch hasil
            
        Returns:
            tuple: (success, result/error_message)
        """
        try:
            with DatabaseConfig.get_db_connection() as conn:
                with DatabaseConfig.get_db_cursor(conn) as cursor:
                    cursor.execute(query, params)
                    
                    if fetch:
                        if query.strip().upper().startswith('SELECT'):
                            result = cursor.fetchall()
                        else:
                            result = cursor.fetchone()
                        conn.commit()
                        return True, result
                    else:
                        conn.commit()
                        return True, "Query executed successfully"
                        
        except psycopg2.Error as e:
            return False, f"Database error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"