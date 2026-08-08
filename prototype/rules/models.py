from dataclasses import dataclass, field, asdict
from typing import Any
@dataclass
class DomainEvent: type:str; payload:dict[str,Any]=field(default_factory=dict)
@dataclass
class StateDelta: changes:dict[str,Any]=field(default_factory=dict); events:list[DomainEvent]=field(default_factory=list); telemetry:list[dict[str,Any]]=field(default_factory=list); trace:list[str]=field(default_factory=list)
@dataclass
class PlayerState:
    schema_version:str; day:int; slot:int; seed:int; stats:dict[str,Any]; relations:dict[str,int]; skills:dict[str,dict[str,Any]]; jobs:dict[str,dict[str,Any]]; items:dict[str,int]; quests:dict[str,str]; obligations:list[dict[str,Any]]; flags:dict[str,Any]; action_history:list[dict[str,Any]]=field(default_factory=list); drawn_opportunities:list[str]=field(default_factory=list)
    def derived(self): return {'stress_internal':100-int(self.stats.get('morale',0))}
    def to_dict(self): return asdict(self)
