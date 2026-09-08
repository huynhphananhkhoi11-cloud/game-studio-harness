#!/usr/bin/env python3
"""Deterministic offline NVIDIA NIM adapter for STUDIO-009P-03.

No network, NVIDIA account discovery, API-key resolution, provider SDK/CLI call,
model inference, tool execution, routing, production use, or spend occurs.
"""
from __future__ import annotations
import copy, math
from typing import Any, Iterable
from scripts import credential_redaction as cr
from scripts import provider_onboarding as po

PROVIDER_PROFILE_ID = "provider-profile:nvidia-nim-free-deepseek-v4-pro-0813"
MODEL_PROFILE_ID = "provider-model:nvidia-nim-deepseek-v4-pro-0813"
CHILD_CONTRACT_ID = "STUDIO-009P-03"
MODEL_ID = "deepseek-ai/deepseek-v4-pro-0813"
MODEL_IDENTITY_REF = "model-id:deepseek-ai/deepseek-v4-pro-0813"
HOST = "integrate.api.nvidia.com"
BASE_PATH = "/v1"
BASE_URL = "https://integrate.api.nvidia.com/v1"
CHAT_PATH = "/v1/chat/completions"
TRANSPORT_PROFILE_REF = "transport-profile:nvidia-nim-https-openai-v1"
CREDENTIAL_PROFILE_REF = "credential-profile:nvidia-nim-api-key"
ACCOUNT_REF = "account-ref:nvidia-developer-program-owner-account"
DATA_POLICY_REF = "data-policy:nvidia-nim-public-synthetic-trial"
QUOTA_POLICY_REF = "quota-policy:nvidia-nim-trial-dynamic"
BUDGET_POLICY_REF = "budget-policy:nvidia-nim-zero"
MAX_INPUT_TOKENS = 32768
MAX_OUTPUT_TOKENS = 16384
MAX_REQUEST_BYTES = 262144
MAX_OUTPUT_BYTES = 131072
MAX_CONCURRENCY = 1
MAX_RETRIES = 0
TIMEOUT_SECONDS = 60
ALLOWED_DATA_CLASSIFICATIONS = ("PUBLIC",)
ALLOWED_CAPABILITIES = ("REASONING", "TEXT_GENERATION")
_FORBIDDEN_FIELD_NAMES = {"secret","secret_value","credential_value","token","access_token","refresh_token","password","passwd","private_key","api_key","authorization","cookie","session","session_token","raw_api_key"}
_SAFE_MESSAGES = {
"INVALID_TYPE":"NVIDIA NIM adapter input has an invalid type","EXTRA_FIELD":"NVIDIA NIM adapter input contains unknown fields","MISSING_FIELD":"NVIDIA NIM adapter input is missing required fields",
"MODEL_NOT_ALLOWLISTED":"NVIDIA NIM model is not allowlisted","DATA_NOT_ALLOWED":"data classification is not allowed for NVIDIA NIM trial","INPUT_LIMIT":"estimated NVIDIA NIM input exceeds GAME contract ceiling",
"OUTPUT_LIMIT":"requested NVIDIA NIM output exceeds GAME contract ceiling","REQUEST_TOO_LARGE":"NVIDIA NIM synthetic request exceeds byte ceiling","TOOL_FORBIDDEN":"tool execution is forbidden under STUDIO-009P-03",
"REMOTE_MCP_FORBIDDEN":"remote MCP is forbidden under STUDIO-009P-03","CODE_EXECUTION_FORBIDDEN":"code execution is forbidden under STUDIO-009P-03","FILE_SEARCH_FORBIDDEN":"file search is forbidden under STUDIO-009P-03",
"URL_CONTEXT_FORBIDDEN":"URL context is forbidden under STUDIO-009P-03","ROUTING_FORBIDDEN":"routing or failover is forbidden under STUDIO-009P-03","SECRET_MATERIAL":"secret material is forbidden",
"SYNTHETIC_REQUIRED":"offline NVIDIA NIM adapter accepts synthetic evidence only","RESPONSE_INVALID":"synthetic NVIDIA NIM response is invalid","USAGE_INVALID":"synthetic NVIDIA NIM usage is invalid",
"POLICY_MISMATCH":"NVIDIA NIM policy does not match the accepted contract","CONTRACT_METADATA_INVALID":"NVIDIA NIM metadata failed generic onboarding validation","NONZERO_BUDGET":"NVIDIA NIM monetary ceiling must remain zero",
"PAID_PATH_REQUIRED":"NVIDIA NIM path requires payment or subscription","ZERO_COST_ELIGIBILITY_UNPROVEN":"NVIDIA NIM zero-cost eligibility is unproven","RATE_LIMIT_OR_CAPACITY":"NVIDIA NIM rate limit or capacity prevented execution",
"AUTH_FAILURE":"NVIDIA NIM authentication or authorization failed","REQUEST_VALIDATION_FAILURE":"NVIDIA NIM request validation failed","PROVIDER_EXECUTION_FAILURE":"NVIDIA NIM provider execution failed",
"TIMEOUT":"NVIDIA NIM request timed out","MALFORMED_RESPONSE":"NVIDIA NIM response was malformed","REFERENCE_MISMATCH":"NVIDIA NIM reserved reference does not match contract"}
class NvidiaNimAdapterError(ValueError):
    def __init__(self, code): self.code=code; self.safe_message=_SAFE_MESSAGES.get(code,"NVIDIA NIM adapter rejected input"); super().__init__(self.safe_message)
