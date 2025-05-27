import json
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI

from impact_analyzer.prompts import (
    functional_prompt, data_prompt, api_prompt, ui_prompt,
    compliance_prompt, security_prompt, performance_prompt
)
from impact_analyzer.faiss_store import FaissStore


INSURANCE_ENTITIES = [
    {
        "id": "Customer",
        "type": "Entity",
        "name": "Customer",
        "description": "An individual or entity purchasing or benefiting from an insurance policy.",
        "attributes": [
            "name", "age", "gender", "contact_details", "occupation", "income",
            "risk_profile", "claims_history", "credit_score", "customer_ID"
        ],
        "owner": "Policyholder Services",
        "impact_dimensions": {
            "functional": ["policy_management", "claims_processing"],
            "data": ["personal_data", "financial_information"],
            "compliance": ["KYC", "GDPR"]
        }
    },
    {
        "id": "Policy",
        "type": "Contract",
        "name": "Policy",
        "description": "The insurance contract outlining coverage, terms, and conditions.",
        "attributes": [
            "policy_number", "type", "premium_amount", "coverage_amount",
            "policy_term", "effective_date", "expiry_date", "status"
        ],
        "owner": "Underwriting",
        "impact_dimensions": {
            "functional": ["policy_issuance", "renewals"],
            "data": ["policy_terms", "coverage_details"],
            "integration": ["Billing_System", "Claims_System"]
        }
    },
    {
        "id": "Insurer",
        "type": "Entity",
        "name": "Insurer",
        "description": "Insurance company providing policies and coverage.",
        "attributes": [
            "company_name", "license_number", "jurisdiction", "financial_rating",
            "contact_information"
        ],
        "owner": "Corporate",
        "impact_dimensions": {
            "functional": ["policy_issuance", "claims_settlement"],
            "compliance": ["Licensing", "Regulatory_Filing"]
        }
    },
    {
        "id": "Claim",
        "type": "Process",
        "name": "Claim",
        "description": "Request made by the customer for compensation under a policy.",
        "attributes": [
            "claim_number", "policy_number", "claim_date", "claim_amount",
            "status", "adjuster_notes"
        ],
        "owner": "Claims Department",
        "impact_dimensions": {
            "functional": ["claims_processing", "fraud_detection"],
            "data": ["claim_details", "payment_information"],
            "compliance": ["Fraud_Rules", "Reporting"]
        }
    },
    {
        "id": "Underwriter",
        "type": "Role",
        "name": "Underwriter",
        "description": "Person or system responsible for assessing risk and pricing policies.",
        "attributes": [
            "employee_id", "name", "region", "expertise_level"
        ],
        "owner": "Underwriting",
        "impact_dimensions": {
            "functional": ["risk_assessment", "policy_approval"],
            "data": ["underwriting_guidelines"]
        }
    },
    {
        "id": "Agent",
        "type": "Role",
        "name": "Agent/Broker",
        "description": "Intermediary who sells policies and provides customer support.",
        "attributes": [
            "agent_id", "name", "license_number", "region", "commission_rate"
        ],
        "owner": "Sales",
        "impact_dimensions": {
            "functional": ["policy_sales", "customer_service"],
            "compliance": ["Agent_Licensing"]
        }
    },
    {
        "id": "Payment",
        "type": "Transaction",
        "name": "Payment",
        "description": "Payments made by customers for premiums or settlements.",
        "attributes": [
            "payment_id", "amount", "payment_date", "payment_method",
            "policy_number", "status"
        ],
        "owner": "Finance",
        "impact_dimensions": {
            "functional": ["billing", "reconciliation"],
            "data": ["payment_records"]
        }
    },
    {
        "id": "Risk",
        "type": "Entity",
        "name": "Risk",
        "description": "Assessment of potential future loss or damage covered by a policy.",
        "attributes": [
            "risk_id", "risk_type", "risk_score", "location", "exposure"
        ],
        "owner": "Risk Management",
        "impact_dimensions": {
            "functional": ["risk_assessment"],
            "data": ["risk_models"],
            "compliance": ["Regulatory_Reporting"]
        }
    },
    {
        "id": "Coverage",
        "type": "Entity",
        "name": "Coverage",
        "description": "Specific protections and limits defined in the policy.",
        "attributes": [
            "coverage_id", "coverage_type", "limit_amount", "deductible"
        ],
        "owner": "Underwriting",
        "impact_dimensions": {
            "functional": ["policy_terms_management"],
            "data": ["coverage_details"]
        }
    },
    {
        "id": "Beneficiary",
        "type": "Entity",
        "name": "Beneficiary",
        "description": "Person or entity designated to receive benefits from a policy.",
        "attributes": [
            "beneficiary_id", "name", "relationship", "contact_info"
        ],
        "owner": "Policyholder Services",
        "impact_dimensions": {
            "functional": ["claims_payment"],
            "data": ["beneficiary_information"]
        }
    },
    {
        "id": "ClaimAdjuster",
        "type": "Role",
        "name": "Claim Adjuster",
        "description": "Person who investigates and processes claims.",
        "attributes": [
            "adjuster_id", "name", "region", "expertise_level"
        ],
        "owner": "Claims Department",
        "impact_dimensions": {
            "functional": ["claims_assessment"],
            "data": ["claim_investigation_data"]
        }
    },
    {
        "id": "Reinsurer",
        "type": "Entity",
        "name": "Reinsurer",
        "description": "Company providing insurance to insurance companies to mitigate risk.",
        "attributes": [
            "company_name", "license_number", "jurisdiction"
        ],
        "owner": "Corporate",
        "impact_dimensions": {
            "functional": ["risk_transfer"],
            "data": ["reinsurance_contracts"]
        }
    },
    {
        "id": "LossEvent",
        "type": "Event",
        "name": "Loss Event",
        "description": "An incident causing damage or loss that may lead to a claim.",
        "attributes": [
            "event_id", "type", "date", "location", "description"
        ],
        "owner": "Claims Department",
        "impact_dimensions": {
            "functional": ["claims_investigation"],
            "data": ["event_reports"]
        }
    },
    {
        "id": "Product",
        "type": "Entity",
        "name": "Product",
        "description": "Insurance product or plan offered to customers.",
        "attributes": [
            "product_id", "name", "description", "terms_conditions", "pricing"
        ],
        "owner": "Product Management",
        "impact_dimensions": {
            "functional": ["product_management", "pricing"],
            "data": ["product_details"]
        }
    },
    {
        "id": "TPAProvider",
        "type": "Entity",
        "name": "Third Party Administrator",
        "description": "External agency managing claims and services on behalf of insurer.",
        "attributes": [
            "provider_id", "name", "contact_info", "service_scope"
        ],
        "owner": "Claims Department",
        "impact_dimensions": {
            "functional": ["claims_processing"],
            "data": ["service_agreements"]
        }
    },
    {
        "id": "FraudCase",
        "type": "Entity",
        "name": "Fraud Case",
        "description": "Identified or suspected insurance fraud incident.",
        "attributes": [
            "case_id", "claim_number", "detection_date", "status", "investigation_notes"
        ],
        "owner": "Fraud Department",
        "impact_dimensions": {
            "functional": ["fraud_detection", "investigation"],
            "data": ["fraud_reports"],
            "compliance": ["Anti-Fraud_Regulations"]
        }
    },
    {
        "id": "Premium",
        "type": "Entity",
        "name": "Premium",
        "description": "The amount paid periodically by a customer for insurance coverage.",
        "attributes": [
            "premium_id", "amount", "payment_frequency", "due_date", "policy_number"
        ],
        "owner": "Finance",
        "impact_dimensions": {
            "functional": ["billing", "collections"],
            "data": ["premium_records"]
        }
    }
]

