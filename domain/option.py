from dataclasses import dataclass


@dataclass(slots=True)
class Options:
    enable_snap: bool
    record_snapped_positions_only: bool

    @classmethod
    def create_default(cls):
        return cls(
            enable_snap=True,
            record_snapped_positions_only=True,
        )
