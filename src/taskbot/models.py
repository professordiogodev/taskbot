from dataclasses import asdict, dataclass

PRIORITIES = ("low", "med", "high")


@dataclass
class Task:
    id: int
    text: str
    done: bool = False
    priority: str = "med"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            id=data["id"],
            text=data["text"],
            done=data.get("done", False),
            priority=data.get("priority", "med"),
        )
