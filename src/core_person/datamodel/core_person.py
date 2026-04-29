# Auto generated from core_person.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-04-29T10:04:38
# Schema: core_person
#
# id: https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1
# description: LinkML approximation of the SEMIC Core Person Vocabulary 2.1.1. The Core Person Vocabulary captures the fundamental characteristics of a person, e.g. name, gender, date of birth, etc. It is the ontological backbone for several Core Vocabularies and Application Profiles published by SEMIC.
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

from linkml_runtime.linkml_model.types import Date, String, Uri
from linkml_runtime.utils.metamodelcore import URI, XSDDate

metamodel_version = "1.7.0"
version = "2.1.1"

# Namespaces
ADMS = CurieNamespace('adms', 'http://www.w3.org/ns/adms#')
CPV = CurieNamespace('cpv', 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOCN = CurieNamespace('locn', 'http://www.w3.org/ns/locn#')
M8G = CurieNamespace('m8g', 'http://data.europa.eu/m8g/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PERSON = CurieNamespace('person', 'http://www.w3.org/ns/person#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SKOS = CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CPV


# Types
class LangString(String):
    """ A natural-language string with an optional language tag. """
    type_class_uri = RDF["langString"]
    type_class_curie = "rdf:langString"
    type_name = "LangString"
    type_model_uri = CPV.LangString


# Class references



@dataclass(repr=False)
class Person(YAMLRoot):
    """
    An individual human being who may be dead or alive, but not imaginary.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PERSON["Person"]
    class_class_curie: ClassVar[str] = "person:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = CPV.Person

    identifier: Optional[Union[Union[dict, "Identifier"], list[Union[dict, "Identifier"]]]] = empty_list()
    alternativeName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    birthName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    citizenship: Optional[Union[Union[dict, "Jurisdiction"], list[Union[dict, "Jurisdiction"]]]] = empty_list()
    contactPoint: Optional[Union[Union[dict, "ContactPoint"], list[Union[dict, "ContactPoint"]]]] = empty_list()
    countryOfBirth: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    countryOfDeath: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    dateOfBirth: Optional[Union[Union[dict, "GenericDate"], list[Union[dict, "GenericDate"]]]] = empty_list()
    dateOfDeath: Optional[Union[Union[dict, "GenericDate"], list[Union[dict, "GenericDate"]]]] = empty_list()
    domicile: Optional[Union[Union[dict, "Address"], list[Union[dict, "Address"]]]] = empty_list()
    familyName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    fullName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    gender: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()
    givenName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    matronymicName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    patronymicName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    placeOfBirth: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    placeOfDeath: Optional[Union[Union[dict, "Location"], list[Union[dict, "Location"]]]] = empty_list()
    residency: Optional[Union[Union[dict, "Jurisdiction"], list[Union[dict, "Jurisdiction"]]]] = empty_list()
    sex: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.identifier, list):
            self.identifier = [self.identifier] if self.identifier is not None else []
        self.identifier = [v if isinstance(v, Identifier) else Identifier(**as_dict(v)) for v in self.identifier]

        if not isinstance(self.alternativeName, list):
            self.alternativeName = [self.alternativeName] if self.alternativeName is not None else []
        self.alternativeName = [v if isinstance(v, LangString) else LangString(v) for v in self.alternativeName]

        if not isinstance(self.birthName, list):
            self.birthName = [self.birthName] if self.birthName is not None else []
        self.birthName = [v if isinstance(v, LangString) else LangString(v) for v in self.birthName]

        if not isinstance(self.citizenship, list):
            self.citizenship = [self.citizenship] if self.citizenship is not None else []
        self.citizenship = [v if isinstance(v, Jurisdiction) else Jurisdiction(**as_dict(v)) for v in self.citizenship]

        if not isinstance(self.contactPoint, list):
            self.contactPoint = [self.contactPoint] if self.contactPoint is not None else []
        self.contactPoint = [v if isinstance(v, ContactPoint) else ContactPoint(**as_dict(v)) for v in self.contactPoint]

        if not isinstance(self.countryOfBirth, list):
            self.countryOfBirth = [self.countryOfBirth] if self.countryOfBirth is not None else []
        self.countryOfBirth = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.countryOfBirth]

        if not isinstance(self.countryOfDeath, list):
            self.countryOfDeath = [self.countryOfDeath] if self.countryOfDeath is not None else []
        self.countryOfDeath = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.countryOfDeath]

        if not isinstance(self.dateOfBirth, list):
            self.dateOfBirth = [self.dateOfBirth] if self.dateOfBirth is not None else []
        self.dateOfBirth = [v if isinstance(v, GenericDate) else GenericDate(**as_dict(v)) for v in self.dateOfBirth]

        if not isinstance(self.dateOfDeath, list):
            self.dateOfDeath = [self.dateOfDeath] if self.dateOfDeath is not None else []
        self.dateOfDeath = [v if isinstance(v, GenericDate) else GenericDate(**as_dict(v)) for v in self.dateOfDeath]

        if not isinstance(self.domicile, list):
            self.domicile = [self.domicile] if self.domicile is not None else []
        self.domicile = [v if isinstance(v, Address) else Address(**as_dict(v)) for v in self.domicile]

        if not isinstance(self.familyName, list):
            self.familyName = [self.familyName] if self.familyName is not None else []
        self.familyName = [v if isinstance(v, LangString) else LangString(v) for v in self.familyName]

        if not isinstance(self.fullName, list):
            self.fullName = [self.fullName] if self.fullName is not None else []
        self.fullName = [v if isinstance(v, LangString) else LangString(v) for v in self.fullName]

        if not isinstance(self.gender, list):
            self.gender = [self.gender] if self.gender is not None else []
        self.gender = [v if isinstance(v, Concept) else Concept(**as_dict(v)) for v in self.gender]

        if not isinstance(self.givenName, list):
            self.givenName = [self.givenName] if self.givenName is not None else []
        self.givenName = [v if isinstance(v, LangString) else LangString(v) for v in self.givenName]

        if not isinstance(self.matronymicName, list):
            self.matronymicName = [self.matronymicName] if self.matronymicName is not None else []
        self.matronymicName = [v if isinstance(v, LangString) else LangString(v) for v in self.matronymicName]

        if not isinstance(self.patronymicName, list):
            self.patronymicName = [self.patronymicName] if self.patronymicName is not None else []
        self.patronymicName = [v if isinstance(v, LangString) else LangString(v) for v in self.patronymicName]

        if not isinstance(self.placeOfBirth, list):
            self.placeOfBirth = [self.placeOfBirth] if self.placeOfBirth is not None else []
        self.placeOfBirth = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.placeOfBirth]

        if not isinstance(self.placeOfDeath, list):
            self.placeOfDeath = [self.placeOfDeath] if self.placeOfDeath is not None else []
        self.placeOfDeath = [v if isinstance(v, Location) else Location(**as_dict(v)) for v in self.placeOfDeath]

        if not isinstance(self.residency, list):
            self.residency = [self.residency] if self.residency is not None else []
        self.residency = [v if isinstance(v, Jurisdiction) else Jurisdiction(**as_dict(v)) for v in self.residency]

        if not isinstance(self.sex, list):
            self.sex = [self.sex] if self.sex is not None else []
        self.sex = [v if isinstance(v, Concept) else Concept(**as_dict(v)) for v in self.sex]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Identifier(YAMLRoot):
    """
    A character string used to uniquely identify one instance of an object within an identification scheme.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = ADMS["Identifier"]
    class_class_curie: ClassVar[str] = "adms:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = CPV.Identifier

    schemeUri: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    schemeName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    dateOfIssue: Optional[Union[Union[str, XSDDate], list[Union[str, XSDDate]]]] = empty_list()
    identifies: Optional[Union[Union[dict, Person], list[Union[dict, Person]]]] = empty_list()
    issuingAuthorityUri: Optional[Union[Union[dict, "Agent"], list[Union[dict, "Agent"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.schemeUri, list):
            self.schemeUri = [self.schemeUri] if self.schemeUri is not None else []
        self.schemeUri = [v if isinstance(v, URI) else URI(v) for v in self.schemeUri]

        if not isinstance(self.schemeName, list):
            self.schemeName = [self.schemeName] if self.schemeName is not None else []
        self.schemeName = [v if isinstance(v, LangString) else LangString(v) for v in self.schemeName]

        if not isinstance(self.dateOfIssue, list):
            self.dateOfIssue = [self.dateOfIssue] if self.dateOfIssue is not None else []
        self.dateOfIssue = [v if isinstance(v, XSDDate) else XSDDate(v) for v in self.dateOfIssue]

        if not isinstance(self.identifies, list):
            self.identifies = [self.identifies] if self.identifies is not None else []
        self.identifies = [v if isinstance(v, Person) else Person(**as_dict(v)) for v in self.identifies]

        if not isinstance(self.issuingAuthorityUri, list):
            self.issuingAuthorityUri = [self.issuingAuthorityUri] if self.issuingAuthorityUri is not None else []
        self.issuingAuthorityUri = [v if isinstance(v, Agent) else Agent(**as_dict(v)) for v in self.issuingAuthorityUri]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Address(YAMLRoot):
    """
    An "address representation" as conceptually defined by the INSPIRE Address Representation data type.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = LOCN["Address"]
    class_class_curie: ClassVar[str] = "locn:Address"
    class_name: ClassVar[str] = "Address"
    class_model_uri: ClassVar[URIRef] = CPV.Address

    thoroughfare: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    administrativeUnitLevel1: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    administrativeUnitLevel2: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    addressArea: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    postName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    locatorName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    fullAddress: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.thoroughfare, list):
            self.thoroughfare = [self.thoroughfare] if self.thoroughfare is not None else []
        self.thoroughfare = [v if isinstance(v, LangString) else LangString(v) for v in self.thoroughfare]

        if not isinstance(self.administrativeUnitLevel1, list):
            self.administrativeUnitLevel1 = [self.administrativeUnitLevel1] if self.administrativeUnitLevel1 is not None else []
        self.administrativeUnitLevel1 = [v if isinstance(v, LangString) else LangString(v) for v in self.administrativeUnitLevel1]

        if not isinstance(self.administrativeUnitLevel2, list):
            self.administrativeUnitLevel2 = [self.administrativeUnitLevel2] if self.administrativeUnitLevel2 is not None else []
        self.administrativeUnitLevel2 = [v if isinstance(v, LangString) else LangString(v) for v in self.administrativeUnitLevel2]

        if not isinstance(self.addressArea, list):
            self.addressArea = [self.addressArea] if self.addressArea is not None else []
        self.addressArea = [v if isinstance(v, LangString) else LangString(v) for v in self.addressArea]

        if not isinstance(self.postName, list):
            self.postName = [self.postName] if self.postName is not None else []
        self.postName = [v if isinstance(v, LangString) else LangString(v) for v in self.postName]

        if not isinstance(self.locatorName, list):
            self.locatorName = [self.locatorName] if self.locatorName is not None else []
        self.locatorName = [v if isinstance(v, LangString) else LangString(v) for v in self.locatorName]

        if not isinstance(self.fullAddress, list):
            self.fullAddress = [self.fullAddress] if self.fullAddress is not None else []
        self.fullAddress = [v if isinstance(v, LangString) else LangString(v) for v in self.fullAddress]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContactPoint(YAMLRoot):
    """
    Information (e.g. e-mail address, telephone number) of a person or department through which the user can get in
    touch with.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = M8G["ContactPoint"]
    class_class_curie: ClassVar[str] = "m8g:ContactPoint"
    class_name: ClassVar[str] = "ContactPoint"
    class_model_uri: ClassVar[URIRef] = CPV.ContactPoint

    contactPage: Optional[Union[Union[dict, "Document"], list[Union[dict, "Document"]]]] = empty_list()
    hasEmail: Optional[Union[str, list[str]]] = empty_list()
    hasTelephone: Optional[Union[str, list[str]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.contactPage, list):
            self.contactPage = [self.contactPage] if self.contactPage is not None else []
        self.contactPage = [v if isinstance(v, Document) else Document(**as_dict(v)) for v in self.contactPage]

        if not isinstance(self.hasEmail, list):
            self.hasEmail = [self.hasEmail] if self.hasEmail is not None else []
        self.hasEmail = [v if isinstance(v, str) else str(v) for v in self.hasEmail]

        if not isinstance(self.hasTelephone, list):
            self.hasTelephone = [self.hasTelephone] if self.hasTelephone is not None else []
        self.hasTelephone = [v if isinstance(v, str) else str(v) for v in self.hasTelephone]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Agent(YAMLRoot):
    """
    Any entity carrying out actions, typically a person or an organisation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Agent"]
    class_class_curie: ClassVar[str] = "foaf:Agent"
    class_name: ClassVar[str] = "Agent"
    class_model_uri: ClassVar[URIRef] = CPV.Agent

    agentName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    agentType: Optional[Union[Union[dict, "Concept"], list[Union[dict, "Concept"]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.agentName, list):
            self.agentName = [self.agentName] if self.agentName is not None else []
        self.agentName = [v if isinstance(v, LangString) else LangString(v) for v in self.agentName]

        if not isinstance(self.agentType, list):
            self.agentType = [self.agentType] if self.agentType is not None else []
        self.agentType = [v if isinstance(v, Concept) else Concept(**as_dict(v)) for v in self.agentType]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Jurisdiction(YAMLRoot):
    """
    The legal authority — usually a public body — defined by a geographical extent within which it has the power to
    make legal decisions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Jurisdiction"]
    class_class_curie: ClassVar[str] = "dcterms:Jurisdiction"
    class_name: ClassVar[str] = "Jurisdiction"
    class_model_uri: ClassVar[URIRef] = CPV.Jurisdiction

    jurisdictionId: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()
    jurisdictionName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.jurisdictionId, list):
            self.jurisdictionId = [self.jurisdictionId] if self.jurisdictionId is not None else []
        self.jurisdictionId = [v if isinstance(v, URI) else URI(v) for v in self.jurisdictionId]

        if not isinstance(self.jurisdictionName, list):
            self.jurisdictionName = [self.jurisdictionName] if self.jurisdictionName is not None else []
        self.jurisdictionName = [v if isinstance(v, LangString) else LangString(v) for v in self.jurisdictionName]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Location(YAMLRoot):
    """
    A region or named place. It can be described by a geographic name or geographic identifier.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = DCTERMS["Location"]
    class_class_curie: ClassVar[str] = "dcterms:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = CPV.Location

    geographicName: Optional[Union[Union[str, LangString], list[Union[str, LangString]]]] = empty_list()
    geographicIdentifier: Optional[Union[Union[str, URI], list[Union[str, URI]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if not isinstance(self.geographicName, list):
            self.geographicName = [self.geographicName] if self.geographicName is not None else []
        self.geographicName = [v if isinstance(v, LangString) else LangString(v) for v in self.geographicName]

        if not isinstance(self.geographicIdentifier, list):
            self.geographicIdentifier = [self.geographicIdentifier] if self.geographicIdentifier is not None else []
        self.geographicIdentifier = [v if isinstance(v, URI) else URI(v) for v in self.geographicIdentifier]

        super().__post_init__(**kwargs)


class Document(YAMLRoot):
    """
    A document, e.g. a web page.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = FOAF["Document"]
    class_class_curie: ClassVar[str] = "foaf:Document"
    class_name: ClassVar[str] = "Document"
    class_model_uri: ClassVar[URIRef] = CPV.Document


class Concept(YAMLRoot):
    """
    A SKOS concept, used for controlled vocabularies (e.g. for sex, gender).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SKOS["Concept"]
    class_class_curie: ClassVar[str] = "skos:Concept"
    class_name: ClassVar[str] = "Concept"
    class_model_uri: ClassVar[URIRef] = CPV.Concept


class GenericDate(YAMLRoot):
    """
    The generic date data type is the union of xsd:date, xsd:gYearMonth and xsd:gYear.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = M8G["GenericDate"]
    class_class_curie: ClassVar[str] = "m8g:GenericDate"
    class_name: ClassVar[str] = "GenericDate"
    class_model_uri: ClassVar[URIRef] = CPV.GenericDate


# Enumerations


# Slots
class slots:
    pass

slots.identifier = Slot(uri=DCTERMS.identifier, name="identifier", curie=DCTERMS.curie('identifier'),
                   model_uri=CPV.identifier, domain=None, range=Optional[Union[Union[dict, Identifier], list[Union[dict, Identifier]]]])

slots.alternativeName = Slot(uri=DCTERMS.alternative, name="alternativeName", curie=DCTERMS.curie('alternative'),
                   model_uri=CPV.alternativeName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.birthName = Slot(uri=PERSON.birthName, name="birthName", curie=PERSON.curie('birthName'),
                   model_uri=CPV.birthName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.citizenship = Slot(uri=PERSON.citizenship, name="citizenship", curie=PERSON.curie('citizenship'),
                   model_uri=CPV.citizenship, domain=None, range=Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]])

slots.contactPoint = Slot(uri=M8G.contactPoint, name="contactPoint", curie=M8G.curie('contactPoint'),
                   model_uri=CPV.contactPoint, domain=None, range=Optional[Union[Union[dict, ContactPoint], list[Union[dict, ContactPoint]]]])

slots.countryOfBirth = Slot(uri=PERSON.countryOfBirth, name="countryOfBirth", curie=PERSON.curie('countryOfBirth'),
                   model_uri=CPV.countryOfBirth, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.countryOfDeath = Slot(uri=PERSON.countryOfDeath, name="countryOfDeath", curie=PERSON.curie('countryOfDeath'),
                   model_uri=CPV.countryOfDeath, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.dateOfBirth = Slot(uri=M8G.birthDate, name="dateOfBirth", curie=M8G.curie('birthDate'),
                   model_uri=CPV.dateOfBirth, domain=None, range=Optional[Union[Union[dict, GenericDate], list[Union[dict, GenericDate]]]])

slots.dateOfDeath = Slot(uri=M8G.deathDate, name="dateOfDeath", curie=M8G.curie('deathDate'),
                   model_uri=CPV.dateOfDeath, domain=None, range=Optional[Union[Union[dict, GenericDate], list[Union[dict, GenericDate]]]])

slots.domicile = Slot(uri=M8G.domicile, name="domicile", curie=M8G.curie('domicile'),
                   model_uri=CPV.domicile, domain=None, range=Optional[Union[Union[dict, Address], list[Union[dict, Address]]]])

slots.familyName = Slot(uri=FOAF.familyName, name="familyName", curie=FOAF.curie('familyName'),
                   model_uri=CPV.familyName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.fullName = Slot(uri=FOAF.name, name="fullName", curie=FOAF.curie('name'),
                   model_uri=CPV.fullName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.gender = Slot(uri=M8G.gender, name="gender", curie=M8G.curie('gender'),
                   model_uri=CPV.gender, domain=None, range=Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]])

slots.givenName = Slot(uri=FOAF.givenName, name="givenName", curie=FOAF.curie('givenName'),
                   model_uri=CPV.givenName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.matronymicName = Slot(uri=M8G.matronymicName, name="matronymicName", curie=M8G.curie('matronymicName'),
                   model_uri=CPV.matronymicName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.patronymicName = Slot(uri=PERSON.patronymicName, name="patronymicName", curie=PERSON.curie('patronymicName'),
                   model_uri=CPV.patronymicName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.placeOfBirth = Slot(uri=PERSON.placeOfBirth, name="placeOfBirth", curie=PERSON.curie('placeOfBirth'),
                   model_uri=CPV.placeOfBirth, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.placeOfDeath = Slot(uri=PERSON.placeOfDeath, name="placeOfDeath", curie=PERSON.curie('placeOfDeath'),
                   model_uri=CPV.placeOfDeath, domain=None, range=Optional[Union[Union[dict, Location], list[Union[dict, Location]]]])

slots.residency = Slot(uri=PERSON.residency, name="residency", curie=PERSON.curie('residency'),
                   model_uri=CPV.residency, domain=None, range=Optional[Union[Union[dict, Jurisdiction], list[Union[dict, Jurisdiction]]]])

slots.sex = Slot(uri=M8G.sex, name="sex", curie=M8G.curie('sex'),
                   model_uri=CPV.sex, domain=None, range=Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]])

slots.schemeUri = Slot(uri=DCTERMS.conformsTo, name="schemeUri", curie=DCTERMS.curie('conformsTo'),
                   model_uri=CPV.schemeUri, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.schemeName = Slot(uri=RDFS.label, name="schemeName", curie=RDFS.curie('label'),
                   model_uri=CPV.schemeName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.dateOfIssue = Slot(uri=DCTERMS.issued, name="dateOfIssue", curie=DCTERMS.curie('issued'),
                   model_uri=CPV.dateOfIssue, domain=None, range=Optional[Union[Union[str, XSDDate], list[Union[str, XSDDate]]]])

slots.identifies = Slot(uri=M8G.identifies, name="identifies", curie=M8G.curie('identifies'),
                   model_uri=CPV.identifies, domain=None, range=Optional[Union[Union[dict, Person], list[Union[dict, Person]]]])

slots.issuingAuthorityUri = Slot(uri=DCTERMS.creator, name="issuingAuthorityUri", curie=DCTERMS.curie('creator'),
                   model_uri=CPV.issuingAuthorityUri, domain=None, range=Optional[Union[Union[dict, Agent], list[Union[dict, Agent]]]])

slots.thoroughfare = Slot(uri=LOCN.thoroughfare, name="thoroughfare", curie=LOCN.curie('thoroughfare'),
                   model_uri=CPV.thoroughfare, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.administrativeUnitLevel1 = Slot(uri=LOCN.adminUnitL1, name="administrativeUnitLevel1", curie=LOCN.curie('adminUnitL1'),
                   model_uri=CPV.administrativeUnitLevel1, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.administrativeUnitLevel2 = Slot(uri=LOCN.adminUnitL2, name="administrativeUnitLevel2", curie=LOCN.curie('adminUnitL2'),
                   model_uri=CPV.administrativeUnitLevel2, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.addressArea = Slot(uri=LOCN.addressArea, name="addressArea", curie=LOCN.curie('addressArea'),
                   model_uri=CPV.addressArea, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.postName = Slot(uri=LOCN.postName, name="postName", curie=LOCN.curie('postName'),
                   model_uri=CPV.postName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.locatorName = Slot(uri=LOCN.locatorName, name="locatorName", curie=LOCN.curie('locatorName'),
                   model_uri=CPV.locatorName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.fullAddress = Slot(uri=LOCN.fullAddress, name="fullAddress", curie=LOCN.curie('fullAddress'),
                   model_uri=CPV.fullAddress, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.contactPage = Slot(uri=M8G.contactPage, name="contactPage", curie=M8G.curie('contactPage'),
                   model_uri=CPV.contactPage, domain=None, range=Optional[Union[Union[dict, Document], list[Union[dict, Document]]]])

slots.hasEmail = Slot(uri=M8G.email, name="hasEmail", curie=M8G.curie('email'),
                   model_uri=CPV.hasEmail, domain=None, range=Optional[Union[str, list[str]]])

slots.hasTelephone = Slot(uri=M8G.telephone, name="hasTelephone", curie=M8G.curie('telephone'),
                   model_uri=CPV.hasTelephone, domain=None, range=Optional[Union[str, list[str]]])

slots.agentName = Slot(uri=DCTERMS.title, name="agentName", curie=DCTERMS.curie('title'),
                   model_uri=CPV.agentName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.agentType = Slot(uri=DCTERMS.type, name="agentType", curie=DCTERMS.curie('type'),
                   model_uri=CPV.agentType, domain=None, range=Optional[Union[Union[dict, Concept], list[Union[dict, Concept]]]])

slots.jurisdictionId = Slot(uri=DCTERMS.identifier, name="jurisdictionId", curie=DCTERMS.curie('identifier'),
                   model_uri=CPV.jurisdictionId, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])

slots.jurisdictionName = Slot(uri=RDFS.label, name="jurisdictionName", curie=RDFS.curie('label'),
                   model_uri=CPV.jurisdictionName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.geographicName = Slot(uri=LOCN.geographicName, name="geographicName", curie=LOCN.curie('geographicName'),
                   model_uri=CPV.geographicName, domain=None, range=Optional[Union[Union[str, LangString], list[Union[str, LangString]]]])

slots.geographicIdentifier = Slot(uri=RDFS.seeAlso, name="geographicIdentifier", curie=RDFS.curie('seeAlso'),
                   model_uri=CPV.geographicIdentifier, domain=None, range=Optional[Union[Union[str, URI], list[Union[str, URI]]]])
