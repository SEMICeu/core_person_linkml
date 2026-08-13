# Auto generated from core_person.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-08-13T20:08:18
# Schema: core_person_2_1_2
#
# id: https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml
# description: LinkML candidate for the SEMIC Core Person Vocabulary 2.1.2. The official SHACL distribution remains authoritative. This schema preserves its open, optional and multivalued property semantics; SEMIC generator extensions are used for sh:uniqueLang and unrestricted RDF literal constraints.
# license: https://creativecommons.org/licenses/by/4.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Date
from linkml_runtime.utils.metamodelcore import XSDDate

metamodel_version = "1.11.0"
version = "2.1.2"

# Namespaces
ADMS = CurieNamespace('adms', 'http://www.w3.org/ns/adms#')
CP212 = CurieNamespace('cp212', 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOCN = CurieNamespace('locn', 'http://www.w3.org/ns/locn#')
M8G = CurieNamespace('m8g', 'http://data.europa.eu/m8g/')
PERSON = CurieNamespace('person', 'http://www.w3.org/ns/person#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CP212


# Types
class LangString(str):
    """ An RDF language-tagged string. """
    type_class_uri = RDF["langString"]
    type_class_curie = "rdf:langString"
    type_name = "lang_string"
    type_model_uri = CP212.LangString


class RdfLiteral(str):
    """ Any RDF literal. The SEMIC SHACL adapter emits only sh:nodeKind sh:Literal and intentionally removes the overly restrictive sh:datatype rdfs:Literal. """
    type_class_uri = RDFS["Literal"]
    type_class_curie = "rdfs:Literal"
    type_name = "rdf_literal"
    type_model_uri = CP212.RdfLiteral


class AnyUriLiteral(str):
    """ An xsd:anyURI typed RDF literal. This is intentionally not an RDF IRI node. """
    type_class_uri = XSD["anyURI"]
    type_class_curie = "xsd:anyURI"
    type_name = "any_uri_literal"
    type_model_uri = CP212.AnyUriLiteral


# Class references



@dataclass(repr=False)
class Address(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LOCN["Address"]
    class_class_curie: ClassVar[str] = "locn:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = CP212.Address

    administrative_unit: Optional[Union[Union[dict, "AdministrativeUnit"], list[Union[dict, "AdministrativeUnit"]]]] = empty_list()
    address_area: Optional[Union[str, list[str]]] = empty_list()
    address_id: Optional[Union[str, list[str]]] = empty_list()
    admin_unit_l1: Optional[Union[str, list[str]]] = empty_list()
    admin_unit_l2: Optional[Union[str, list[str]]] = empty_list()
    full_address: Optional[Union[str, list[str]]] = empty_list()
    locator_designator: Optional[Union[str, list[str]]] = empty_list()
    locator_name: Optional[Union[str, list[str]]] = empty_list()
    po_box: Optional[Union[str, list[str]]] = empty_list()
    post_code: Optional[Union[str, list[str]]] = empty_list()
    post_name: Optional[Union[str, list[str]]] = empty_list()
    thoroughfare: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.administrative_unit, list):
            self.administrative_unit = [self.administrative_unit] if self.administrative_unit is not None else []
        self.administrative_unit = [v if isinstance(v, AdministrativeUnit) else AdministrativeUnit(**as_dict(v)) for v in self.administrative_unit]

        if not isinstance(self.address_area, list):
            self.address_area = [self.address_area] if self.address_area is not None else []
        self.address_area = [v if isinstance(v, str) else str(v) for v in self.address_area]

        if not isinstance(self.address_id, list):
            self.address_id = [self.address_id] if self.address_id is not None else []
        self.address_id = [v if isinstance(v, str) else str(v) for v in self.address_id]

        if not isinstance(self.admin_unit_l1, list):
            self.admin_unit_l1 = [self.admin_unit_l1] if self.admin_unit_l1 is not None else []
        self.admin_unit_l1 = [v if isinstance(v, str) else str(v) for v in self.admin_unit_l1]

        if not isinstance(self.admin_unit_l2, list):
            self.admin_unit_l2 = [self.admin_unit_l2] if self.admin_unit_l2 is not None else []
        self.admin_unit_l2 = [v if isinstance(v, str) else str(v) for v in self.admin_unit_l2]

        if not isinstance(self.full_address, list):
            self.full_address = [self.full_address] if self.full_address is not None else []
        self.full_address = [v if isinstance(v, str) else str(v) for v in self.full_address]

        if not isinstance(self.locator_designator, list):
            self.locator_designator = [self.locator_designator] if self.locator_designator is not None else []
        self.locator_designator = [v if isinstance(v, str) else str(v) for v in self.locator_designator]

        if not isinstance(self.locator_name, list):
            self.locator_name = [self.locator_name] if self.locator_name is not None else []
        self.locator_name = [v if isinstance(v, str) else str(v) for v in self.locator_name]

        if not isinstance(self.po_box, list):
            self.po_box = [self.po_box] if self.po_box is not None else []
        self.po_box = [v if isinstance(v, str) else str(v) for v in self.po_box]

        if not isinstance(self.post_code, list):
            self.post_code = [self.post_code] if self.post_code is not None else []
        self.post_code = [v if isinstance(v, str) else str(v) for v in self.post_code]

        if not isinstance(self.post_name, list):
            self.post_name = [self.post_name] if self.post_name is not None else []
        self.post_name = [v if isinstance(v, str) else str(v) for v in self.post_name]

        if not isinstance(self.thoroughfare, list):
            self.thoroughfare = [self.thoroughfare] if self.thoroughfare is not None else []
        self.thoroughfare = [v if isinstance(v, str) else str(v) for v in self.thoroughfare]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AdministrativeUnit(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = M8G["AdminUnit"]
    class_class_curie: ClassVar[str] = "m8g:AdminUnit"
    class_name: ClassVar[str] = "AdministrativeUnit"
    class_model_uri: ClassVar[URIRef] = CP212.AdministrativeUnit

    code: Optional[Union[Union[dict, "Code"], list[Union[dict, "Code"]]]] = empty_list()
    level: Optional[Union[Union[dict, "Code"], list[Union[dict, "Code"]]]] = empty_list()
    label: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.code, list):
            self.code = [self.code] if self.code is not None else []
        self.code = [v if isinstance(v, Code) else Code(**as_dict(v)) for v in self.code]

        if not isinstance(self.level, list):
            self.level = [self.level] if self.level is not None else []
        self.level = [v if isinstance(v, Code) else Code(**as_dict(v)) for v in self.level]

        if not isinstance(self.label, list):
            self.label = [self.label] if self.label is not None else []
        self.label = [v if isinstance(v, str) else str(v) for v in self.label]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Agent(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Agent"]
    class_class_curie: ClassVar[str] = "foaf:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = CP212.Agent

    agent_name: Optional[Union[str, list[str]]] = empty_list()
    agent_type: Optional[Union[Union[dict, "Code"], list[Union[dict, "Code"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.agent_name, list):
            self.agent_name = [self.agent_name] if self.agent_name is not None else []
        self.agent_name = [v if isinstance(v, str) else str(v) for v in self.agent_name]

        if not isinstance(self.agent_type, list):
            self.agent_type = [self.agent_type] if self.agent_type is not None else []
        self.agent_type = [v if isinstance(v, Code) else Code(**as_dict(v)) for v in self.agent_type]

        super().__post_init__(**kwargs)


class Code(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "Code"
    class_model_uri: ClassVar[URIRef] = CP212.Code


@dataclass(repr=False)
class ContactPoint(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = M8G["ContactPoint"]
    class_class_curie: ClassVar[str] = "m8g:ContactPoint"
    class_name: ClassVar[str] = "ContactPoint"
    class_model_uri: ClassVar[URIRef] = CP212.ContactPoint

    contact_page: Optional[Union[Union[dict, "Document"], list[Union[dict, "Document"]]]] = empty_list()
    email: Optional[Union[str, list[str]]] = empty_list()
    telephone: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.contact_page, list):
            self.contact_page = [self.contact_page] if self.contact_page is not None else []
        self.contact_page = [v if isinstance(v, Document) else Document(**as_dict(v)) for v in self.contact_page]

        if not isinstance(self.email, list):
            self.email = [self.email] if self.email is not None else []
        self.email = [v if isinstance(v, str) else str(v) for v in self.email]

        if not isinstance(self.telephone, list):
            self.telephone = [self.telephone] if self.telephone is not None else []
        self.telephone = [v if isinstance(v, str) else str(v) for v in self.telephone]

        super().__post_init__(**kwargs)


class Document(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Document"]
    class_class_curie: ClassVar[str] = "foaf:Document"
    class_name: ClassVar[str] = "Document"
    class_model_uri: ClassVar[URIRef] = CP212.Document


class GenericDate(YAMLRoot):
    """
    Published vocabulary describes date, gYearMonth or gYear; official SHACL currently provides no constraints on this
    class.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = M8G["GenericDate"]
    class_class_curie: ClassVar[str] = "m8g:GenericDate"
    class_name: ClassVar[str] = "GenericDate"
    class_model_uri: ClassVar[URIRef] = CP212.GenericDate


@dataclass(repr=False)
class Identifier(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ADMS["Identifier"]
    class_class_curie: ClassVar[str] = "adms:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = CP212.Identifier

    identifies: Optional[Union[Union[dict, "Person"], list[Union[dict, "Person"]]]] = empty_list()
    issued_by: Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]] = empty_list()
    date_issued: Optional[Union[Union[str, XSDDate], list[Union[str, XSDDate]]]] = empty_list()
    notation: Optional[Union[str, list[str]]] = empty_list()
    scheme_agency: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.identifies, list):
            self.identifies = [self.identifies] if self.identifies is not None else []
        self.identifies = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.identifies]

        if not isinstance(self.issued_by, list):
            self.issued_by = [self.issued_by] if self.issued_by is not None else []
        self.issued_by = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.issued_by]

        if not isinstance(self.date_issued, list):
            self.date_issued = [self.date_issued] if self.date_issued is not None else []
        self.date_issued = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.date_issued]

        if not isinstance(self.notation, list):
            self.notation = [self.notation] if self.notation is not None else []
        self.notation = [v if isinstance(v, str) else str(v) for v in self.notation]

        if not isinstance(self.scheme_agency, list):
            self.scheme_agency = [self.scheme_agency] if self.scheme_agency is not None else []
        self.scheme_agency = [v if isinstance(v, str) else str(v) for v in self.scheme_agency]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Jurisdiction(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["Jurisdiction"]
    class_class_curie: ClassVar[str] = "dct:Jurisdiction"
    class_name: ClassVar[str] = "Jurisdiction"
    class_model_uri: ClassVar[URIRef] = CP212.Jurisdiction

    jurisdiction_identifier: Optional[Union[str, list[str]]] = empty_list()
    label: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.jurisdiction_identifier, list):
            self.jurisdiction_identifier = [self.jurisdiction_identifier] if self.jurisdiction_identifier is not None else []
        self.jurisdiction_identifier = [v if isinstance(v, str) else str(v) for v in self.jurisdiction_identifier]

        if not isinstance(self.label, list):
            self.label = [self.label] if self.label is not None else []
        self.label = [v if isinstance(v, str) else str(v) for v in self.label]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Location(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCT["Location"]
    class_class_curie: ClassVar[str] = "dct:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = CP212.Location

    geographic_identifier: Optional[Union[str, list[str]]] = empty_list()
    geographic_name: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.geographic_identifier, list):
            self.geographic_identifier = [self.geographic_identifier] if self.geographic_identifier is not None else []
        self.geographic_identifier = [v if isinstance(v, str) else str(v) for v in self.geographic_identifier]

        if not isinstance(self.geographic_name, list):
            self.geographic_name = [self.geographic_name] if self.geographic_name is not None else []
        self.geographic_name = [v if isinstance(v, str) else str(v) for v in self.geographic_name]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Person(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSON["Person"]
    class_class_curie: ClassVar[str] = "person:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = CP212.Person

    date_of_birth: Optional[Union[str, list[str]]] = empty_list()
    contact_point: Optional[Union[Union[dict, ContactPoint], list[Union[dict, ContactPoint]]]] = empty_list()
    date_of_death: Optional[Union[str, list[str]]] = empty_list()
    domicile: Optional[Union[Union[dict, Address], list[Union[dict, Address]]]] = empty_list()
    gender: Optional[Union[Union[dict, Code], list[Union[dict, Code]]]] = empty_list()
    matronymic_name: Optional[Union[str, list[str]]] = empty_list()
    sex: Optional[Union[Union[dict, Code], list[Union[dict, Code]]]] = empty_list()
    alternative_name: Optional[Union[str, list[str]]] = empty_list()
    person_identifier: Optional[Union[Union[dict, Identifier], list[Union[dict, Identifier]]]] = empty_list()
    birth_name: Optional[Union[str, list[str]]] = empty_list()
    citizenship: Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]] = empty_list()
    country_of_birth: Optional[Union[Union[dict, Location], list[Union[dict, Location]]]] = empty_list()
    country_of_death: Optional[Union[Union[dict, Location], list[Union[dict, Location]]]] = empty_list()
    patronymic_name: Optional[Union[str, list[str]]] = empty_list()
    place_of_birth: Optional[Union[Union[dict, Location], list[Union[dict, Location]]]] = empty_list()
    place_of_death: Optional[Union[Union[dict, Location], list[Union[dict, Location]]]] = empty_list()
    residency: Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]] = empty_list()
    family_name: Optional[Union[str, list[str]]] = empty_list()
    given_name: Optional[Union[str, list[str]]] = empty_list()
    full_name: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.date_of_birth, list):
            self.date_of_birth = [self.date_of_birth] if self.date_of_birth is not None else []
        self.date_of_birth = [v if isinstance(v, str) else str(v) for v in self.date_of_birth]

        if not isinstance(self.contact_point, list):
            self.contact_point = [self.contact_point] if self.contact_point is not None else []
        self.contact_point = [v if isinstance(v, ContactPoint) else ContactPoint(**as_dict(v)) for v in self.contact_point]

        if not isinstance(self.date_of_death, list):
            self.date_of_death = [self.date_of_death] if self.date_of_death is not None else []
        self.date_of_death = [v if isinstance(v, str) else str(v) for v in self.date_of_death]

        if not isinstance(self.domicile, list):
            self.domicile = [self.domicile] if self.domicile is not None else []
        self.domicile = [v if isinstance(v, Address) else Address(**as_dict(v)) for v in self.domicile]

        if not isinstance(self.gender, list):
            self.gender = [self.gender] if self.gender is not None else []
        self.gender = [v if isinstance(v, Code) else Code(**as_dict(v)) for v in self.gender]

        if not isinstance(self.matronymic_name, list):
            self.matronymic_name = [self.matronymic_name] if self.matronymic_name is not None else []
        self.matronymic_name = [v if isinstance(v, str) else str(v) for v in self.matronymic_name]

        if not isinstance(self.sex, list):
            self.sex = [self.sex] if self.sex is not None else []
        self.sex = [v if isinstance(v, Code) else Code(**as_dict(v)) for v in self.sex]

        if not isinstance(self.alternative_name, list):
            self.alternative_name = [self.alternative_name] if self.alternative_name is not None else []
        self.alternative_name = [v if isinstance(v, str) else str(v) for v in self.alternative_name]

        if not isinstance(self.person_identifier, list):
            self.person_identifier = [self.person_identifier] if self.person_identifier is not None else []
        self.person_identifier = [v if isinstance(v, Identifier) else Identifier(**as_dict(v)) for v in self.person_identifier]

        if not isinstance(self.birth_name, list):
            self.birth_name = [self.birth_name] if self.birth_name is not None else []
        self.birth_name = [v if isinstance(v, str) else str(v) for v in self.birth_name]

        if not isinstance(self.citizenship, list):
            self.citizenship = [self.citizenship] if self.citizenship is not None else []
        self.citizenship = [v if isinstance(v, Jurisdiction) else Jurisdiction(**as_dict(v)) for v in self.citizenship]

        if not isinstance(self.country_of_birth, list):
            self.country_of_birth = [self.country_of_birth] if self.country_of_birth is not None else []
        self.country_of_birth = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.country_of_birth]

        if not isinstance(self.country_of_death, list):
            self.country_of_death = [self.country_of_death] if self.country_of_death is not None else []
        self.country_of_death = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.country_of_death]

        if not isinstance(self.patronymic_name, list):
            self.patronymic_name = [self.patronymic_name] if self.patronymic_name is not None else []
        self.patronymic_name = [v if isinstance(v, str) else str(v) for v in self.patronymic_name]

        if not isinstance(self.place_of_birth, list):
            self.place_of_birth = [self.place_of_birth] if self.place_of_birth is not None else []
        self.place_of_birth = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.place_of_birth]

        if not isinstance(self.place_of_death, list):
            self.place_of_death = [self.place_of_death] if self.place_of_death is not None else []
        self.place_of_death = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.place_of_death]

        if not isinstance(self.residency, list):
            self.residency = [self.residency] if self.residency is not None else []
        self.residency = [v if isinstance(v, Jurisdiction) else Jurisdiction(**as_dict(v)) for v in self.residency]

        if not isinstance(self.family_name, list):
            self.family_name = [self.family_name] if self.family_name is not None else []
        self.family_name = [v if isinstance(v, str) else str(v) for v in self.family_name]

        if not isinstance(self.given_name, list):
            self.given_name = [self.given_name] if self.given_name is not None else []
        self.given_name = [v if isinstance(v, str) else str(v) for v in self.given_name]

        if not isinstance(self.full_name, list):
            self.full_name = [self.full_name] if self.full_name is not None else []
        self.full_name = [v if isinstance(v, str) else str(v) for v in self.full_name]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.administrative_unit = Slot(uri=M8G.adminUnit, name="administrative_unit", curie=M8G.curie('adminUnit'),
                   model_uri=CP212.administrative_unit, domain=None, range=Optional[Union[Union[dict, AdministrativeUnit], list[Union[dict, AdministrativeUnit]]]])

slots.address_area = Slot(uri=LOCN.addressArea, name="address_area", curie=LOCN.curie('addressArea'),
                   model_uri=CP212.address_area, domain=None, range=Optional[Union[str, list[str]]])

slots.address_id = Slot(uri=LOCN.addressId, name="address_id", curie=LOCN.curie('addressId'),
                   model_uri=CP212.address_id, domain=None, range=Optional[Union[str, list[str]]])

slots.admin_unit_l1 = Slot(uri=LOCN.adminUnitL1, name="admin_unit_l1", curie=LOCN.curie('adminUnitL1'),
                   model_uri=CP212.admin_unit_l1, domain=None, range=Optional[Union[str, list[str]]])

slots.admin_unit_l2 = Slot(uri=LOCN.adminUnitL2, name="admin_unit_l2", curie=LOCN.curie('adminUnitL2'),
                   model_uri=CP212.admin_unit_l2, domain=None, range=Optional[Union[str, list[str]]])

slots.full_address = Slot(uri=LOCN.fullAddress, name="full_address", curie=LOCN.curie('fullAddress'),
                   model_uri=CP212.full_address, domain=None, range=Optional[Union[str, list[str]]])

slots.locator_designator = Slot(uri=LOCN.locatorDesignator, name="locator_designator", curie=LOCN.curie('locatorDesignator'),
                   model_uri=CP212.locator_designator, domain=None, range=Optional[Union[str, list[str]]])

slots.locator_name = Slot(uri=LOCN.locatorName, name="locator_name", curie=LOCN.curie('locatorName'),
                   model_uri=CP212.locator_name, domain=None, range=Optional[Union[str, list[str]]])

slots.po_box = Slot(uri=LOCN.poBox, name="po_box", curie=LOCN.curie('poBox'),
                   model_uri=CP212.po_box, domain=None, range=Optional[Union[str, list[str]]])

slots.post_code = Slot(uri=LOCN.postCode, name="post_code", curie=LOCN.curie('postCode'),
                   model_uri=CP212.post_code, domain=None, range=Optional[Union[str, list[str]]])

slots.post_name = Slot(uri=LOCN.postName, name="post_name", curie=LOCN.curie('postName'),
                   model_uri=CP212.post_name, domain=None, range=Optional[Union[str, list[str]]])

slots.thoroughfare = Slot(uri=LOCN.thoroughfare, name="thoroughfare", curie=LOCN.curie('thoroughfare'),
                   model_uri=CP212.thoroughfare, domain=None, range=Optional[Union[str, list[str]]])

slots.code = Slot(uri=M8G.code, name="code", curie=M8G.curie('code'),
                   model_uri=CP212.code, domain=None, range=Optional[Union[Union[dict, Code], list[Union[dict, Code]]]])

slots.level = Slot(uri=M8G.level, name="level", curie=M8G.curie('level'),
                   model_uri=CP212.level, domain=None, range=Optional[Union[Union[dict, Code], list[Union[dict, Code]]]])

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=CP212.label, domain=None, range=Optional[Union[str, list[str]]])

slots.agent_name = Slot(uri=DCT.title, name="agent_name", curie=DCT.curie('title'),
                   model_uri=CP212.agent_name, domain=None, range=Optional[Union[str, list[str]]])

slots.agent_type = Slot(uri=DCT.type, name="agent_type", curie=DCT.curie('type'),
                   model_uri=CP212.agent_type, domain=None, range=Optional[Union[Union[dict, Code], list[Union[dict, Code]]]])

slots.contact_page = Slot(uri=M8G.contactPage, name="contact_page", curie=M8G.curie('contactPage'),
                   model_uri=CP212.contact_page, domain=None, range=Optional[Union[Union[dict, Document], list[Union[dict, Document]]]])

slots.email = Slot(uri=M8G.email, name="email", curie=M8G.curie('email'),
                   model_uri=CP212.email, domain=None, range=Optional[Union[str, list[str]]])

slots.telephone = Slot(uri=M8G.telephone, name="telephone", curie=M8G.curie('telephone'),
                   model_uri=CP212.telephone, domain=None, range=Optional[Union[str, list[str]]])

slots.identifies = Slot(uri=M8G.identifies, name="identifies", curie=M8G.curie('identifies'),
                   model_uri=CP212.identifies, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.issued_by = Slot(uri=DCT.creator, name="issued_by", curie=DCT.curie('creator'),
                   model_uri=CP212.issued_by, domain=None, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.date_issued = Slot(uri=DCT.issued, name="date_issued", curie=DCT.curie('issued'),
                   model_uri=CP212.date_issued, domain=None, range=Optional[Union[Union[str, XSDDate], list[Union[str, XSDDate]]]])

slots.notation = Slot(uri=SKOS.notation, name="notation", curie=SKOS.curie('notation'),
                   model_uri=CP212.notation, domain=None, range=Optional[Union[str, list[str]]])

slots.scheme_agency = Slot(uri=ADMS.schemeAgency, name="scheme_agency", curie=ADMS.curie('schemeAgency'),
                   model_uri=CP212.scheme_agency, domain=None, range=Optional[Union[str, list[str]]])

slots.jurisdiction_identifier = Slot(uri=DCT.identifier, name="jurisdiction_identifier", curie=DCT.curie('identifier'),
                   model_uri=CP212.jurisdiction_identifier, domain=None, range=Optional[Union[str, list[str]]])

slots.geographic_identifier = Slot(uri=RDFS.seeAlso, name="geographic_identifier", curie=RDFS.curie('seeAlso'),
                   model_uri=CP212.geographic_identifier, domain=None, range=Optional[Union[str, list[str]]])

slots.geographic_name = Slot(uri=LOCN.geographicName, name="geographic_name", curie=LOCN.curie('geographicName'),
                   model_uri=CP212.geographic_name, domain=None, range=Optional[Union[str, list[str]]])

slots.date_of_birth = Slot(uri=M8G.birthDate, name="date_of_birth", curie=M8G.curie('birthDate'),
                   model_uri=CP212.date_of_birth, domain=None, range=Optional[Union[str, list[str]]])

slots.contact_point = Slot(uri=M8G.contactPoint, name="contact_point", curie=M8G.curie('contactPoint'),
                   model_uri=CP212.contact_point, domain=None, range=Optional[Union[Union[dict, ContactPoint], list[Union[dict, ContactPoint]]]])

slots.date_of_death = Slot(uri=M8G.deathDate, name="date_of_death", curie=M8G.curie('deathDate'),
                   model_uri=CP212.date_of_death, domain=None, range=Optional[Union[str, list[str]]])

slots.domicile = Slot(uri=M8G.domicile, name="domicile", curie=M8G.curie('domicile'),
                   model_uri=CP212.domicile, domain=None, range=Optional[Union[Union[dict, Address], list[Union[dict, Address]]]])

slots.gender = Slot(uri=M8G.gender, name="gender", curie=M8G.curie('gender'),
                   model_uri=CP212.gender, domain=None, range=Optional[Union[Union[dict, Code], list[Union[dict, Code]]]])

slots.matronymic_name = Slot(uri=M8G.matronymicName, name="matronymic_name", curie=M8G.curie('matronymicName'),
                   model_uri=CP212.matronymic_name, domain=None, range=Optional[Union[str, list[str]]])

slots.sex = Slot(uri=M8G.sex, name="sex", curie=M8G.curie('sex'),
                   model_uri=CP212.sex, domain=None, range=Optional[Union[Union[dict, Code], list[Union[dict, Code]]]])

slots.alternative_name = Slot(uri=DCT.alternative, name="alternative_name", curie=DCT.curie('alternative'),
                   model_uri=CP212.alternative_name, domain=None, range=Optional[Union[str, list[str]]])

slots.person_identifier = Slot(uri=DCT.identifier, name="person_identifier", curie=DCT.curie('identifier'),
                   model_uri=CP212.person_identifier, domain=None, range=Optional[Union[Union[dict, Identifier], list[Union[dict, Identifier]]]])

slots.birth_name = Slot(uri=PERSON.birthName, name="birth_name", curie=PERSON.curie('birthName'),
                   model_uri=CP212.birth_name, domain=None, range=Optional[Union[str, list[str]]])

slots.citizenship = Slot(uri=PERSON.citizenship, name="citizenship", curie=PERSON.curie('citizenship'),
                   model_uri=CP212.citizenship, domain=None, range=Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]])

slots.country_of_birth = Slot(uri=PERSON.countryOfBirth, name="country_of_birth", curie=PERSON.curie('countryOfBirth'),
                   model_uri=CP212.country_of_birth, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.country_of_death = Slot(uri=PERSON.countryOfDeath, name="country_of_death", curie=PERSON.curie('countryOfDeath'),
                   model_uri=CP212.country_of_death, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.patronymic_name = Slot(uri=PERSON.patronymicName, name="patronymic_name", curie=PERSON.curie('patronymicName'),
                   model_uri=CP212.patronymic_name, domain=None, range=Optional[Union[str, list[str]]])

slots.place_of_birth = Slot(uri=PERSON.placeOfBirth, name="place_of_birth", curie=PERSON.curie('placeOfBirth'),
                   model_uri=CP212.place_of_birth, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.place_of_death = Slot(uri=PERSON.placeOfDeath, name="place_of_death", curie=PERSON.curie('placeOfDeath'),
                   model_uri=CP212.place_of_death, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.residency = Slot(uri=PERSON.residency, name="residency", curie=PERSON.curie('residency'),
                   model_uri=CP212.residency, domain=None, range=Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]])

slots.family_name = Slot(uri=FOAF.familyName, name="family_name", curie=FOAF.curie('familyName'),
                   model_uri=CP212.family_name, domain=None, range=Optional[Union[str, list[str]]])

slots.given_name = Slot(uri=FOAF.givenName, name="given_name", curie=FOAF.curie('givenName'),
                   model_uri=CP212.given_name, domain=None, range=Optional[Union[str, list[str]]])

slots.full_name = Slot(uri=FOAF.name, name="full_name", curie=FOAF.curie('name'),
                   model_uri=CP212.full_name, domain=None, range=Optional[Union[str, list[str]]])
