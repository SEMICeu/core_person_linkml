from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.11.0"
version = "2.1.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'cpv',
     'default_range': 'string',
     'description': 'LinkML approximation of the SEMIC Core Person Vocabulary '
                    '2.1.1. The Core Person Vocabulary captures the fundamental '
                    'characteristics of a person, e.g. name, gender, date of '
                    'birth, etc. It is the ontological backbone for several Core '
                    'Vocabularies and Application Profiles published by SEMIC.',
     'id': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/licenses/by/4.0/',
     'name': 'core_person',
     'prefixes': {'adms': {'prefix_prefix': 'adms',
                           'prefix_reference': 'http://www.w3.org/ns/adms#'},
                  'cpv': {'prefix_prefix': 'cpv',
                          'prefix_reference': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'foaf': {'prefix_prefix': 'foaf',
                           'prefix_reference': 'http://xmlns.com/foaf/0.1/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'locn': {'prefix_prefix': 'locn',
                           'prefix_reference': 'http://www.w3.org/ns/locn#'},
                  'm8g': {'prefix_prefix': 'm8g',
                          'prefix_reference': 'http://data.europa.eu/m8g/'},
                  'owl': {'prefix_prefix': 'owl',
                          'prefix_reference': 'http://www.w3.org/2002/07/owl#'},
                  'person': {'prefix_prefix': 'person',
                             'prefix_reference': 'http://www.w3.org/ns/person#'},
                  'rdf': {'prefix_prefix': 'rdf',
                          'prefix_reference': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'skos': {'prefix_prefix': 'skos',
                           'prefix_reference': 'http://www.w3.org/2004/02/skos/core#'},
                  'xsd': {'prefix_prefix': 'xsd',
                          'prefix_reference': 'http://www.w3.org/2001/XMLSchema#'}},
     'source_file': 'src/core_person/schema/core_person.yaml',
     'title': 'Core Person Vocabulary',
     'types': {'LangString': {'base': 'str',
                              'description': 'A natural-language string with an '
                                             'optional language tag.',
                              'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1',
                              'name': 'LangString',
                              'typeof': 'string',
                              'uri': 'rdf:langString'},
               'gYear': {'base': 'str',
                         'description': 'An XSD gregorian year (e.g. "1980"). '
                                        'Represents a year value in the proleptic '
                                        'Gregorian calendar without a month or '
                                        'day. Backed by Python str because Python '
                                        'has no native gYear type.',
                         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1',
                         'name': 'gYear',
                         'uri': 'xsd:gYear'},
               'gYearMonth': {'base': 'str',
                              'description': 'An XSD gregorian year-month (e.g. '
                                             '"1980-09"). Represents a specific '
                                             'month of a specific year in the '
                                             'proleptic Gregorian calendar without '
                                             'a day. Backed by Python str because '
                                             'Python has no native gYearMonth '
                                             'type.',
                              'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1',
                              'name': 'gYearMonth',
                              'uri': 'xsd:gYearMonth'}}} )


