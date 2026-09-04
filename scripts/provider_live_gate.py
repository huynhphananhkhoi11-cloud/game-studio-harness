#!/usr/bin/env python3
"""Deterministic STUDIO-009R live-state and worker-mode gate.

Offline metadata validation only. This module performs no provider, network,
credential-store, routing, repository-write, subprocess, or Unity activity.
"""
from __future__ import annotations
import copy, hashlib, json, math, re
from datetime import datetime, timezone
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
MAX_INPUT_BYTES = 1_048_576
MAX_STRUCTURE_DEPTH = 32
MAX_STRUCTURE_NODES = 10_000
CLASSIFICATIONS = {"PUBLIC","INTERNAL","RESTRICTED"}
LIVE_STATES = {"DISABLED","LIVE_VALIDATION_READY","LIVE_VALIDATED","LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER","ROUTING_ELIGIBLE","PAUSED","REVOKED"}
REFERENCE_RE = re.compile(r"^[a-z][a-z0-9-]{1,31}:[A-Za-z0-9._/-]{1,160}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
UTC_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")
LIVE_ID_RE = re.compile(r"^provider-live-state:[a-z0-9][a-z0-9._-]{2,95}$")
PROFILE_ID_RE = re.compile(r"^provider-profile:[a-z0-9][a-z0-9._-]{2,95}$")
CHILD_ID_RE = re.compile(r"^STUDIO-009P-[A-Z0-9][A-Z0-9-]{0,31}$")
WORKER_ID_RE = re.compile(r"^worker-policy:[a-z0-9][a-z0-9._-]{2,95}$")
SAFE_PATH_RE = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$|^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*/\*\*$")
FORBIDDEN_SECRET_KEYS = {"secret","secret_value","credential_value","token","access_token","refresh_token","password","passwd","private_key","api_key","authorization","cookie","session"}
SECRET_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
)
LIVE_FIELDS = {
    "schema_version","live_state_id","provider_profile_id","provider_child_id","offline_merge_ref","offline_qa_ref",
    "offline_review_ref","offline_owner_merge_ref","v_contract_ref","connected_validation_ref","routing_authority_ref",
    "state","allowed_data_classifications","money_ceiling","paused_at","revoked_at","as_of","canonical_digest",
}
WORKER_FIELDS = {
    "schema_version","worker_policy_id","provider_profile_id","provider_child_id","mode","work_order_ref","writer_claim_ref",
    "worktree_ref","allowed_paths","repository_write_allowed","direct_main_write_allowed","merge_allowed","deploy_allowed",
    "publish_allowed","secret_access_allowed","arbitrary_tools_allowed","local_mediation_required","money_ceiling","as_of","canonical_digest",
}
SAFE_MESSAGES = {
 "EXTRA_FIELD":"input contains unknown fields","MISSING_FIELD":"input is missing required fields","INVALID_TYPE":"input has an invalid type",
 "INVALID_FORMAT":"input has invalid format","INVALID_ENUM":"input contains an unsupported value","INVALID_TIME":"input contains invalid chronology",
 "INPUT_ENCODING":"input contains invalid Unicode","INPUT_NUMBER":"non-finite numbers are forbidden","INPUT_SIZE":"input exceeds the accepted byte limit",
 "STRUCTURE_LIMIT":"input structure exceeds validation limits","DUPLICATE_JSON_KEY":"JSON contains duplicate object keys","DIGEST_MISMATCH":"canonical digest does not match",
 "SECRET_MATERIAL":"secret material is forbidden in this interface","NONZERO_BUDGET":"live validation requires zero monetary ceiling",
 "OFFLINE_CHILD_NOT_MERGED":"offline provider lifecycle is not durably complete","MISSING_QA_REVIEW_OWNER":"offline QA, Review, and Owner merge evidence are required",
 "MISSING_V_CONTRACT":"provider-specific V-contract authority is required","MISSING_CONNECTED_EVIDENCE":"connected-validation evidence is required",
 "DATA_CLASS_BROADENING":"live data scope exceeds accepted provider scope","ROUTING_BEFORE_009E":"routing eligibility requires later STUDIO-009E authority",
 "PAUSED_PROVIDER":"paused provider is not eligible for promotion","REVOKED_PROVIDER":"revoked provider is not eligible for promotion",
 "INVALID_TRANSITION":"live-state transition skips a required gate","WORKER_AUTHORITY":"worker policy grants unauthorized authority",
 "WRITER_CLAIM_REQUIRED":"bounded worker requires Work Order, writer claim, worktree, and exact paths","UNSAFE_PATH":"worker path is not a safe repository-relative path",
}
class LiveGateError(ValueError):
    def __init__(self, code:str):
        self.code=code; self.safe_message=SAFE_MESSAGES.get(code,"live gate rejected"); super().__init__(self.safe_message)
