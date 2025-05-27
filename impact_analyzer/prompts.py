from langchain.prompts import PromptTemplate

functional_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "You are a system analyst specializing in the functional impacts of software changes.\n"
        "Change Request Description:\n{change_desc}\n\n"
        "Context from system documentation including requirements, existing functionality, and business rules:\n{context}\n\n"
        "Provide a detailed analysis of functional impact.\n"
        "Return *only* a JSON object with these keys:\n"
        "- rules_changed (int): number of business rules impacted\n"
        "- description (str): detailed explanation of the impact\n\n"
        "If no rules are changed, return rules_changed as 0 and provide a relevant description.\n\n"
        "Example:\n"
        "{{\n"
        "  \"rules_changed\": 2,\n"
        "  \"description\": \"This change modifies validation logic for user registration and password policies.\"\n"
        "}}"
    )
)


data_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "You are a data impact assessor.\n"
        "Change Request Description:\n{change_desc}\n\n"
        "Context including database schema, data flows, and storage details:\n{context}\n\n"
        "Describe how data is impacted.\n"
        "Return *only* a JSON object with keys:\n"
        "- fields_added (int): number of new data fields added\n"
        "- fields_modified (int): number of existing fields modified\n"
        "- details (str): detailed explanation of data impact\n\n"
        "If no data fields are changed, set counts to 0 and provide explanation.\n\n"
        "Example:\n"
        "{{\n"
        "  \"fields_added\": 1,\n"
        "  \"fields_modified\": 0,\n"
        "  \"details\": \"Added a new 'customer_segment' field to customer profile data.\"\n"
        "}}"
    )
)


api_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze API changes.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context including current API endpoints and integration details:\n{context}\n\n"
        "Return *only* a JSON object with keys:\n"
        "- endpoints_modified (int): number of endpoints modified\n"
        "- endpoints_added (int): number of new endpoints added\n"
        "- description (str): detailed explanation of API changes\n\n"
        "If no endpoints are changed, set counts to 0 and provide explanation.\n\n"
        "Example:\n"
        "{{\n"
        "  \"endpoints_modified\": 2,\n"
        "  \"endpoints_added\": 1,\n"
        "  \"description\": \"Modified user login endpoint and added new endpoint for multi-factor authentication.\"\n"
        "}}"
    )
)


ui_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze UI/UX impacts.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context including UI screens, components, and user workflows:\n{context}\n\n"
        "Return *only* a JSON object with keys:\n"
        "- screens_affected (int): number of UI screens affected\n"
        "- components_changed (int): number of UI components changed\n"
        "- summary (str): detailed explanation of UI impact\n\n"
        "If no UI changes, set counts to 0 and provide explanation.\n\n"
        "Example:\n"
        "{{\n"
        "  \"screens_affected\": 1,\n"
        "  \"components_changed\": 3,\n"
        "  \"summary\": \"Updated the user profile screen and changed the avatar and contact info components.\"\n"
        "}}"
    )
)


compliance_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze compliance impact (e.g., GDPR, security policies).\n"
        "Change Request:\n{change_desc}\n\n"
        "Context including regulatory requirements and policies:\n{context}\n\n"
        "Return *only* a JSON object with keys:\n"
        "- compliance_flags (list): list of compliance issues flagged\n"
        "- risk_level (str): overall risk level (e.g., Low, Medium, High)\n"
        "- details (str): detailed explanation of compliance impact\n\n"
        "If no compliance issues, return empty list and 'Low' risk level.\n\n"
        "Example:\n"
        "{{\n"
        "  \"compliance_flags\": [\"GDPR data retention\"],\n"
        "  \"risk_level\": \"Medium\",\n"
        "  \"details\": \"Change affects data retention policies requiring review.\"\n"
        "}}"
    )
)


security_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze security risks.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context including security policies, threat models, and controls:\n{context}\n\n"
        "Return *only* a JSON object with keys:\n"
        "- risk_level (str): overall risk level (e.g., None, Low, Medium, High)\n"
        "- vulnerabilities_introduced (bool): whether new vulnerabilities are introduced\n"
        "- description (str): detailed explanation of security impact\n\n"
        "If no security risks, set risk_level to 'None' and vulnerabilities_introduced to false.\n\n"
        "Example:\n"
        "{{\n"
        "  \"risk_level\": \"High\",\n"
        "  \"vulnerabilities_introduced\": true,\n"
        "  \"description\": \"Change introduces potential SQL injection vulnerability in data input handling.\"\n"
        "}}"
    )
)


performance_prompt = PromptTemplate(
    input_variables=["change_desc", "context"],
    template=(
        "Analyze performance impact.\n"
        "Change Request:\n{change_desc}\n\n"
        "Context including system architecture, current performance metrics, and workload:\n{context}\n\n"
        "Return *only* a JSON object with keys:\n"
        "- latency_impact (str): impact on latency (e.g., None, Minor increase, Significant decrease)\n"
        "- throughput_impact (str): impact on throughput\n"
        "- summary (str): detailed explanation of performance impact\n\n"
        "If no performance impact, return 'None' for impacts.\n\n"
        "Example:\n"
        "{{\n"
        "  \"latency_impact\": \"Minor increase\",\n"
        "  \"throughput_impact\": \"No change\",\n"
        "  \"summary\": \"Change adds additional validation step causing slight latency increase.\"\n"
        "}}"
    )
)

