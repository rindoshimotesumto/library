from dataclasses import dataclass


@dataclass(slots=True)
class Authors:
    author_name: str