def _fail(code): raise NvidiaNimAdapterError(code)
def _exact_fields(value, expected):
    if not isinstance(value, dict): _fail("INVALID_TYPE")
    keys=set(value)
    if expected-keys: _fail("MISSING_FIELD")
    if keys-expected: _fail("EXTRA_FIELD")
    return value
def _walk(value):
    stack=[(None,value,0)]; observed=0
    while stack:
        key,item,depth=stack.pop(); observed+=1
        if observed>po.cb.MAX_STRUCTURE_NODES or depth>po.cb.MAX_STRUCTURE_DEPTH: _fail("INVALID_TYPE")
        yield key,item
        if isinstance(item,dict): stack.extend((k,v,depth+1) for k,v in reversed(list(item.items())))
        elif isinstance(item,list): stack.extend((None,v,depth+1) for v in reversed(item))
def _public_preflight(value, byte_limit=None):
    try: raw=po.cb.canonical_json_bytes(value)
    except (TypeError,ValueError,UnicodeEncodeError,RecursionError): _fail("INVALID_TYPE")
    if byte_limit is not None and len(raw)>byte_limit: _fail("REQUEST_TOO_LARGE")
    for key,item in _walk(value):
        if key is not None and key.casefold() in _FORBIDDEN_FIELD_NAMES: _fail("SECRET_MATERIAL")
        if isinstance(item,str) and cr.contains_secret_like(item): _fail("SECRET_MATERIAL")
        if isinstance(item,float) and not math.isfinite(item): _fail("INVALID_TYPE")
def _require_int(value, low, high, code):
    if isinstance(value,bool) or not isinstance(value,int) or not low<=value<=high: _fail(code)
    return value
def validate_reserved_refs(credential_ref, account_ref):
    if credential_ref!=CREDENTIAL_PROFILE_REF or account_ref!=ACCOUNT_REF: _fail("REFERENCE_MISMATCH")
    return {"credential_profile_ref":CREDENTIAL_PROFILE_REF,"account_ref":ACCOUNT_REF}