def _fail(code): raise LiveGateError(code)
def canonical_json_bytes(value):
    try: return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode("utf-8")
    except RecursionError: _fail("STRUCTURE_LIMIT")
    except (UnicodeEncodeError,ValueError,TypeError): _fail("INPUT_ENCODING")
def canonical_digest(value):
    material=copy.deepcopy(value); material.pop("canonical_digest",None)
    return "sha256:"+hashlib.sha256(canonical_json_bytes(material)).hexdigest()
def _walk(value):
    stack=[(None,value,0)]; n=0
    while stack:
        key,child,depth=stack.pop(); n+=1
        if n>MAX_STRUCTURE_NODES or depth>MAX_STRUCTURE_DEPTH: _fail("STRUCTURE_LIMIT")
        yield key,child
        if isinstance(child,dict): stack.extend((k,v,depth+1) for k,v in reversed(list(child.items())))
        elif isinstance(child,list): stack.extend((None,v,depth+1) for v in reversed(child))
def _preflight(value):
    raw=canonical_json_bytes(value)
    if len(raw)>MAX_INPUT_BYTES: _fail("INPUT_SIZE")
    for key,child in _walk(value):
        if key is not None:
            try: key.encode("utf-8")
            except UnicodeEncodeError: _fail("INPUT_ENCODING")
            if key.casefold() in FORBIDDEN_SECRET_KEYS: _fail("SECRET_MATERIAL")
        if isinstance(child,str):
            try: child.encode("utf-8")
            except UnicodeEncodeError: _fail("INPUT_ENCODING")
            if any(p.search(child) for p in SECRET_PATTERNS): _fail("SECRET_MATERIAL")
        elif isinstance(child,float) and not math.isfinite(child): _fail("INPUT_NUMBER")
def load_json_document(text):
    if not isinstance(text,str): _fail("INVALID_TYPE")
    try: raw=text.encode("utf-8")
    except UnicodeEncodeError: _fail("INPUT_ENCODING")
    if len(raw)>MAX_INPUT_BYTES: _fail("INPUT_SIZE")
    def hook(pairs):
        out={}
        for k,v in pairs:
            if k in out: _fail("DUPLICATE_JSON_KEY")
            out[k]=v
        return out
    try: value=json.loads(text,object_pairs_hook=hook,parse_constant=lambda _: _fail("INPUT_NUMBER"))
    except LiveGateError: raise
    except (json.JSONDecodeError,ValueError,UnicodeDecodeError): _fail("INVALID_FORMAT")
    if not isinstance(value,dict): _fail("INVALID_TYPE")
    _preflight(value); return value
def _exact(value,fields):
    if not isinstance(value,dict): _fail("INVALID_TYPE")
    keys=set(value)
    if fields-keys: _fail("MISSING_FIELD")
    if keys-fields: _fail("EXTRA_FIELD")
    return value
def _ref(v,nullable=False):
    if v is None and nullable: return None
    if not isinstance(v,str) or not REFERENCE_RE.fullmatch(v) or "://" in v: _fail("INVALID_FORMAT")
    return v
