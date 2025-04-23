from typing import Set
from .components import FunctionalDependency, Attribute, Relvar


def closure(attributes: Set[Attribute], functional_dependencies: Set[FunctionalDependency]) -> Set[Attribute]:
    closure_set = set(attributes)
    changed = True
    while changed:
        changed = False
        for fd in functional_dependencies:
            if fd.determinant.issubset(closure_set):
                if not fd.dependant.issubset(closure_set):
                    closure_set.update(fd.dependant)
                    changed = True
    return closure_set


def is_superkey(attributes: Set[Attribute], heading: Set[Attribute], functional_dependencies: Set[FunctionalDependency]) -> bool:
    return closure(attributes, functional_dependencies) >= heading


def is_key(attributes: Set[Attribute], heading: Set[Attribute], functional_dependencies: Set[FunctionalDependency]) -> bool:
    if not is_superkey(attributes, heading, functional_dependencies):
        return False
    for attr in attributes:
        subset = attributes - {attr}
        if is_superkey(subset, heading, functional_dependencies):
            return False
    return True


def is_relvar_in_bcnf(relvar: Relvar):
    for fd in relvar.functional_dependencies:
        if not fd.is_trivial() and not is_superkey(fd.determinant, relvar.heading, relvar.functional_dependencies):
            return False
    return True


def is_relvar_in_4nf(relvar: Relvar):
    for mvd in relvar.multivalued_dependencies:
        if not mvd.is_trivial(relvar.heading) and not is_superkey(mvd.determinant, relvar.heading, relvar.functional_dependencies):
            return False
    return True