def validate_static_chain(profile, child, model, transport, data_policy, quota_policy, budget_policy):
    originals=(profile,child,model,transport,data_policy,quota_policy,budget_policy); snapshots=[copy.deepcopy(x) for x in originals]
    for value in snapshots: _public_preflight(value)
    try:
        np=po.validate_provider_profile(profile); nc=po.validate_child_contract_evidence(child, normalized_profile=np); nm=po.validate_model_profile(model, normalized_profile=np, normalized_child=nc)
    except po.ProviderOnboardingError: _fail("CONTRACT_METADATA_INVALID")
    if np["provider_profile_id"]!=PROVIDER_PROFILE_ID or np["profile_status"]!="DISABLED" or np["transport_profile_ref"]!=TRANSPORT_PROFILE_REF or np["credential_profile_ref"]!=CREDENTIAL_PROFILE_REF or np["data_policy_ref"]!=DATA_POLICY_REF or np["quota_policy_ref"]!=QUOTA_POLICY_REF or np["budget_policy_ref"]!=BUDGET_POLICY_REF or tuple(np["allowed_data_classifications"])!=ALLOWED_DATA_CLASSIFICATIONS or tuple(np["allowed_capabilities"])!=ALLOWED_CAPABILITIES: _fail("POLICY_MISMATCH")
    if np["money_ceiling"]!=0: _fail("NONZERO_BUDGET")
    if nc["child_contract_id"]!=CHILD_CONTRACT_ID or nc["evidence_class"]!="SYNTHETIC" or nc["credential_profile_ref"]!=CREDENTIAL_PROFILE_REF: _fail("POLICY_MISMATCH")
    if nm["provider_model_profile_id"]!=MODEL_PROFILE_ID or nm["model_identity_ref"]!=MODEL_IDENTITY_REF or nm["model_status"]!="DECLARED" or tuple(nm["allowed_data_classifications"])!=ALLOWED_DATA_CLASSIFICATIONS or nm["max_request_bytes"]!=MAX_REQUEST_BYTES or nm["max_output_bytes"]!=MAX_OUTPUT_BYTES: _fail("MODEL_NOT_ALLOWLISTED")
    _validate_transport_policy(transport); _validate_data_policy(data_policy); _validate_quota_policy(quota_policy); _validate_budget_policy(budget_policy)
    result={"provider_profile_id":np["provider_profile_id"],"child_contract_id":nc["child_contract_id"],"provider_model_profile_id":nm["provider_model_profile_id"],"model_id":MODEL_ID,"provider_state":"DISABLED","model_state":"DECLARED","child_evidence_class":"SYNTHETIC","network_authority":"NONE","credential_resolution_authority":"NONE","tool_authority":"NONE","routing_authority":"NONE","money_ceiling":0}
    cr.assert_public_safe(result)
    for original,snapshot in zip(originals,snapshots):
        if original!=snapshot: _fail("POLICY_MISMATCH")
    return result
def _validate_transport_policy(v):
    e={"schema_version","transport_profile_id","scheme","host","base_path","canonical_base_url","chat_completions_path","accepted_credential_profile_ref","accepted_account_ref","allow_redirects","allowed_protocols","network_activation"}; v=_exact_fields(v,e)
    if v!={"schema_version":"1.0","transport_profile_id":TRANSPORT_PROFILE_REF,"scheme":"https","host":HOST,"base_path":BASE_PATH,"canonical_base_url":BASE_URL,"chat_completions_path":CHAT_PATH,"accepted_credential_profile_ref":CREDENTIAL_PROFILE_REF,"accepted_account_ref":ACCOUNT_REF,"allow_redirects":False,"allowed_protocols":["HTTPS"],"network_activation":"NONE_P03_OFFLINE"}: _fail("POLICY_MISMATCH")
def _validate_data_policy(v):
    e={"schema_version","data_policy_id","allowed_data_classifications","denied_data_classifications","synthetic_data_allowed","private_or_unreleased_export_allowed","personal_data_allowed","confidential_or_sensitive_data_allowed","trial_collection_risk_acknowledged","connected_activation"}; v=_exact_fields(v,e)
    if v!={"schema_version":"1.0","data_policy_id":DATA_POLICY_REF,"allowed_data_classifications":["PUBLIC"],"denied_data_classifications":["INTERNAL","RESTRICTED"],"synthetic_data_allowed":True,"private_or_unreleased_export_allowed":False,"personal_data_allowed":False,"confidential_or_sensitive_data_allowed":False,"trial_collection_risk_acknowledged":True,"connected_activation":"NONE_P03_OFFLINE"}: _fail("DATA_NOT_ALLOWED")
