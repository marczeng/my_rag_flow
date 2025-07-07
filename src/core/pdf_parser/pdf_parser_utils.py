"""Utility functions describing and improving the PDF parser."""
from typing import List


def describe_pdf_parser() -> str:
    """Return a brief description of how the PDF parser works and its role."""
    return (
        "PDF解析模块通过ParserPDF类读取并解析PDF文件，"
        "利用pdfplumber提取文本、表格和图片OCR结果，"
        "并将这些内容按顺序保存到缓存状态，供后续向量化处理。"
        "出现异常时会记录日志并将工作流状态置为error，确保系统稳定。"
    )


def pdf_parser_improvement_suggestions() -> List[str]:
    """Return detailed suggestions for improving the PDF parser and system."""
    return [
        "支持表格、图片及扫描件的更复杂解析，例如集成OCR识别表格结构", 
        "使用异步或多进程提升批量PDF解析效率", 
        "对解析结果引入缓存和版本控制，避免重复计算", 
        "在异常情况下提供回退策略并增强错误信息", 
        "结合性能监控与日志追踪，持续评估解析质量与速度", 
    ]
