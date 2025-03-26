# encoding : utf-8 -*-                            
# @author  : 冬瓜                              
# @mail    : dylan_han@126.com    
# @Time    : 2025/3/26 10:11
import json
columns_mapping = {
    "案件id": "case_id",
    "号码": "phone_number",
    "姓名": "name",
    "关系": "relationship",
    "通话结果": "call_result",
    "最终结果": "final_result",
    "备注": "remark",
    "时间": "timestamps",
    "案件号": "case_number",
    "账号": "account",
    "回款时间": "repayment_time",
    "回款金额": "repayment_amount",
    "地址类型": "address_type",
    "地址": "address",
    "id": "case_id",
    "身份证": "id_card",
    "卡号": "card_number",
    "城市": "city",
    "记录时间": "timestamps",
    "开户时间": "account_opening_time",
    "开催时间": "start_collection_time",
    "结案时间": "case_closure_time",
    "账单日": "billing_date",
    "逾期本金": "overdue_principal",
    "委案金额": "assigned_amount",
    "逾期罚息": "overdue_penalty",
    "滞纳金": "late_fee",
    "手别": "hand_difference",
    "拨打时间": "call_time",
    "挂短时间": "hangup_time",
    "通话时长": "call_duration",
    "录音地址": "recording_address"
}

columns_remark = {
    "case_id": "表示案件的唯一标识",
    "phone_number": "电话号码",
    "name": "联系人姓名",
    "relationship": "与欠款人的关系",
    "call_result": "通话的结果描述",
    "final_result": "最终处理结果",
    "remark": "历史催收记录",
    "timestamps": "记录的时间戳",
    "case_number": "案件编号",
    "account": "账户信息",
    "repayment_time": "还款的时间",
    "repayment_amount": "还款金额",
    "address_type": "地址的分类（如家庭地址、工作地址）",
    "address": "具体的地址信息",
    "id_card": "身份证号码",
    "card_number": "银行卡号",
    "city": "所在城市",
    "account_opening_time": "账户开立的时间",
    "start_collection_time": "开始催收的时间",
    "case_closure_time": "案件结束的时间",
    "billing_date": "每个月的还款日期",
    "overdue_principal": "逾期的本金金额",
    "assigned_amount": "委托案件的金额",
    "overdue_penalty": "因逾期产生的罚息",
    "late_fee": "滞纳金金额",
    "hand_difference": "案件的难度等级",
    "call_time": "拨打电话的时间",
    "hangup_time": "挂断电话的时间",
    "call_duration": "通话持续的时间",
    "recording_address": "录音文件的存储地址"
}

table_name_mapping = {
    "催记":{
        "name":"collection_records",
        "remark":"存储关于催收记录的信息。"
    },
    "号码":{
        "name":"phone_numbers",
        "remark":"存储关于联系人的通讯信息及联系人与欠款人的关系"
    },
    "回款":{
        "name":"repayments",
        "remark":"存储有关还款的信息，如时间、金额等"
    },
    "地址":{
        "name":"addresses",
        "remark":"存储各种地址信息"
    },
    "案件信息":{
        "name":"case_information",
        "remark":"存储案件相关的详细信息"
    },
    "话单":{
        "name":"call_records",
        "remark":"存储通话记录或话单信息，包括拨打时间、挂断时间、通话时长等"
    }
}