class Person(ConfiguredBaseModel):
    """
    An individual human being who may be dead or alive, but not imaginary.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'person:Person',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    identifier: Optional[list[Identifier]] = Field(default=None, title="identifier", description="""The unambiguous structured reference to the Person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'dcterms:identifier'} })
    alternativeName: Optional[list[str]] = Field(default=None, title="alternative name", description="""Any name by which a Person is known, other than their full name.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'dcterms:alternative'} })
    birthName: Optional[list[str]] = Field(default=None, title="birth name", description="""Full name of the Person given upon their birth.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:birthName'} })
    citizenship: Optional[list[Jurisdiction]] = Field(default=None, title="citizenship", description="""The Jurisdiction that has conferred citizenship rights on the Person such as the right to vote, to receive certain protection from the community or the issuance of a passport.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:citizenship'} })
    contactPoint: Optional[list[ContactPoint]] = Field(default=None, title="contact point", description="""The main contact information of the resource.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:contactPoint'} })
    countryOfBirth: Optional[list[Location]] = Field(default=None, title="country of birth", description="""The country in which the Person was born.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:countryOfBirth'} })
    countryOfDeath: Optional[list[Location]] = Field(default=None, title="country of death", description="""The country in which the Person died.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:countryOfDeath'} })
    dateOfBirth: Optional[list[Union[date, str]]] = Field(default=None, title="date of birth", description="""The point in time on which the Person was born.""", json_schema_extra = { "linkml_meta": {'annotations': {'rdfs:isDefinedBy': {'tag': 'rdfs:isDefinedBy',
                                              'value': 'http://data.europa.eu/m8g'},
                         'rdfs:seeAlso': {'tag': 'rdfs:seeAlso',
                                          'value': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1/#Person.birthdate'}},
         'any_of': [{'range': 'date'}, {'range': 'gYear'}, {'range': 'gYearMonth'}],
         'comments': ['The date of birth could be expressed as date, gYearMonth or '
                      'gYear, e.g. 1980-09-16, 1980-09, 1980.'],
         'domain_of': ['Person'],
         'slot_uri': 'm8g:birthDate'} })
    dateOfDeath: Optional[list[Union[date, str]]] = Field(default=None, title="date of death", description="""The point in time on which the Person died.""", json_schema_extra = { "linkml_meta": {'any_of': [{'range': 'date'}, {'range': 'gYear'}, {'range': 'gYearMonth'}],
         'domain_of': ['Person'],
         'slot_uri': 'm8g:deathDate'} })
    domicile: Optional[list[Address]] = Field(default=None, title="domicile", description="""The place that the Person treats as permanent home.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:domicile'} })
    familyName: Optional[list[str]] = Field(default=None, title="family name", description="""The hereditary surname of a family.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'foaf:familyName'} })
    fullName: Optional[list[str]] = Field(default=None, title="full name", description="""The complete name of the Person as one string.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'foaf:name'} })
    gender: Optional[list[Concept]] = Field(default=None, title="gender", description="""The identities, expressions and societal roles of the Person.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:gender'} })
    givenName: Optional[list[str]] = Field(default=None, title="given name", description="""The name(s) that identify the Person within a family with a common surname.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'foaf:givenName'} })
    matronymicName: Optional[list[str]] = Field(default=None, title="matronymic name", description="""Name based on the given name of the Person's mother.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:matronymicName'} })
    patronymicName: Optional[list[str]] = Field(default=None, title="patronymic name", description="""Name based on the given name of the Person's father.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:patronymicName'} })
    placeOfBirth: Optional[list[Location]] = Field(default=None, title="place of birth", description="""The Location where the Person was born.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:placeOfBirth'} })
    placeOfDeath: Optional[list[Location]] = Field(default=None, title="place of death", description="""The Location where the Person died.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:placeOfDeath'} })
    residency: Optional[list[Jurisdiction]] = Field(default=None, title="residency", description="""Jurisdiction where the Person has their dwelling.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:residency'} })
    sex: Optional[list[Concept]] = Field(default=None, title="sex", description="""The organism's biological sex.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:sex'} })


class Identifier(ConfiguredBaseModel):
    """
    A character string used to uniquely identify one instance of an object within an identification scheme.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'adms:Identifier',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    schemeUri: Optional[list[str]] = Field(default=None, title="scheme URI", description="""URI of the scheme used to construct the identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'dcterms:conformsTo'} })
    schemeName: Optional[list[str]] = Field(default=None, title="scheme name", description="""Name of the scheme used to construct the identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'rdfs:label'} })
    dateOfIssue: Optional[list[date]] = Field(default=None, title="date of issue", description="""The date on which the Identifier was assigned.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'dcterms:issued'} })
    identifies: Optional[list[Person]] = Field(default=None, title="identifies", description="""The entity that is referenced by the Identifier.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'm8g:identifies'} })
    issuingAuthorityUri: Optional[list[Agent]] = Field(default=None, title="issuing authority URI", description="""The reference in the form of a Uniform Resource Identifier to the issuing authority.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'dcterms:creator'} })


class Address(ConfiguredBaseModel):
    """
    An \"address representation\" as conceptually defined by the INSPIRE Address Representation data type.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'locn:Address',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    thoroughfare: Optional[list[str]] = Field(default=None, title="thoroughfare", description="""The name of a passage or way through from one location to another.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:thoroughfare'} })
    administrativeUnitLevel1: Optional[list[str]] = Field(default=None, title="administrative unit level 1", description="""The name of the uppermost level of the address, almost always a country.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:adminUnitL1'} })
    administrativeUnitLevel2: Optional[list[str]] = Field(default=None, title="administrative unit level 2", description="""The name of a secondary level/region of the address, usually a county, state or other such area that typically encompasses several localities.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:adminUnitL2'} })
    addressArea: Optional[list[str]] = Field(default=None, title="address area", description="""The name of a geographic area that groups Addresses.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:addressArea'} })
    postName: Optional[list[str]] = Field(default=None, title="post name", description="""A name created and maintained for postal purposes to identify a subdivision of addresses and postal delivery points.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:postName'} })
    locatorName: Optional[list[str]] = Field(default=None, title="locator name", description="""Proper noun(s) applied to the real world entity identified by the locator. The locator name could be the name of the property or complex, of the building or part of the building, or it could be the name of a room inside a building.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:locatorName'} })
    fullAddress: Optional[list[str]] = Field(default=None, title="full address", description="""The complete address written as a string.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:fullAddress'} })


class ContactPoint(ConfiguredBaseModel):
    """
    Information (e.g. e-mail address, telephone number) of a person or department through which the user can get in touch with.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'm8g:ContactPoint',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    contactPage: Optional[list[Document]] = Field(default=None, title="contact page", description="""A web page that could be used to reach out the Contact Point.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:contactPage'} })
    hasEmail: Optional[list[str]] = Field(default=None, title="has email", description="""An electronic address through which the Contact Point can be contacted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:email'} })
    hasTelephone: Optional[list[str]] = Field(default=None, title="has telephone", description="""A telephone number through which the Contact Point can be contacted.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:telephone'} })


class Agent(ConfiguredBaseModel):
    """
    Any entity carrying out actions, typically a person or an organisation.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'foaf:Agent',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    agentName: Optional[list[str]] = Field(default=None, title="name", description="""The noun given to the Agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Agent'], 'slot_uri': 'dcterms:title'} })
    agentType: Optional[list[Concept]] = Field(default=None, title="type", description="""A classification assigned to an Agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Agent'], 'slot_uri': 'dcterms:type'} })


class Jurisdiction(ConfiguredBaseModel):
    """
    The legal authority — usually a public body — defined by a geographical extent within which it has the power to make legal decisions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcterms:Jurisdiction',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    jurisdictionId: Optional[list[str]] = Field(default=None, title="id", description="""A reference in the form of a Uniform Resource Identifier to the Jurisdiction.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Jurisdiction'], 'slot_uri': 'dcterms:identifier'} })
    jurisdictionName: Optional[list[str]] = Field(default=None, title="name", description="""A string of characters that represents a Jurisdiction.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Jurisdiction'], 'slot_uri': 'rdfs:label'} })


class Location(ConfiguredBaseModel):
    """
    A region or named place. It can be described by a geographic name or geographic identifier.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dcterms:Location',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    geographicName: Optional[list[str]] = Field(default=None, title="geographic name", description="""A textual description for a Location.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location'], 'slot_uri': 'locn:geographicName'} })
    geographicIdentifier: Optional[list[str]] = Field(default=None, title="geographic identifier", description="""A reference in the form of a Uniform Resource Identifier to the Location.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Location'], 'slot_uri': 'rdfs:seeAlso'} })


class Document(ConfiguredBaseModel):
    """
    A document, e.g. a web page.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'foaf:Document',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    pass


class Concept(ConfiguredBaseModel):
    """
    A SKOS concept, used for controlled vocabularies (e.g. for sex, gender).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.1'})

    pass


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Person.model_rebuild()
Identifier.model_rebuild()
Address.model_rebuild()
ContactPoint.model_rebuild()
Agent.model_rebuild()
Jurisdiction.model_rebuild()
Location.model_rebuild()
Document.model_rebuild()
Concept.model_rebuild()
