from enum import Enum
from typing import Union

from rafiki.model import Knobs

class AdvisorType(Enum):
    FIXED = 'FIXED'
    BAYES_OPT_WITH_PARAM_SHARING = 'BAYES_OPT_WITH_PARAM_SHARING'
    BAYES_OPT = 'BAYES_OPT'
    RANDOM = 'RANDOM'
    ENAS = 'ENAS'

class ParamsType(Enum):
    LOCAL_RECENT = 'LOCAL_RECENT'
    LOCAL_BEST = 'LOCAL_BEST'
    GLOBAL_RECENT = 'GLOBAL_RECENT'
    GLOBAL_BEST = 'GLOBAL_BEST'
    NONE = 'NONE'

class Jsonable():
    @classmethod
    def from_jsonable(cls, jsonable) -> object:
        return cls(**jsonable)

    def to_jsonable(self) -> any:
        jsonable = self.__dict__.copy()

        # Convert all nested jsonables & enums
        for (name, value) in jsonable.items():
            if isinstance(value, Jsonable):
                jsonable[name] = value.to_jsonable()
            elif isinstance(value, Enum):
                jsonable[name] = value.value

        return jsonable

    def __str__(self):
        return str(self.to_jsonable())

class Proposal(Jsonable):
    def __init__(self, 
                trial_no: int, # Trial no.
                knobs: Knobs, # Knobs for this trial
                params_type: ParamsType = ParamsType.NONE, # Parameters to use for this trial
                to_eval=True, # Whether the model should be evaluated
                to_cache_params=False, # Whether this trial's parameters should be cached
                to_save_params=True, # Whether this trial's parameters should be persisted
                meta: dict = None, # Extra metadata associated with proposal
                trial_id: str = None): # ID of trial associated with proposal, to be set by worker
        self.trial_no = trial_no
        self.knobs = knobs
        self.params_type = ParamsType(params_type)
        self.to_eval = to_eval
        self.to_cache_params = to_cache_params
        self.to_save_params = to_save_params
        self.meta = meta or {}
        self.trial_id = trial_id 

class TrialResult(Jsonable):
    def __init__(self, 
                proposal: Proposal, 
                score: Union[float, None] = None): # Score for the proposal
        self.proposal = proposal if isinstance(proposal, Proposal) else Proposal(**proposal)
        self.score = score