from normalization.components import Relvar, FunctionalDependency, MultivaluedDependency
from normalization.components import Attribute
from normalization.algorithms import closure, is_key, is_superkey, is_relvar_in_bcnf, is_relvar_in_4nf



if __name__ == "__main__":
    fd1 = FunctionalDependency("{RFC} -> {Nombre, CP}")
    fd2 = FunctionalDependency("{FolioF} -> {RFC}")
    fd3 = FunctionalDependency("{FolioF} -> {MontoF, IVA, FechaF}")
    fd4 = FunctionalDependency("{FolioF} -> {RegimenF, CFDI}")
    fd5 = FunctionalDependency("{FolioP} -> {MontoP, FechaP}")
    fd6 = FunctionalDependency("{FolioP} -> {FolioF}")
    fd7 = FunctionalDependency("{MontoF} -> {IVA}")

    mvd1 = MultivaluedDependency("{RFC} ->-> {RegimenC}")

    relvar = Relvar(
        heading=["Nombre", "RFC", "CP", "RegimenF", "RegimenC", "CFDI", "FolioF", "MontoF", "IVA", "FechaF", "Producto", "FolioP", "MontoP", "FechaP"],
        functional_dependencies=[fd1, fd2, fd3, fd4, fd5, fd6],
        multivalued_dependencies=[mvd1]
    )

    print(f"Relvar: {relvar}")

    print("\nFunctional dependencies:")
    for fd in relvar.functional_dependencies:
        print(fd)

    print("\nMultivalued dependencies:")
    for mvd in relvar.multivalued_dependencies:
        print(mvd)
    rfc = Attribute("RFC")
    cierre = closure({rfc}, relvar.functional_dependencies)
    print(f"\nCierre de {{RFC}}: {[attr.name for attr in cierre]}")
    print("¿{RFC} es superllave?", is_superkey({rfc}, relvar.heading, relvar.functional_dependencies))

    print("¿{RFC} es llave?", is_key({rfc}, relvar.heading, relvar.functional_dependencies))

    # Probar BCNF y 4NF
    print("¿Relvar en BCNF?", is_relvar_in_bcnf(relvar))
    print("¿Relvar en 4NF?", is_relvar_in_4nf(relvar))
