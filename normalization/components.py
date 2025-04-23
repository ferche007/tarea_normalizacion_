
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Set
from .exceptions import InvalidDependency, InvalidExpression


@dataclass(frozen=True)
class Attribute:
    """
    Represents an attribute for a relvar in terms of the relational model design theory.
    Each attribute has a name and is immutable.

    Attributes:
        name (str): The name of the attribute.
    """
    name: str

    def __str__(self) -> str:
        return self.name


class Dependency(ABC):
    """Base abstract class for functional and multivalued dependencies."""
    _CAPTURE_EXPRESSION: str
    _SEPARATOR: str

    def __init__(self, expression: str):
        if not isinstance(expression, str):
            raise InvalidExpression(f"Expression must be a string, got {type(expression).__name__}.")

        expression = expression.replace(" ", "")

        if not self._is_expression_valid(expression):
            raise InvalidExpression("Provided string does not represent a functional dependency.")

        determinant_expression, dependant_expression = expression.split(self._SEPARATOR)
        self.determinant = Dependency._get_set_from_expression(determinant_expression)
        self.dependant = Dependency._get_set_from_expression(dependant_expression)

    def __str__(self) -> str:
        determinant_expression = f"{{{', '.join(attribute.name for attribute in self.determinant)}}}"
        dependent_expression = f"{{{', '.join(attribute.name for attribute in self.dependant)}}}"
        return f"{determinant_expression} {self._SEPARATOR} {dependent_expression}"

    def __repr__(self) -> str:
        return self.__str__()

    def _is_expression_valid(self, expression: str) -> bool:
        clean_expression = expression.replace(" ", '')
        return bool(re.fullmatch(self._CAPTURE_EXPRESSION, clean_expression))

    @staticmethod
    def _get_set_from_expression(expression: str) -> Set[Attribute]:
        expression = expression.replace(" ", '')
        expression = expression.strip("{}")
        return set(Attribute(name) for name in expression.split(","))

    @abstractmethod
    def is_trivial(self, *args, **kwargs) -> bool:
        return self.dependant.issubset(self.determinant)
        raise NotImplementedError()


class FunctionalDependency(Dependency):
    """Class for functional dependencies."""
    _CAPTURE_EXPRESSION = r"\{[A-z]+(?:,[A-z]+)*\}->\{[A-z]+(?:,[A-z]+)*\}"
    _SEPARATOR = "->"

    def is_trivial(self) -> bool:
        return self.dependant.issubset(self.determinant)


class MultivaluedDependency(Dependency):
    """Class for multivalued dependencies."""
    _CAPTURE_EXPRESSION = r"\{[A-z]+(?:,[A-z]+)*\}->->\{[A-z]+(?:,[A-z]+)*\}"
    _SEPARATOR = "->->"

    def is_trivial(self, heading: Set[Attribute]) -> bool:
        return self.dependant.issubset(self.determinant) or self.determinant.union(self.dependant) == heading


class Relvar:
    """Class for relvars."""
    def __init__(self, heading: [str], functional_dependencies: [FunctionalDependency] = None, multivalued_dependencies: [MultivaluedDependency] = None):
        self.heading = set(Attribute(name) for name in heading)
        self.functional_dependencies = set()
        self.multivalued_dependencies = set()

        if functional_dependencies:
            for fd in functional_dependencies:
                self.add_functional_dependency(fd)

        if multivalued_dependencies:
            for mvd in multivalued_dependencies:
                self.add_multivalued_dependency(mvd)

    def __str__(self) -> str:
        return f"{{{', '.join(attribute.name for attribute in self.heading)}}}"

    def __repr__(self) -> str:
        return f"heading={repr(self.heading)}, functional_dependencies={repr(self.functional_dependencies)}"

    def _validate_dependency(self, dependency: Dependency):
        for attribute in dependency.determinant | dependency.dependant:
            if attribute not in self.heading:
                raise InvalidDependency(f"{attribute} is not contained in relvar's heading.")

    def add_functional_dependency(self, functional_dependency: FunctionalDependency):
        self._validate_dependency(functional_dependency)
        self.functional_dependencies.add(functional_dependency)

    def add_multivalued_dependency(self, multivalued_dependency: MultivaluedDependency):
        self._validate_dependency(multivalued_dependency)
        self.multivalued_dependencies.add(multivalued_dependency)