def _validate_quota_policy(v):
    e={"schema_version","quota_policy_id","provider_snapshot","future_v03_limits","free_eligibility_must_be_reverified","billing_path_allowed","automatic_quota_increase_allowed","on_unproven"}; v=_exact_fields(v,e)
    if v["schema_version"]!="1.0" or v["quota_policy_id"]!=QUOTA_POLICY_REF: _fail("POLICY_MISMATCH")
    if v["provider_snapshot"]!={"entitlement":"DYNAMIC_ACCOUNT_VISIBLE_REQUIRED","permanent_rpm":None,"permanent_rpd":None,"free_endpoint_observed_in_contract_evidence":True}: _fail("POLICY_MISMATCH")
    if v["future_v03_limits"]!={"max_real_requests":3,"max_concurrency":1,"max_retries":0,"timeout_seconds":60,"max_input_tokens":32768,"max_output_tokens":16384,"streaming":False,"tools":False}: _fail("POLICY_MISMATCH")
    if v["free_eligibility_must_be_reverified"] is not True or v["billing_path_allowed"] is not False or v["automatic_quota_increase_allowed"] is not False or v["on_unproven"]!="FAIL_CLOSED": _fail("PAID_PATH_REQUIRED")
def _validate_budget_policy(v):
    e={"schema_version","budget_policy_id","currency","money_ceiling","zero_cost_trial_required","paid_subscription_allowed","auto_recharge_allowed","paid_fallback_allowed","partner_paid_endpoint_allowed","production_use_under_trial_allowed"}; v=_exact_fields(v,e)
    if v["schema_version"]!="1.0" or v["budget_policy_id"]!=BUDGET_POLICY_REF or v["currency"]!="USD": _fail("POLICY_MISMATCH")
    if v["money_ceiling"]!=0: _fail("NONZERO_BUDGET")
    if v["zero_cost_trial_required"] is not True or any(v[k] is not False for k in ("paid_subscription_allowed","auto_recharge_allowed","paid_fallback_allowed","partner_paid_endpoint_allowed","production_use_under_trial_allowed")): _fail("PAID_PATH_REQUIRED")
def normalize_request(value):
    snapshot=copy.deepcopy(value); _public_preflight(value,MAX_REQUEST_BYTES); e={"model","data_classification","messages","estimated_input_tokens","max_output_tokens","stream","tools","remote_mcp","code_execution","file_search","url_context","routing","retries","concurrency","timeout_seconds"}; v=_exact_fields(value,e)
    if v["model"]!=MODEL_ID: _fail("MODEL_NOT_ALLOWLISTED")
    if v["data_classification"]!="PUBLIC": _fail("DATA_NOT_ALLOWED")
    if not isinstance(v["messages"],list) or not v["messages"]: _fail("INVALID_TYPE")
    for message in v["messages"]:
        m=_exact_fields(message,{"role","content"})
        if m["role"] not in {"system","user","assistant"} or not isinstance(m["content"],str): _fail("INVALID_TYPE")
    _require_int(v["estimated_input_tokens"],0,MAX_INPUT_TOKENS,"INPUT_LIMIT"); _require_int(v["max_output_tokens"],1,MAX_OUTPUT_TOKENS,"OUTPUT_LIMIT")
    if v["stream"] is not False: _fail("POLICY_MISMATCH")
    if v["tools"] not in ([],False,None): _fail("TOOL_FORBIDDEN")
    if v["remote_mcp"] not in ([],False,None): _fail("REMOTE_MCP_FORBIDDEN")
    if v["code_execution"] is not False: _fail("CODE_EXECUTION_FORBIDDEN")
    if v["file_search"] is not False: _fail("FILE_SEARCH_FORBIDDEN")
    if v["url_context"] is not False: _fail("URL_CONTEXT_FORBIDDEN")
    if v["routing"] is not False: _fail("ROUTING_FORBIDDEN")
    if v["retries"]!=0 or v["concurrency"]!=1 or v["timeout_seconds"]!=60: _fail("POLICY_MISMATCH")
    result={"synthetic":True,"model":MODEL_ID,"messages":copy.deepcopy(v["messages"]),"max_tokens":v["max_output_tokens"],"stream":False,"tools":[],"network_activity":"NONE","credential_activity":"NONE","routing_activity":"NONE"}; _public_preflight(result,MAX_REQUEST_BYTES)
    if value!=snapshot: _fail("POLICY_MISMATCH")
    return result