def _utc(v,nullable=False):
    if v is None and nullable: return None
    if not isinstance(v,str) or not UTC_RE.fullmatch(v): _fail("INVALID_TIME")
    try: return datetime.strptime(v,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError: _fail("INVALID_TIME")
def _sorted_classes(v):
    if not isinstance(v,list) or not v or any(not isinstance(x,str) for x in v): _fail("INVALID_TYPE")
    if v!=sorted(v) or len(v)!=len(set(v)): _fail("INVALID_FORMAT")
    if not set(v).issubset(CLASSIFICATIONS): _fail("INVALID_ENUM")
    return tuple(v)
def _verify_digest(v):
    d=v.get("canonical_digest")
    if not isinstance(d,str) or not DIGEST_RE.fullmatch(d): _fail("INVALID_FORMAT")
    if d!=canonical_digest(v): _fail("DIGEST_MISMATCH")
def validate_live_state(record, *, parent_allowed_data_classifications=None):
    _preflight(record); before=canonical_json_bytes(copy.deepcopy(record)); v=_exact(record,LIVE_FIELDS)
    if v["schema_version"]!=SCHEMA_VERSION: _fail("INVALID_ENUM")
    if not isinstance(v["live_state_id"],str) or not LIVE_ID_RE.fullmatch(v["live_state_id"]): _fail("INVALID_FORMAT")
    if not isinstance(v["provider_profile_id"],str) or not PROFILE_ID_RE.fullmatch(v["provider_profile_id"]): _fail("INVALID_FORMAT")
    if not isinstance(v["provider_child_id"],str) or not CHILD_ID_RE.fullmatch(v["provider_child_id"]): _fail("INVALID_FORMAT")
    state=v["state"]
    if state not in LIVE_STATES: _fail("INVALID_ENUM")
    refs={k:_ref(v[k],nullable=True) for k in ("offline_merge_ref","offline_qa_ref","offline_review_ref","offline_owner_merge_ref","v_contract_ref","connected_validation_ref","routing_authority_ref")}
    classes=_sorted_classes(v["allowed_data_classifications"])
    if parent_allowed_data_classifications is not None and not set(classes).issubset(set(parent_allowed_data_classifications)): _fail("DATA_CLASS_BROADENING")
    if isinstance(v["money_ceiling"],bool) or v["money_ceiling"]!=0: _fail("NONZERO_BUDGET")
    as_of=_utc(v["as_of"]); paused=_utc(v["paused_at"],nullable=True); revoked=_utc(v["revoked_at"],nullable=True)
    if paused and paused>as_of or revoked and revoked>as_of: _fail("INVALID_TIME")
    if state in {"LIVE_VALIDATION_READY","LIVE_VALIDATED","LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER","ROUTING_ELIGIBLE","PAUSED","REVOKED"} and refs["offline_merge_ref"] is None: _fail("OFFLINE_CHILD_NOT_MERGED")
    if state in {"LIVE_VALIDATION_READY","LIVE_VALIDATED","LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER","ROUTING_ELIGIBLE","PAUSED","REVOKED"} and any(refs[k] is None for k in ("offline_qa_ref","offline_review_ref","offline_owner_merge_ref")): _fail("MISSING_QA_REVIEW_OWNER")
    if state in {"LIVE_VALIDATED","LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER","ROUTING_ELIGIBLE"}:
        if refs["v_contract_ref"] is None: _fail("MISSING_V_CONTRACT")
        if refs["connected_validation_ref"] is None: _fail("MISSING_CONNECTED_EVIDENCE")
    if state=="ROUTING_ELIGIBLE" and refs["routing_authority_ref"] is None: _fail("ROUTING_BEFORE_009E")
    if state=="PAUSED" and paused is None: _fail("PAUSED_PROVIDER")
    if state=="REVOKED" and revoked is None: _fail("REVOKED_PROVIDER")
    _verify_digest(v)
    if canonical_json_bytes(record)!=before: _fail("INVALID_FORMAT")
    return {"live_state_id":v["live_state_id"],"provider_profile_id":v["provider_profile_id"],"provider_child_id":v["provider_child_id"],"state":state,"allowed_data_classifications":classes,"money_ceiling":0,"live_state_digest":v["canonical_digest"],**refs}
def validate_worker_mode_policy(record):
    _preflight(record); before=canonical_json_bytes(copy.deepcopy(record)); v=_exact(record,WORKER_FIELDS)
    if v["schema_version"]!=SCHEMA_VERSION: _fail("INVALID_ENUM")
    if not isinstance(v["worker_policy_id"],str) or not WORKER_ID_RE.fullmatch(v["worker_policy_id"]): _fail("INVALID_FORMAT")
    _ref(v["provider_profile_id"]); child=v["provider_child_id"]
    if not isinstance(child,str) or not CHILD_ID_RE.fullmatch(child): _fail("INVALID_FORMAT")
    mode=v["mode"]
    if mode not in {"LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER"}: _fail("INVALID_ENUM")
    for key in ("direct_main_write_allowed","merge_allowed","deploy_allowed","publish_allowed","secret_access_allowed","arbitrary_tools_allowed"):
        if v[key] is not False: _fail("WORKER_AUTHORITY")
    if v["local_mediation_required"] is not True: _fail("WORKER_AUTHORITY")
    if isinstance(v["money_ceiling"],bool) or v["money_ceiling"]!=0: _fail("NONZERO_BUDGET")
    _utc(v["as_of"])
    paths=v["allowed_paths"]
    if not isinstance(paths,list) or len(paths)!=len(set(paths)) or paths!=sorted(paths): _fail("INVALID_FORMAT")
    for path in paths:
        if not isinstance(path,str) or not SAFE_PATH_RE.fullmatch(path) or path.startswith(("/","../")) or "/../" in path: _fail("UNSAFE_PATH")
    wo=_ref(v["work_order_ref"],nullable=True); wc=_ref(v["writer_claim_ref"],nullable=True); wt=_ref(v["worktree_ref"],nullable=True)
    if mode=="LIVE_SHADOW_WORKER":
        if v["repository_write_allowed"] is not False or wo is not None or wc is not None or wt is not None or paths: _fail("WORKER_AUTHORITY")
    else:
        if v["repository_write_allowed"] is not True or wo is None or wc is None or wt is None or not paths: _fail("WRITER_CLAIM_REQUIRED")
    _verify_digest(v)
    if canonical_json_bytes(record)!=before: _fail("INVALID_FORMAT")
    return {"worker_policy_id":v["worker_policy_id"],"provider_profile_id":v["provider_profile_id"],"provider_child_id":child,"mode":mode,"allowed_paths":tuple(paths),"repository_write_allowed":v["repository_write_allowed"],"worker_policy_digest":v["canonical_digest"]}
def plan_transition(current, target, *, connected_evidence=None, worker_policy=None, routing_authority=False):
    if not isinstance(current,dict): _fail("INVALID_TYPE")
    state=current.get("state")
    if state=="REVOKED": _fail("REVOKED_PROVIDER")
    if state=="PAUSED": _fail("PAUSED_PROVIDER")
    allowed={
      "DISABLED":{"LIVE_VALIDATION_READY","PAUSED","REVOKED"},
      "LIVE_VALIDATION_READY":{"LIVE_VALIDATED","PAUSED","REVOKED"},
      "LIVE_VALIDATED":{"LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER","PAUSED","REVOKED"},
      "LIVE_SHADOW_WORKER":{"LIVE_BOUNDED_WORKER","PAUSED","REVOKED"},
      "LIVE_BOUNDED_WORKER":{"ROUTING_ELIGIBLE","PAUSED","REVOKED"},
    }
    if target not in allowed.get(state,set()): _fail("INVALID_TRANSITION")
    if target=="LIVE_VALIDATED" and connected_evidence is None: _fail("MISSING_CONNECTED_EVIDENCE")
    if target in {"LIVE_SHADOW_WORKER","LIVE_BOUNDED_WORKER"}:
        if worker_policy is None or worker_policy.get("mode")!=target: _fail("WORKER_AUTHORITY")
    if target=="ROUTING_ELIGIBLE" and not routing_authority: _fail("ROUTING_BEFORE_009E")
    return {"from":state,"to":target,"decision":"ALLOWED"}
