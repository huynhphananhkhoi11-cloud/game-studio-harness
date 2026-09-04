#!/usr/bin/env python3
"""Deterministic STUDIO-009R connected-validation evidence validator.

Validates metadata only. It never resolves credentials or performs provider calls.
"""
from __future__ import annotations
import copy, hashlib, json, math, re
from datetime import datetime, timezone

SCHEMA_VERSION="1.0"; MAX_INPUT_BYTES=1_048_576; MAX_STRUCTURE_DEPTH=32; MAX_STRUCTURE_NODES=10_000
REFERENCE_RE=re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
PROFILE_ID_RE=re.compile(r"^provider-profile:[a-z0-9][a-z0-9._-]{2,95}$")
CHILD_ID_RE=re.compile(r"^STUDIO-009P-[A-Z0-9][A-Z0-9-]{0,31}$")
EVIDENCE_ID_RE=re.compile(r"^connected-validation:[a-z0-9][a-z0-9._-]{2,95}$")
DIGEST_RE=re.compile(r"^sha256:[0-9a-f]{64}$"); UTC_RE=re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
FORBIDDEN_SECRET_KEYS={"secret","secret_value","credential_value","token","access_token","refresh_token","password","private_key","api_key","authorization","cookie","session"}
SECRET_PATTERNS=(re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"))
FIELDS={"schema_version","connected_validation_id","provider_profile_id","provider_child_id","provider_model_ref","transport_ref","credential_profile_ref","v_contract_ref","data_classification","max_request_bytes","max_output_bytes","request_count","concurrency","retry_count","model_identity_verified","transport_identity_verified","quota_evidence_ref","spend_amount","currency","paid_fallback_allowed","kill_switch_evidence_ref","revocation_evidence_ref","connected_qa_ref","connected_review_ref","owner_disposition_ref","validated_at","as_of","canonical_digest"}
SAFE_MESSAGES={
 "EXTRA_FIELD":"input contains unknown fields","MISSING_FIELD":"input is missing required fields","INVALID_TYPE":"input has invalid type","INVALID_FORMAT":"input has invalid format","INVALID_TIME":"input contains invalid chronology","INPUT_ENCODING":"input contains invalid Unicode","INPUT_NUMBER":"non-finite numbers are forbidden","INPUT_SIZE":"input exceeds the accepted byte limit","STRUCTURE_LIMIT":"input structure exceeds validation limits","DUPLICATE_JSON_KEY":"JSON contains duplicate object keys","DIGEST_MISMATCH":"canonical digest does not match","SECRET_MATERIAL":"secret material is forbidden in this interface","PUBLIC_ONLY":"initial connected validation is PUBLIC/SYNTHETIC only","REQUEST_LIMIT":"connected smoke exceeds request limit","CONCURRENCY_LIMIT":"connected smoke concurrency must equal one","RETRY_LIMIT":"automatic retry must equal zero","IDENTITY_UNVERIFIED":"provider transport/model identity evidence is incomplete","NONZERO_SPEND":"connected validation requires observed spend zero","PAID_FALLBACK":"paid fallback is forbidden","MISSING_V_CONTRACT":"provider-specific V-contract authority is required","MISSING_KILL_REVOKE":"kill-switch and revocation evidence are required","MISSING_CONNECTED_QA":"connected QA evidence is required","MISSING_CONNECTED_REVIEW":"connected Review evidence is required","MISSING_OWNER_DISPOSITION":"Owner disposition evidence is required"}
class ConnectedEvidenceError(ValueError):
    def __init__(self,code): self.code=code; self.safe_message=SAFE_MESSAGES.get(code,"connected evidence rejected"); super().__init__(self.safe_message)
def _fail(c): raise ConnectedEvidenceError(c)
def canonical_json_bytes(v):
    try:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except RecursionError:_fail("STRUCTURE_LIMIT")
    except (UnicodeEncodeError,ValueError,TypeError):_fail("INPUT_ENCODING")
def canonical_digest(v):
    m=copy.deepcopy(v);m.pop("canonical_digest",None);return "sha256:"+hashlib.sha256(canonical_json_bytes(m)).hexdigest()
def _walk(v):
    s=[(None,v,0)];n=0
    while s:
        k,c,d=s.pop();n+=1
        if n>MAX_STRUCTURE_NODES or d>MAX_STRUCTURE_DEPTH:_fail("STRUCTURE_LIMIT")
        yield k,c
        if isinstance(c,dict):s.extend((kk,vv,d+1) for kk,vv in reversed(list(c.items())))
        elif isinstance(c,list):s.extend((None,vv,d+1) for vv in reversed(c))
def _preflight(v):
    raw=canonical_json_bytes(v)
    if len(raw)>MAX_INPUT_BYTES:_fail("INPUT_SIZE")
    for k,c in _walk(v):
        if k is not None:
            try:k.encode("utf-8")
            except UnicodeEncodeError:_fail("INPUT_ENCODING")
            if k.casefold() in FORBIDDEN_SECRET_KEYS:_fail("SECRET_MATERIAL")
        if isinstance(c,str):
            try:c.encode("utf-8")
            except UnicodeEncodeError:_fail("INPUT_ENCODING")
            if any(p.search(c) for p in SECRET_PATTERNS):_fail("SECRET_MATERIAL")
        elif isinstance(c,float) and not math.isfinite(c):_fail("INPUT_NUMBER")
def load_json_document(text):
    if not isinstance(text,str):_fail("INVALID_TYPE")
    try:raw=text.encode("utf-8")
    except UnicodeEncodeError:_fail("INPUT_ENCODING")
    if len(raw)>MAX_INPUT_BYTES:_fail("INPUT_SIZE")
    def hook(pairs):
        d={}
        for k,v in pairs:
            if k in d:_fail("DUPLICATE_JSON_KEY")
            d[k]=v
        return d
    try:v=json.loads(text,object_pairs_hook=hook,parse_constant=lambda _:_fail("INPUT_NUMBER"))
    except ConnectedEvidenceError:raise
    except (json.JSONDecodeError,ValueError,UnicodeDecodeError):_fail("INVALID_FORMAT")
    if not isinstance(v,dict):_fail("INVALID_TYPE")
    _preflight(v);return v
def _ref(v,nullable=False):
    if v is None and nullable:return None
    if not isinstance(v,str) or not REFERENCE_RE.fullmatch(v) or "://" in v:_fail("INVALID_FORMAT")
    return v
def _utc(v):
    if not isinstance(v,str) or not UTC_RE.fullmatch(v):_fail("INVALID_TIME")
    try:return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:_fail("INVALID_TIME")
def validate_connected_validation(record, *, initial_smoke=True):
    _preflight(record);before=canonical_json_bytes(copy.deepcopy(record))
    if not isinstance(record,dict):_fail("INVALID_TYPE")
    keys=set(record)
    if FIELDS-keys:_fail("MISSING_FIELD")
    if keys-FIELDS:_fail("EXTRA_FIELD")
    v=record
    if v["schema_version"]!=SCHEMA_VERSION:_fail("INVALID_FORMAT")
    if not isinstance(v["connected_validation_id"],str) or not EVIDENCE_ID_RE.fullmatch(v["connected_validation_id"]):_fail("INVALID_FORMAT")
    if not isinstance(v["provider_profile_id"],str) or not PROFILE_ID_RE.fullmatch(v["provider_profile_id"]):_fail("INVALID_FORMAT")
    if not isinstance(v["provider_child_id"],str) or not CHILD_ID_RE.fullmatch(v["provider_child_id"]):_fail("INVALID_FORMAT")
    model=_ref(v["provider_model_ref"]); transport=_ref(v["transport_ref"]); credential=_ref(v["credential_profile_ref"]); vc=_ref(v["v_contract_ref"],nullable=True)
    if vc is None:_fail("MISSING_V_CONTRACT")
    if v["data_classification"] not in {"PUBLIC","INTERNAL","RESTRICTED"}:_fail("INVALID_FORMAT")
    if initial_smoke and v["data_classification"]!="PUBLIC":_fail("PUBLIC_ONLY")
    for key in ("max_request_bytes","max_output_bytes"):
        if isinstance(v[key],bool) or not isinstance(v[key],int) or v[key]<1 or v[key]>2_097_152:_fail("INVALID_TYPE")
    if isinstance(v["request_count"],bool) or not isinstance(v["request_count"],int) or not (1<=v["request_count"]<=3):_fail("REQUEST_LIMIT")
    if v["concurrency"]!=1 or isinstance(v["concurrency"],bool):_fail("CONCURRENCY_LIMIT")
    if v["retry_count"]!=0 or isinstance(v["retry_count"],bool):_fail("RETRY_LIMIT")
    if v["model_identity_verified"] is not True or v["transport_identity_verified"] is not True:_fail("IDENTITY_UNVERIFIED")
    quota=_ref(v["quota_evidence_ref"],nullable=True)
    if isinstance(v["spend_amount"],bool) or v["spend_amount"]!=0:_fail("NONZERO_SPEND")
    if not isinstance(v["currency"],str) or not re.fullmatch(r"^[A-Z]{3}$",v["currency"]):_fail("INVALID_FORMAT")
    if v["paid_fallback_allowed"] is not False:_fail("PAID_FALLBACK")
    kill=_ref(v["kill_switch_evidence_ref"],nullable=True); revoke=_ref(v["revocation_evidence_ref"],nullable=True)
    if kill is None or revoke is None:_fail("MISSING_KILL_REVOKE")
    qa=_ref(v["connected_qa_ref"],nullable=True)
    if qa is None:_fail("MISSING_CONNECTED_QA")
    review=_ref(v["connected_review_ref"],nullable=True)
    if review is None:_fail("MISSING_CONNECTED_REVIEW")
    owner=_ref(v["owner_disposition_ref"],nullable=True)
    if owner is None:_fail("MISSING_OWNER_DISPOSITION")
    validated=_utc(v["validated_at"]); as_of=_utc(v["as_of"])
    if validated>as_of:_fail("INVALID_TIME")
    d=v["canonical_digest"]
    if not isinstance(d,str) or not DIGEST_RE.fullmatch(d):_fail("INVALID_FORMAT")
    if d!=canonical_digest(v):_fail("DIGEST_MISMATCH")
    if canonical_json_bytes(record)!=before:_fail("INVALID_FORMAT")
    return {"connected_validation_id":v["connected_validation_id"],"provider_profile_id":v["provider_profile_id"],"provider_child_id":v["provider_child_id"],"provider_model_ref":model,"transport_ref":transport,"credential_profile_ref":credential,"v_contract_ref":vc,"data_classification":v["data_classification"],"request_count":v["request_count"],"concurrency":1,"retry_count":0,"spend_amount":0,"quota_evidence_ref":quota,"connected_validation_digest":d,"decision":"ACCEPTED"}