INSURANCE_RELATIONSHIPS = [
    {
        "source": "Customer",
        "target": "Policy",
        "type": "PURCHASES",
        "direction": "outbound",
        "description": "A customer buys or holds an insurance policy.",
        "attributes": ["purchase_date", "policy_number"],
        "business_rules": [
            "Customer must meet KYC requirements",
            "Policy must be active"
        ]
    },
    {
        "source": "Policy",
        "target": "Insurer",
        "type": "ISSUED_BY",
        "direction": "outbound",
        "description": "The insurer issues the policy.",
        "attributes": ["issue_date", "policy_terms"],
        "business_rules": [
            "Insurer must be licensed in jurisdiction"
        ]
    },
    {
        "source": "Claim",
        "target": "Policy",
        "type": "MAKES_CLAIM_ON",
        "direction": "outbound",
        "description": "A claim is made against a specific policy.",
        "attributes": ["claim_number", "claim_date"],
        "business_rules": [
            "Claim must be within policy coverage period",
            "Claim must be valid and approved"
        ]
    },
    {
        "source": "Claim",
        "target": "ClaimAdjuster",
        "type": "ASSIGNED_TO",
        "direction": "outbound",
        "description": "A claim is assigned to a claim adjuster for processing.",
        "attributes": ["assignment_date", "status"],
        "business_rules": [
            "Adjuster must have required expertise"
        ]
    },
    {
        "source": "Underwriter",
        "target": "Policy",
        "type": "APPROVES",
        "direction": "outbound",
        "description": "An underwriter approves a policy after risk assessment.",
        "attributes": ["approval_date", "risk_score"],
        "business_rules": [
            "Policy must meet underwriting guidelines"
        ]
    },
    {
        "source": "Agent",
        "target": "Customer",
        "type": "SERVES",
        "direction": "outbound",
        "description": "An agent serves a customer for policy sales and support.",
        "attributes": ["contract_date", "commission_rate"],
        "business_rules": [
            "Agent must be licensed"
        ]
    },
    {
        "source": "Policy",
        "target": "Coverage",
        "type": "INCLUDES",
        "direction": "outbound",
        "description": "A policy includes one or more coverages.",
        "attributes": ["coverage_limit", "deductible"],
        "business_rules": [
            "Coverage must comply with product terms"
        ]
    },
    {
        "source": "Policy",
        "target": "Premium",
        "type": "REQUIRES_PAYMENT_OF",
        "direction": "outbound",
        "description": "A policy requires payment of premiums.",
        "attributes": ["amount", "due_date"],
        "business_rules": [
            "Premiums must be paid timely"
        ]
    },
    {
        "source": "Customer",
        "target": "Beneficiary",
        "type": "NAMES",
        "direction": "outbound",
        "description": "A customer names beneficiaries for the policy.",
        "attributes": ["relationship", "percentage_share"],
        "business_rules": [
            "Beneficiaries must be valid individuals/entities"
        ]
    },
    {
        "source": "Insurer",
        "target": "Reinsurer",
        "type": "TRANSFERS_RISK_TO",
        "direction": "outbound",
        "description": "An insurer transfers some risk to a reinsurer.",
        "attributes": ["reinsurance_contract_id", "coverage_amount"],
        "business_rules": [
            "Reinsurer must be licensed"
        ]
    },
    {
        "source": "Claim",
        "target": "FraudCase",
        "type": "MAY_BE_ASSOCIATED_WITH",
        "direction": "outbound",
        "description": "A claim may be associated with a fraud case if suspected.",
        "attributes": ["fraud_flag", "investigation_status"],
        "business_rules": [
            "Fraud investigations must comply with regulations"
        ]
    },
    {
        "source": "Policy",
        "target": "Product",
        "type": "BASED_ON",
        "direction": "outbound",
        "description": "A policy is based on an insurance product.",
        "attributes": ["product_id", "version"],
        "business_rules": []
    },
    {
        "source": "Claim",
        "target": "LossEvent",
        "type": "RESULTS_FROM",
        "direction": "outbound",
        "description": "A claim results from a loss event.",
        "attributes": ["event_id", "description"],
        "business_rules": []
    },
    {
        "source": "TPAProvider",
        "target": "Insurer",
        "type": "SERVICES",
        "direction": "outbound",
        "description": "TPA provider services insurer with claim processing.",
        "attributes": ["service_contract_id", "service_scope"],
        "business_rules": [
            "Services must comply with insurer policies"
        ]
    },
    {
        "source": "Payment",
        "target": "Policy",
        "type": "APPLIES_TO",
        "direction": "outbound",
        "description": "A payment applies to a policy (premium or claim settlement).",
        "attributes": ["payment_date", "amount"],
        "business_rules": []
    }
]




