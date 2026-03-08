"""Base types for OpenEnv environments."""

from pydantic import BaseModel, ConfigDict


class Action(BaseModel):
    model_config = ConfigDict()


class Observation(BaseModel):
    model_config = ConfigDict()


class State(BaseModel):
    model_config = ConfigDict()
