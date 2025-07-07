"""Example of parameterized SQL query to avoid injection."""
from typing import List, Dict
import sqlite3


def secure_matrixone_query(query_embedding: str) -> List[Dict[str, str]]:
    """Query the database using parameterized SQL to prevent injection.

    Parameters
    ----------
    query_embedding: str
        Serialized embedding string used for similarity search.

    Returns
    -------
    List[Dict[str, str]]
        Simplified query results.
    """
    conn = sqlite3.connect("matrixone.db")
    cursor = conn.cursor()

    sql = (
        "SELECT id, file, file_name, chunks, title, indexs "
        "FROM chunk_table "
        "ORDER BY l1_norm(chunks_embedding - ?) "
        "LIMIT 5;"
    )

    cursor.execute(sql, (query_embedding,))
    rows = cursor.fetchall()
    result: List[Dict[str, str]] = []
    for row in rows:
        id_, file, file_name, chunks, title, indexs = row
        result.append(
            {
                "id": id_,
                "source": file,
                "file_name": file_name,
                "title": title,
                "index": indexs,
                "chunks": chunks,
            }
        )

    cursor.close()
    conn.close()
    return result
