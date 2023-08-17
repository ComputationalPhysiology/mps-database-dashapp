from enum import StrEnum, auto


class TraceTypes(StrEnum):
    fluorescence = auto()
    displacement_norm = auto()
    displacement_x = auto()
    displacement_y = auto()
    velocity_norm = auto()
    velocity_x = auto()
    velocity_y = auto()

    @classmethod
    def from_string(cls, selected_trace: str):
        try:
            value = cls[selected_trace]
        except KeyError as e:
            msg = f"Invalid trace type {selected_trace}. " f"Expected one of {tuple(cls.__members__.keys())}"
            raise RuntimeError(msg) from e
        return value


class PlotTypes(StrEnum):
    original = auto()
    original_w_pacing = auto()
    average = auto()
    average_normalized = auto()
    chopped = auto()
    chopped_aligned = auto()
    corrected_and_background = auto()

    @classmethod
    def from_string(cls, plot_type: str):
        try:
            value = cls[plot_type]
        except KeyError as e:
            msg = f"Invalid plot type {plot_type}. " f"Expected one of {tuple(cls.__members__.keys())}"
            raise RuntimeError(msg) from e
        return value


# class PlotTypes(StrEnum):
#     original = auto()
#     pacing = auto()
#     chopped = auto()
#     chopped_aligned = auto()
#     background = auto()
#     corrected = auto()
#     average = auto()

#     @classmethod
#     def from_string(cls, plot_type: str):
#         try:
#             value = cls[plot_type]
#         except KeyError as e:
#             msg = (
#                 f"Invalid plot type {plot_type}. "
#                 f"Expected one of {tuple(cls.__members__.keys())}"
#             )
#             raise RuntimeError(msg) from e
#         return value
