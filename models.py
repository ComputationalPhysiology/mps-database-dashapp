from __future__ import annotations
from typing import Any
from pydantic import BaseModel, root_validator, Field


class UnchoppedData(BaseModel):
    background: list[float] = Field(default_factory=list)
    original_pacing: list[float] = Field(default_factory=list)
    original_times: list[float] = Field(default_factory=list)
    original_trace: list[float] = Field(default_factory=list)
    pacing: list[float] = Field(default_factory=list)
    sliced_filtered_pacing: list[float] = Field(default_factory=list)
    sliced_filtered_times: list[float] = Field(default_factory=list)
    sliced_filtered_trace: list[float] = Field(default_factory=list)
    times: list[float] = Field(default_factory=list)
    trace: list[float] = Field(default_factory=list)


class ChoppedData(BaseModel):
    pacing_all: list[float] = Field(default_factory=list)
    time_all: list[float] = Field(default_factory=list)
    trace_all: list[float] = Field(default_factory=list)
    pacing_1std: list[float] = Field(default_factory=list)
    time_1std: list[float] = Field(default_factory=list)
    trace_1std: list[float] = Field(default_factory=list)
    extra: dict[str, Any] = Field(default_factory=dict)

    @root_validator(pre=True)
    def build_extra(cls, values: dict[str, Any]) -> dict[str, Any]:
        all_required_field_names = {
            field.alias for field in cls.__fields__.values() if field.alias != "extra"
        }  # to support alias

        extra: dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)
        values["extra"] = extra
        return values


class ChoppedArray(BaseModel):
    t: list[list[float]] = Field(default_factory=list)
    y: list[list[float]] = Field(default_factory=list)


class MotionArray(BaseModel):
    average_time: list[float] = Field(default_factory=list)
    average_trace: list[float] = Field(default_factory=list)
    background: list[float] = Field(default_factory=list)
    chopped: ChoppedArray = Field(default_factory=ChoppedArray)
    chopped_aligned: ChoppedArray = Field(default_factory=ChoppedArray)
    corrected: list[float] = Field(default_factory=list)
    original: list[float] = Field(default_factory=list)


class MotionTracking(BaseModel):
    displacement_norm: MotionArray = Field(default_factory=MotionArray)
    displacement_x: MotionArray = Field(default_factory=MotionArray)
    displacement_y: MotionArray = Field(default_factory=MotionArray)
    pacing: list[float] = Field(default_factory=list)
    time: list[float] = Field(default_factory=list)
    velocity_norm: MotionArray = Field(default_factory=MotionArray)
    velocity_x: MotionArray = Field(default_factory=MotionArray)
    velocity_y: MotionArray = Field(default_factory=MotionArray)

    def get_motion_array(self, key: str) -> MotionArray:
        assert key in [
            "displacement_norm",
            "displacement_x",
            "displacement_y",
            "velocity_norm",
            "velocity_x",
            "velocity_y",
        ]
        return getattr(self, key)


class MPSData(BaseModel):
    analysis_settings: dict[str, Any] = Field(default_factory=dict)
    chopped_data: ChoppedData = Field(default_factory=ChoppedData)
    analysis_tags: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)
    current_tag: str = ""
    features: dict[str, float] = Field(default_factory=dict)
    id: int = -1
    intervals: list[Any]
    motion_features: dict[str, float] = Field(default_factory=dict)
    motion_tracking: MotionTracking = Field(default_factory=MotionTracking)
    motion_tracking_settings: dict[str, Any] = Field(default_factory=dict)
    plot_label_values: dict[str, Any] = Field(default_factory=dict)
    plot_labels: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    trace_quality: str | None = None
    unchopped_data: UnchoppedData = Field(default_factory=UnchoppedData)