class SystemImpactAnalyzer:
    def __init__(self, api_key: str):
        # ✅ Initialize Gemini 1.5 Flash model with API key
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-1.5-flash",
            temperature=0,
            google_api_key=api_key
        )

        self.faiss_store = FaissStore()

        # ✅ Initialize chains with the Gemini 1.5 Flash LLM
        self.functional_chain = LLMChain(llm=self.llm, prompt=functional_prompt)
        self.data_chain = LLMChain(llm=self.llm, prompt=data_prompt)
        self.api_chain = LLMChain(llm=self.llm, prompt=api_prompt)
        self.ui_chain = LLMChain(llm=self.llm, prompt=ui_prompt)
        self.compliance_chain = LLMChain(llm=self.llm, prompt=compliance_prompt)
        self.security_chain = LLMChain(llm=self.llm, prompt=security_prompt)
        self.performance_chain = LLMChain(llm=self.llm, prompt=performance_prompt)

        # Load domain entities and relationships
        self.entities = INSURANCE_ENTITIES
        self.relationships = INSURANCE_RELATIONSHIPS


    def safe_json_loads(self, text):
        try:
            return json.loads(text)
        except Exception:
            return {}

    def find_impacted_entities(self, change_description):
        """
        Simple keyword matching to find relevant entities.
        Could be enhanced with embedding similarity or LLM calls.
        """
        impacted = []
        text_lower = change_description.lower()

        for entity in self.entities:
            # Check if any attribute, name, or description keywords match
            keywords = [entity['name'].lower()] + [attr.lower() for attr in entity.get('attributes', [])] + [entity.get('description', '').lower()]
            if any(keyword in text_lower for keyword in keywords):
                impacted.append(entity['id'])
        return list(set(impacted))

    def find_impacted_relationships(self, impacted_entities):
        """
        Find relationships involving impacted entities.
        """
        impacted_rels = []
        for rel in self.relationships:
            if rel['source'] in impacted_entities or rel['target'] in impacted_entities:
                impacted_rels.append(rel['type'])
        return list(set(impacted_rels))

    def add_default_deprecation_schedule(self, change_desc):
        # Check if "deprecation schedule" mentioned, else add default
        if "deprecation schedule" not in change_desc.lower():
            # Append a default message to the description
            change_desc += " Deprecation Schedule: No deprecation planned in next 3 minor releases."
        return change_desc
    def analyze(self, change_request_id, change_description):
        # Add default deprecation schedule if missing
        change_description = self.add_default_deprecation_schedule(change_description)

        context = self.faiss_store.retrieve_context(change_description)

        func_res = self.functional_chain.invoke({"change_desc": change_description, "context": context})
        data_res = self.data_chain.invoke({"change_desc": change_description, "context": context})
        api_res = self.api_chain.invoke({"change_desc": change_description, "context": context})
        ui_res = self.ui_chain.invoke({"change_desc": change_description, "context": context})
        compliance_res = self.compliance_chain.invoke({"change_desc": change_description, "context": context})
        security_res = self.security_chain.invoke({"change_desc": change_description, "context": context})
        performance_res = self.performance_chain.invoke({"change_desc": change_description, "context": context})

        func_json = self.safe_json_loads(func_res)
        data_json = self.safe_json_loads(data_res)
        api_json = self.safe_json_loads(api_res)
        ui_json = self.safe_json_loads(ui_res)
        compliance_json = self.safe_json_loads(compliance_res)
        security_json = self.safe_json_loads(security_res)
        performance_json = self.safe_json_loads(performance_res)

        # Domain impact extraction
        impacted_entities = self.find_impacted_entities(change_description)
        impacted_relationships = self.find_impacted_relationships(impacted_entities)

        summary = {
            "functional": f"{func_json.get('rules_changed', 'N/A')} rule(s) changed",
            "data": f"{data_json.get('fields_added', 'N/A')} fields added",
            "api": f"{api_json.get('endpoints_modified', 'N/A')} endpoint(s) modified",
            "ui": f"{ui_json.get('screens_affected', 'N/A')} screens affected",
            "compliance": f"{len(compliance_json.get('compliance_flags', []))} compliance flags",
            "security": security_json.get("risk_level", "No major risk"),
            "performance": performance_json.get("latency_impact", "No significant impact"),
            "domain_entities_impacted": impacted_entities,
            "domain_relationships_impacted": impacted_relationships
        }

        details = {
            "functional_analyzer": func_json,
            "data_impact_assessor": data_json,
            "api_impact_assessor": api_json,
            "ui_impact_assessor": ui_json,
            "compliance_impact_assessor": compliance_json,
            "security_impact_assessor": security_json,
            "performance_impact_assessor": performance_json,
            "domain_entities": [e for e in self.entities if e['id'] in impacted_entities],
            "domain_relationships": [r for r in self.relationships if r['type'] in impacted_relationships]
        }

        return {
            "change_request_id": change_request_id,
            "summary": summary,
            "details": details
        }

def analyze_change_request(change_request_id, change_description, api_key):
    analyzer = SystemImpactAnalyzer(api_key)
    return analyzer.analyze(change_request_id, change_description)
