# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/26 9:54
import sqlite3
from datetime import datetime


class SQL():
    def __init__(self,db_name='data/sql/example.db'):
        # 连接到 SQLite 数据库（如果数据库不存在，则会自动创建）
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_collection_records_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS collection_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,            -- 案件ID
            phone_number TEXT NOT NULL,       -- 电话号码
            name TEXT NOT NULL,               -- 姓名
            relationship TEXT NOT NULL,       -- 关系
            call_result TEXT NOT NULL,        -- 通话结果
            final_result TEXT NOT NULL,       -- 最终结果
            remark LONGTEXT NOT NULL,         -- 备注
            timestamps DATETIME NOT NULL       -- 时间戳
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def operate(self,date_string):
        if not isinstance(date_string,str):
            date_string = str(date_string)
        try:
            # 定义可能的日期格式
            datetime_formats = [
                "%m/%d/%Y %H:%M:%S",  # 带时间的格式，如 "12/24/2024 10:20:47"
                "%Y/%m/%d %H:%M",
                "%m/%d/%Y",
                "%Y/%m/%d",  # 仅日期的格式，如 "2025/2/18"
                "%Y-%m-%d",  # 仅日期的格式，如 "2025-02-18"
                "%Y-%m-%d %H:%M:%S"
            ]

            # 遍历所有可能的格式，尝试解析
            dt_object = None
            for fmt in datetime_formats:
                try:
                    dt_object = datetime.strptime(date_string, fmt)
                    break  # 如果解析成功，跳出循环
                except ValueError:
                    continue  # 如果解析失败，继续尝试下一个格式

            # 如果所有格式都解析失败，则抛出异常
            if dt_object is None:
                raise ValueError("无法匹配任何已知的日期格式")

            # 如果仅日期格式，补全时间为 00:00:00
            if " " not in date_string:
                dt_object = dt_object.replace(hour=0, minute=0, second=0)

            # 返回 datetime 对象
            return dt_object
        except ValueError as e:
            print(f"日期时间格式错误: {e},date string is {date_string}")
            return None

    def create_phone_number_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS phone_numbers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,            -- 案件ID
            phone_number TEXT NOT NULL,       -- 电话号码
            name TEXT NOT NULL,               -- 姓名
            relationship TEXT NOT NULL
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def create_repayments_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS repayments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,           
            case_number TEXT NOT NULL,       
            account TEXT NOT NULL,           
            repayment_time DATETIME NOT NULL,
            repayment_amount FLOAT NOT NULL
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def create_addresses_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,           
            address_type TEXT NOT NULL,       
            address TEXT NOT NULL          
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def create_case_information_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS case_information (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,           
            name TEXT NOT NULL,       
            phone_number TEXT NOT NULL,
            id_card TEXT NOT NULL,
            card_number TEXT NOT NULL,
            city TEXT NOT NULL,
            remark LONGTEXT NOT NULL,
            case_number TEXT NOT NULL,
            final_result TEXT NOT NULL,
            timestamps DATETIME NOT NULL,
            account_opening_time DATETIME NOT NULL,
            start_collection_time DATETIME,
            case_closure_time DATETIME NOT NULL,
            billing_date INT NOT NULL,
            overdue_principal FLOAT NOT NULL,
            assigned_amount FLOAT NOT NULL,
            overdue_penalty FLOAT NOT NULL,
            late_fee FLOAT NOT NULL,
            hand_difference TEXT NOT NULL,
            account TEXT NOT NULL
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def create_call_record_database(self):
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS call_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id TEXT NOT NULL,
            call_time DATETIME NOT NULL,           
            hangup_time DATETIME NOT NULL,       
            call_duration INT NOT NULL,  
            recording_address LONGTEXT NOT NULL,
            asr_result LONGTEXT          
        );
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        # self.conn.close()

    def insert_collection_record2database(self,data):
        # df_columns = ['案件id', '号码', '姓名', '关系', '通话结果', '最终结果', '备注', '时间']
        time_string = data["时间"]
        timestamp = self.operate(time_string)
        insert_sql = '''
            INSERT INTO collection_records (
                case_id, phone_number, name, relationship, 
                call_result, final_result, remark, timestamps
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            '''
        try:
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['案件id'],
                data['号码'],
                data['姓名'],
                data['关系'],
                data['通话结果'],
                data['最终结果'],
                data['备注'],
                timestamp
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")
        # finally:
        #     # 关闭连接
        #     self.conn.close()

    def insert_phone_number2database(self,data):
        # df_columns = ['案件id', '姓名', '号码', '关系']
        insert_sql = '''
                    INSERT INTO phone_numbers(
                        case_id,  name, phone_number, relationship
                    ) VALUES (?, ?, ?, ?);
                    '''
        try:
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['案件id'],
                data['姓名'],
                data['号码'],
                data['关系']
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")
        # finally:
        #     # 关闭连接
        #     self.conn.close()

    def insert_repayments2database(self,data):
        # df_columns = ['案件id','案件号','账号','回款时间','回款金额']
        insert_sql = '''
                            INSERT INTO repayments(
                                case_id,  case_number, account, repayment_time,repayment_amount
                            ) VALUES (?, ?, ?, ?, ?);
                            '''
        timestamp = self.operate(str(data['回款时间']))

        try:
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['案件id'],
                data['案件号'],
                data['账号'],
                timestamp,
                data['回款金额']
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")
        # finally:
        #     # 关闭连接
        #     self.conn.close()

    def insert_addresses2database(self,data):
        # df_columns = ['案件id','地址类型','地址']
        insert_sql = '''
            INSERT INTO addresses(
                case_id,  address_type, address
            ) VALUES (?, ?, ?);
            '''

        try:
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['案件id'],
                data['地址类型'],
                data['地址']
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")

    def insert_case_information2database(self,data):
        # df_columns = ['id','姓名','号码','身份证','卡号','城市','备注','案件号','最终结果','记录时间','开户时间','开催时间','结案时间','账单日',
        # '逾期本金','委案金额','逾期罚息','滞纳金','手别','账号']
        insert_sql = '''
            INSERT INTO case_information(
                case_id,  name, phone_number,id_card,card_number,
                city,remark,case_number,final_result,timestamps,
                account_opening_time,start_collection_time,case_closure_time,billing_date,overdue_principal,
                assigned_amount,overdue_penalty,late_fee,hand_difference,account
            ) VALUES (?, ?, ?,?,?, ?, ?,?,?, ?, ?,?,?, ?, ?,?,?, ?, ?,?);
            '''
        timestamps = self.operate(data["记录时间"])
        account_opening_time = self.operate(data["开户时间"])
        start_collection_time = self.operate(data["开催时间"])
        case_closure_time = self.operate(data["结案时间"])
        billing_date = int(data["账单日"])
        overdue_principal = float(data['逾期本金'])
        assigned_amount = float(data['委案金额'])
        overdue_penalty = float(data["逾期罚息"])
        late_fee = float(data["滞纳金"])
        try:
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['id'],data['姓名'],data['号码'],data['身份证'],data['卡号'],
                data['城市'],data['备注'],data['案件号'],data['最终结果'],timestamps,
                account_opening_time,start_collection_time,case_closure_time,billing_date,overdue_principal,
                assigned_amount,overdue_penalty,late_fee,data['手别'],data['账号']
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")

    def insert_call_record2database(self,data):
        # df_columns = ["案件id","拨打时间","挂短时间","通话时长","录音地址"]
        insert_sql = '''
                    INSERT INTO call_records(
                        case_id,  call_time, hangup_time,call_duration,recording_address
                    ) VALUES (?, ?, ?, ?, ?);
                    '''

        try:
            call_time = self.operate(data["拨打时间"])
            hangup_time = self.operate(data["挂短时间"])
            call_duration = int(data["通话时长"])
            # 提取数据并插入
            self.cursor.execute(insert_sql, (
                data['案件id'],
                call_time,
                hangup_time,
                call_duration,
                data['录音地址']
            ))

            # 提交更改
            self.conn.commit()
            print("数据插入成功！")
        except sqlite3.Error as e:
            print(f"插入数据时发生错误: {e}")