# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/13 15:16
import uuid
from datetime import datetime

def get_time(days=True):
    now = datetime.now()
    if days:
        return now.strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d-%H:%M:%S")

def get_uuid(prefix=""):
    return str(uuid.uuid4()) if prefix=="" else prefix+"-"+str(uuid.uuid4())

def _judge_heading_isin(param):
    for unit in param:
        if "Heading" in unit[-1]:
            return True
    return False


