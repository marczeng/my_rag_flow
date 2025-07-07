import os
import sys
import time
from shutil import copyfile
import types
from typing import List

import pytest

# provide dummy modules so heavy dependencies are not required during tests
dummy_st = types.ModuleType("sentence_transformers")


class DummyModel:
    def __init__(self, *args, **kwargs):
        pass

    def encode(self, *args, **kwargs):
        return [0.0]


dummy_st.SentenceTransformer = DummyModel
sys.modules.setdefault("sentence_transformers", dummy_st)

dummy_pymysql = types.ModuleType("pymysql")
dummy_pymysql.connect = lambda *a, **kw: None
sys.modules.setdefault("pymysql", dummy_pymysql)

dummy_modelscope = types.ModuleType("modelscope")
dummy_modelscope.snapshot_download = lambda *a, **kw: ""
sys.modules.setdefault("modelscope", dummy_modelscope)

from src.core.knowledge_workflow import UserKnowledgeWorkflow


class TestPdfParser:
    """Tests for the PDF parsing workflow."""

    def setup_method(self):
        self.workflow = UserKnowledgeWorkflow()

    def _state_for(self, pdf_path: str):
        return {
            "sessionId": "test_session",
            "input_files": pdf_path,
            "file_type": "AF",
            "file_extension": "pdf",
            "cache": False,
            "error_messages": [],
            "workflow_status": "running",
            "messages": [],
        }

    def test_pdf_parse_success(self, tmp_path):
        sample = os.path.join("data", "pdf", "AF01.pdf")
        target = tmp_path / "sample.pdf"
        copyfile(sample, target)
        state = self._state_for(str(target))
        result_state = self.workflow._parser_pdf(state)
        assert result_state["workflow_status"] != "error"
        assert result_state.get("cache_states")

    def test_pdf_parse_failure(self, tmp_path, caplog):
        corrupt = tmp_path / "corrupt.pdf"
        corrupt.write_text("not a pdf")
        state = self._state_for(str(corrupt))
        with caplog.at_level("ERROR"):
            result_state = self.workflow._parser_pdf(state)
        assert result_state["workflow_status"] == "error"
        assert any("PDF 文件解析失败" in rec.message for rec in caplog.records)

    def test_pdf_parse_performance(self, tmp_path):
        large = os.path.join("data", "pdf", "AZ06.pdf")
        target = tmp_path / "large.pdf"
        copyfile(large, target)
        state = self._state_for(str(target))
        start = time.time()
        result_state = self.workflow._parser_pdf(state)
        duration = time.time() - start
        assert duration < 10
        assert result_state["workflow_status"] != "error"

    def test_pdf_parse_empty_file(self, tmp_path):
        empty = tmp_path / "empty.pdf"
        empty.write_bytes(b"")
        state = self._state_for(str(empty))
        result_state = self.workflow._parser_pdf(state)
        assert result_state["workflow_status"] == "error"
