import json
from langchain_community.llms import GooglePalm
from langchain.chains import LLMChain

from impact_analyzer.prompts import (
    functional_prompt, data_prompt, api_prompt, ui_prompt,
    compliance_prompt, security_prompt, performance_prompt
)
from impact_analyzer.faiss_store import FaissStore

class SystemImpactAnalyzer:
    def __init__(self):
        self.llm = GooglePalm(model="models/chat-bison-001", temperature=0)
        self.faiss_store = FaissStore()

        self.functional_chain = LLMChain(llm=self.llm, prompt=functional_prompt)
        self.data_chain = LLMChain(llm=self.llm, prompt=data_prompt)
        self.api_chain = LLMChain(llm=self.llm, prompt=api_prompt)
        self.ui_chain = LLMChain(llm=self.llm, prompt=ui_prompt)
        self.compliance_chain = LLMChain(llm=self.llm, prompt=compliance_prompt)
        self.security_chain = LLMChain(llm=self.llm, prompt=security_prompt)
        self.performance_chain = LLMChain(llm=self.llm, prompt=performance_prompt)

    def safe_json_loads(self, text):
        try:
            return json.loads(text)
        except Exception:
            return {}

    def analyze(self, change_request_id, change_description):
        context = self.faiss_store.retrieve_context(change_description)

        func_res = self.functional_chain.run(change_desc=change_description, context=context)
        data_res = self.data_chain.run(change_desc=change_description, context=context)
        api_res = self.api_chain.run(change_desc=change_description, context=context)
        ui_res = self.ui_chain.run(change_desc=change_description, context=context)
        compliance_res = self.compliance_chain.run(change_desc=change_description, context=context)
        security_res = self.security_chain.run(change_desc=change_description, context=context)
        performance_res = self.performance_chain.run(change_desc=change_description, context=context)

        func_json = self.safe_json_loads(func_res)
        data_json = self.safe_json_loads(data_res)
        api_json = self.safe_json_loads(api_res)
        ui_json = self.safe_json_loads(ui_res)
        compliance_json = self.safe_json_loads(compliance_res)
        security_json = self.safe_json_loads(security_res)
        performance_json = self.safe_json_loads(performance_res)

        summary = {
            "functional": f"{func_json.get('rules_changed', 'N/A')} rule(s) changed",
            "data": f"{data_json.get('fields_added', 'N/A')} fields added",
            "api": f"{api_json.get('endpoints_modified', 'N/A')} endpoint(s) modified",
            "ui": f"{ui_json.get('screens_affected', 'N/A')} screens affected",
            "compliance": f"{len(compliance_json.get('compliance_flags', []))} compliance flags",
            "security": security_json.get("risk_level", "No major risk"),
            "performance": performance_json.get("latency_impact", "No significant impact")
        }

        details = {
            "functional_analyzer": func_json,
            "data_impact_assessor": data_json,
            "api_impact_assessor": api_json,
            "ui_impact_assessor": ui_json,
            "compliance_impact_assessor": compliance_json,
            "security_impact_assessor": security_json,
            "performance_impact_assessor": performance_json
        }

        return {
            "change_request_id": change_request_id,
            "summary": summary,
            "details": details
        }

def analyze_change_request(change_request_id, change_description):
    analyzer = SystemImpactAnalyzer()
    return analyzer.analyze(change_request_id, change_description)

