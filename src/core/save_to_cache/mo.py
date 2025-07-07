# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/17 17:19
try:
    import pymysql
except Exception:  # pragma: no cover - optional dependency
    pymysql = None

class MatrixOne:
    def __init__(self):
        if pymysql is None:  # pragma: no cover - optional dependency
            raise ImportError("pymysql is required for MatrixOne")
        self.db = pymysql.connect(
            host='117.186.222.46',
            port=6001,
            user='root',
            password="111",
            db='competition'
        )
        self.cursor = self.db.cursor()

    def _create_database_document(self):
        instruction = """CREATE TABLE chunk_table(
id int(11) AUTO_INCREMENT PRIMARY KEY,
file VARCHAR NOT NULL,
file_name VARCHAR NOT NULL,
chunks LONGTEXT NOT NULL,
category VARCHAR NOT NULL,
title VARCHAR NOT NULL,
address VARCHAR NOT NULL,
indexs VARCHAR NOT NULL,
chunks_embedding vecf32(1024),
sub_chunks_embedding vecf32(1024),
title_embedding vecf32(1024),
file_name_embedding vecf32(1024)
);"""
        self.cursor.execute(instruction)
        self.db.commit()

    def _create_database_split_document(self):
        instruction = """CREATE TABLE sub_chunk_table(
        id int(11) AUTO_INCREMENT PRIMARY KEY,
        file VARCHAR NOT NULL,
        file_name VARCHAR NOT NULL,
        chunks LONGTEXT NOT NULL,
        sub_chunks LONGTEXT NOT NULL,
        category VARCHAR NOT NULL,
        title VARCHAR NOT NULL,
        address VARCHAR NOT NULL,
        indexs VARCHAR NOT NULL,
        sub_indexs VARCHAR NOT NULL,
        chunks_embedding vecf32(1024),
        sub_chunks_embedding vecf32(1024),
        title_embedding vecf32(1024),
        file_name_embedding vecf32(1024)
        );"""
        self.cursor.execute(instruction)
        self.db.commit()

    def _insert_to_table(self, table, columns, values):
        """Insert a row into ``table`` using parameterized SQL."""
        column = ",".join(columns)
        placeholders = ",".join(["%s"] * len(values))
        sql_instruction = f"INSERT INTO {table} ({column}) VALUES ({placeholders})"
        self.cursor.execute(sql_instruction, values)
        self.db.commit()

    def _insert_to_table_abstract(self, columns, values, table):
        """Insert a row into ``table`` using parameterized SQL (abstracted)."""
        column = ",".join(columns)
        placeholders = ",".join(["%s"] * len(values))
        sql_instruction = f"INSERT INTO {table} ({column}) VALUES ({placeholders})"
        self.cursor.execute(sql_instruction, values)
        self.db.commit()

    def search_to_table(self, embed, column_name="chunks_embedding", method="l1_norm", table_name="handx"):
        assert method in ["l1_norm", "l2_norm", "cosine_similarity"]
        instruction = "SELECT file,file_name,chuncks,category,title FROM {table_name} ORDER BY {method}({column_name} - '{embed}') LIMIT 10;".format(
            table_name=table_name, method=method, column_name=column_name, embed=embed
        )

        self.cursor.execute(instruction)
        result = self.cursor.fetchall()
        result = [list(item) for item in result]

        return result

if __name__ == '__main__':
    func = MatrixOne()
    func._create_database_document()
    func._create_database_split_document()
