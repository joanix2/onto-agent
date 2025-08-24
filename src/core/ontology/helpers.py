from typing import Optional, Union
from src.core.ontology.dataclasses import CardinalityAxiom, ClassEntity, DataPropertyRelation, DisjointClassesAxiom, EquivalentClassesAxiom, FunctionalPropertyAxiom, IndividualEntity, ObjectPropertyRelation, SubClassOfAxiom


def make_class(name: str) -> ClassEntity:
    return ClassEntity(name=name.strip())

def make_individual(name: str, *types_: str) -> IndividualEntity:
    return IndividualEntity(name=name.strip(), types=tuple(t.strip() for t in types_ if t and t.strip()))

def obj_prop(name: str, domain: str, range_: str) -> ObjectPropertyRelation:
    return ObjectPropertyRelation(name=name.strip(), domain=domain.strip(), range=range_.strip())

def data_prop(name: str, domain: str, dtype: str) -> DataPropertyRelation:
    return DataPropertyRelation(name=name.strip(), domain=domain.strip(), range=dtype.strip())

def ax_subclass(subclass: str, superclass: str) -> SubClassOfAxiom:
    return SubClassOfAxiom(subclass=subclass.strip(), superclass=superclass.strip())

def ax_disjoint(*classes: str) -> DisjointClassesAxiom:
    cl = tuple(c.strip() for c in classes if c and c.strip())
    return DisjointClassesAxiom(classes=cl)

def ax_equivalent(*classes: str) -> EquivalentClassesAxiom:
    cl = tuple(c.strip() for c in classes if c and c.strip())
    return EquivalentClassesAxiom(classes=cl)

def ax_functional(prop: str) -> FunctionalPropertyAxiom:
    return FunctionalPropertyAxiom(property=prop.strip())

def ax_cardinality(prop: str, domain: str,
                   min_: Optional[int] = None,
                   max_: Optional[Union[int, str]] = None,
                   exact_: Optional[int] = None) -> CardinalityAxiom:
    return CardinalityAxiom(property=prop.strip(), domain=domain.strip(),
                            min=min_, max=max_, exact=exact_)