import numpy as np
from typing import Annotated
from pydantic import BaseModel, Field


class StdDev:
    def __init__(self):
        self.values = []

    def step(self, value):
        self.values.append(value)

    def finalize(self):
        stddev = float(np.std(self.values, ddof=1))
        return stddev if not np.isnan(stddev) else 0


class RtcAttempt(BaseModel):
    target: Annotated[int, Field(ge=1)]
    darts_thrown: Annotated[int, Field(ge=1)]


def validate_rtc_data(data: list[dict]):
    return [RtcAttempt(**attempt) for attempt in data]
