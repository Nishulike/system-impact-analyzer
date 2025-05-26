from langchain.prompts import PromptTemplate

functional_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "You are a system analyst specialized in functional impacts of software changes.\n"
        "Change Request Description:\n{change_desc}\n\n"
        "Context from system docs:\n{context}\n\n"
        "Provide a detailed analysis of functional impact. "
        "Answer in JSON with keys: rules_changed (int), description (str)."
    )
)

data_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "You are a data impact assessor.\n"
        "Change Request Description:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Describe how data is impacted. "
        "Return JSON with fields_added (int), fields_modified (int), details (str)."
    )
)

api_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze API changes.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Return JSON with endpoints_modified (int), endpoints_added (int), description (str)."
    )
)

ui_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze UI/UX impacts.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Return JSON with screens_affected (int), components_changed (int), summary (str)."
    )
)

compliance_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze compliance impact (e.g., GDPR, security policies).\n"
        "Change Request:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Return JSON with compliance_flags (list), risk_level (str), details (str)."
    )
)

security_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze security risks.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Return JSON with risk_level (str), vulnerabilities_introduced (bool), description (str)."
    )
)

performance_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze performance impact.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context:\n{context}\n\n"
        "Return JSON with latency_impact (str), throughput_impact (str), summary (str)."
    )
)