def normalize_synthetic_response(value):
    snapshot=copy.deepcopy(value); _public_preflight(value,MAX_OUTPUT_BYTES); v=_exact_fields(value,{"synthetic","model","output_text","usage","finish_reason"})
    if v["synthetic"] is not True: _fail("SYNTHETIC_REQUIRED")
    if v["model"]!=MODEL_ID: _fail("MODEL_NOT_ALLOWLISTED")
    if not isinstance(v["output_text"],str): _fail("RESPONSE_INVALID")
    usage=_exact_fields(v["usage"],{"input_tokens","output_tokens"}); _require_int(usage["input_tokens"],0,MAX_INPUT_TOKENS,"USAGE_INVALID"); _require_int(usage["output_tokens"],0,MAX_OUTPUT_TOKENS,"USAGE_INVALID")
    if v["finish_reason"] not in {"stop","length"}: _fail("RESPONSE_INVALID")
    result={"model":MODEL_ID,"output_text":v["output_text"],"usage":copy.deepcopy(usage),"finish_reason":v["finish_reason"],"network_activity":"NONE","provider_runtime_activity":"NONE","tool_execution_activity":"NONE","spend_usd":0}; cr.assert_public_safe(result)
    if value!=snapshot: _fail("POLICY_MISMATCH")
    return result
def normalize_quota_evidence(value):
    snapshot=copy.deepcopy(value); _public_preflight(value); v=_exact_fields(value,{"synthetic","free_endpoint_visible","account_limit_observed","billing_required","subscription_required"})
    if v["synthetic"] is not True: _fail("SYNTHETIC_REQUIRED")
    for n in ("free_endpoint_visible","account_limit_observed","billing_required","subscription_required"):
        if not isinstance(v[n],bool): _fail("INVALID_TYPE")
    if v["billing_required"] or v["subscription_required"]: _fail("PAID_PATH_REQUIRED")
    if not v["free_endpoint_visible"] or not v["account_limit_observed"]: _fail("ZERO_COST_ELIGIBILITY_UNPROVEN")
    result={"zero_cost_eligible":True,"entitlement_basis":"DYNAMIC_ACCOUNT_VISIBLE_REQUIRED","permanent_rpm_assumed":None,"permanent_rpd_assumed":None,"money_ceiling":0}
    if value!=snapshot: _fail("POLICY_MISMATCH")
    return result
def normalize_error(value):
    snapshot=copy.deepcopy(value); _public_preflight(value); v=_exact_fields(value,{"synthetic","http_status","error_type"})
    if v["synthetic"] is not True: _fail("SYNTHETIC_REQUIRED")
    status=v["http_status"]
    if status is not None and (isinstance(status,bool) or not isinstance(status,int)): _fail("INVALID_TYPE")
    if v["error_type"] not in {None,"timeout","malformed","redirect"}: _fail("INVALID_TYPE")
    if v["error_type"]=="timeout": code="TIMEOUT"
    elif v["error_type"] in {"malformed","redirect"}: code="MALFORMED_RESPONSE"
    elif status==429: code="RATE_LIMIT_OR_CAPACITY"
    elif status in {401,403}: code="AUTH_FAILURE"
    elif status==422: code="REQUEST_VALIDATION_FAILURE"
    elif status is not None and status>=500: code="PROVIDER_EXECUTION_FAILURE"
    else: code="MALFORMED_RESPONSE"
    result={"error_code":code,"retry_allowed":False,"paid_upgrade_allowed":False,"model_fallback_allowed":False,"provider_fallback_allowed":False}
    if value!=snapshot: _fail("POLICY_MISMATCH")
    return result
