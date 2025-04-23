# ITAM Primavera 2025 - Tarea de Normalización

---

## Configuración

Este proyecto no tiene dependencias adicionales de Python, por lo que no es 
necesario crear un ambiente virtual. Está desarollado y probado con Python 3.13,
pero debe funcionar con 3.8 o superior.

## Estructura

SUPOSICIONES REALIZADAS

- Las expresiones de dependencias funcionales y multivaluadas siguen la notación:
  - {A,B}->{C} para dependencias funcionales
  - {A}->->{B} para dependencias multivaluadas
- Todos los atributos se representan como strings únicos y válidos (sin espacios).
- Los objetos Attribute son inmutables y se comparan por nombre.
- El encabezado (heading) de una relación es un conjunto de strings que se convierten internamente en objetos Attribute.
- Las dependencias funcionales y multivaluadas se validan y transforman al ser construidas.
- Las funciones de verificación de formas normales asumen que las dependencias ya están correctamente normalizadas sintácticamente.

EJEMPLOS DE USO DE LAS FUNCIONES

1. Cálculo de la cerradura

from normalization.algorithms import closure
from normalization.components import Attribute, FunctionalDependency

A = Attribute("A")
B = Attribute("B")
C = Attribute("C")

fds = {
    FunctionalDependency("{A}->{B}"),
    FunctionalDependency("{B}->{C}")
}

resultado = closure({A}, fds)
print({attr.name for attr in resultado})  # {'A', 'B', 'C'}

2. Verificación de superllave y llave

from normalization.algorithms import is_superkey, is_key

heading = {A, B, C}
print(is_superkey({A}, heading, fds))  # True
print(is_key({A}, heading, fds))       # True

3. Verificación de forma normal de Boyce-Codd (BCNF)

from normalization.components import Relvar

rel = Relvar(["A", "B", "C"], functional_dependencies=list(fds))
print(is_relvar_in_bcnf(rel))  # True

4. Verificación de cuarta forma normal (4NF)

from normalization.components import MultivaluedDependency

mvd = MultivaluedDependency("{A}->->{C}")
rel4 = Relvar(
    ["A", "B", "C"],
    functional_dependencies=list(fds),
    multivalued_dependencies=[mvd]
)
print(is_relvar_in_4nf(rel4))  # Depende de si A es superllave
