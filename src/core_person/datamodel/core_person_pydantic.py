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
version = "2.1.2"


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


linkml_meta = LinkMLMeta({'annotations': {'semic_authority': {'tag': 'semic_authority',
                                         'value': 'official SHACL distribution'},
                     'semic_profile': {'tag': 'semic_profile',
                                       'value': 'open shapes; all properties '
                                                'optional and multivalued'},
                     'semic_source_commit': {'tag': 'semic_source_commit',
                                             'value': 'a1b13f2bed9fd97b28420b0cef7f0032da08d148'},
                     'semic_source_release': {'tag': 'semic_source_release',
                                              'value': 'Core Person 2.1.2'}},
     'default_prefix': 'cp212',
     'default_range': 'rdf_literal',
     'description': 'LinkML candidate for the SEMIC Core Person Vocabulary 2.1.2. '
                    'The official SHACL distribution remains authoritative. This '
                    'schema preserves its open, optional and multivalued property '
                    'semantics; SEMIC generator extensions are used for '
                    'sh:uniqueLang and unrestricted RDF literal constraints.',
     'id': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
     'imports': ['linkml:types'],
     'license': 'https://creativecommons.org/licenses/by/4.0/',
     'name': 'core_person_2_1_2',
     'prefixes': {'adms': {'prefix_prefix': 'adms',
                           'prefix_reference': 'http://www.w3.org/ns/adms#'},
                  'cp212': {'prefix_prefix': 'cp212',
                            'prefix_reference': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/'},
                  'dct': {'prefix_prefix': 'dct',
                          'prefix_reference': 'http://purl.org/dc/terms/'},
                  'foaf': {'prefix_prefix': 'foaf',
                           'prefix_reference': 'http://xmlns.com/foaf/0.1/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'locn': {'prefix_prefix': 'locn',
                           'prefix_reference': 'http://www.w3.org/ns/locn#'},
                  'm8g': {'prefix_prefix': 'm8g',
                          'prefix_reference': 'http://data.europa.eu/m8g/'},
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
     'source_file': 'src\\core_person\\schema\\core_person.yaml',
     'title': 'SEMIC Core Person Vocabulary 2.1.2 � LinkML candidate',
     'types': {'any_uri_literal': {'base': 'str',
                                   'description': 'An xsd:anyURI typed RDF '
                                                  'literal. This is intentionally '
                                                  'not an RDF IRI node.',
                                   'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
                                   'name': 'any_uri_literal',
                                   'uri': 'xsd:anyURI'},
               'lang_string': {'base': 'str',
                               'description': 'An RDF language-tagged string.',
                               'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
                               'name': 'lang_string',
                               'uri': 'rdf:langString'},
               'rdf_literal': {'base': 'str',
                               'description': 'Any RDF literal. The SEMIC SHACL '
                                              'adapter emits only sh:nodeKind '
                                              'sh:Literal and intentionally '
                                              'removes the overly restrictive '
                                              'sh:datatype rdfs:Literal.',
                               'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
                               'name': 'rdf_literal',
                               'uri': 'rdfs:Literal'}}} )


class Address(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'locn:Address',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    administrative_unit: Optional[list[AdministrativeUnit]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'm8g:adminUnit'} })
    address_area: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:addressArea'} })
    address_id: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:addressId'} })
    admin_unit_l1: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:adminUnitL1'} })
    admin_unit_l2: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:adminUnitL2'} })
    full_address: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:fullAddress'} })
    locator_designator: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:locatorDesignator'} })
    locator_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:locatorName'} })
    po_box: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:poBox'} })
    post_code: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Address'], 'slot_uri': 'locn:postCode'} })
    post_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:postName'} })
    thoroughfare: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Address'],
         'slot_uri': 'locn:thoroughfare'} })


class AdministrativeUnit(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'm8g:AdminUnit',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
         'title': 'Administrative Unit'})

    code: Optional[list[Code]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AdministrativeUnit'], 'slot_uri': 'm8g:code'} })
    level: Optional[list[Code]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['AdministrativeUnit'], 'slot_uri': 'm8g:level'} })
    label: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['AdministrativeUnit', 'Jurisdiction'],
         'slot_uri': 'rdfs:label'} })


class Agent(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'foaf:Agent',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    agent_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Agent'],
         'slot_uri': 'dct:title'} })
    agent_type: Optional[list[Code]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Agent'], 'slot_uri': 'dct:type'} })


class Code(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'skos:Concept',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    pass


class ContactPoint(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'm8g:ContactPoint',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
         'title': 'Contact Point'})

    contact_page: Optional[list[Document]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:contactPage'} })
    email: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:email'} })
    telephone: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ContactPoint'], 'slot_uri': 'm8g:telephone'} })


class Document(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'foaf:Document',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    pass


class GenericDate(ConfiguredBaseModel):
    """
    Published vocabulary describes date, gYearMonth or gYear; official SHACL currently provides no constraints on this class.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'm8g:GenericDate',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml',
         'title': 'Generic Date'})

    pass


class Identifier(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'adms:Identifier',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    identifies: Optional[list[Person]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'm8g:identifies'} })
    issued_by: Optional[list[Agent]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'dct:creator'} })
    date_issued: Optional[list[date]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'dct:issued'} })
    notation: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'skos:notation'} })
    scheme_agency: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Identifier'], 'slot_uri': 'adms:schemeAgency'} })


class Jurisdiction(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dct:Jurisdiction',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    jurisdiction_identifier: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Jurisdiction'], 'slot_uri': 'dct:identifier'} })
    label: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['AdministrativeUnit', 'Jurisdiction'],
         'slot_uri': 'rdfs:label'} })


class Location(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'dct:Location',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    geographic_identifier: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Location'], 'slot_uri': 'rdfs:seeAlso'} })
    geographic_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Location'],
         'slot_uri': 'locn:geographicName'} })


class Person(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'person:Person',
         'from_schema': 'https://semiceu.github.io/Core-Person-Vocabulary/releases/2.1.2/linkml/core-person.yaml'})

    date_of_birth: Optional[list[str]] = Field(default=None, description="""Official SHACL constrains only the RDF node kind to Literal. The documented GenericDate union is not imposed pending a SEMIC Working Group decision.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:birthDate'} })
    contact_point: Optional[list[ContactPoint]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:contactPoint'} })
    date_of_death: Optional[list[str]] = Field(default=None, description="""Official SHACL constrains only the RDF node kind to Literal. The documented GenericDate union is not imposed pending a SEMIC Working Group decision.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:deathDate'} })
    domicile: Optional[list[Address]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:domicile'} })
    gender: Optional[list[Code]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:gender'} })
    matronymic_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'm8g:matronymicName'} })
    sex: Optional[list[Code]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'm8g:sex'} })
    alternative_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'dct:alternative'} })
    person_identifier: Optional[list[Identifier]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'dct:identifier'} })
    birth_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'person:birthName'} })
    citizenship: Optional[list[Jurisdiction]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:citizenship'} })
    country_of_birth: Optional[list[Location]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:countryOfBirth'} })
    country_of_death: Optional[list[Location]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:countryOfDeath'} })
    patronymic_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'person:patronymicName'} })
    place_of_birth: Optional[list[Location]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:placeOfBirth'} })
    place_of_death: Optional[list[Location]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:placeOfDeath'} })
    residency: Optional[list[Jurisdiction]] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Person'], 'slot_uri': 'person:residency'} })
    family_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'foaf:familyName'} })
    given_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'foaf:givenName'} })
    full_name: Optional[list[str]] = Field(default=None, json_schema_extra = { "linkml_meta": {'annotations': {'semic_unique_lang': {'tag': 'semic_unique_lang',
                                               'value': True}},
         'domain_of': ['Person'],
         'slot_uri': 'foaf:name'} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Address.model_rebuild()
AdministrativeUnit.model_rebuild()
Agent.model_rebuild()
Code.model_rebuild()
ContactPoint.model_rebuild()
Document.model_rebuild()
GenericDate.model_rebuild()
Identifier.model_rebuild()
Jurisdiction.model_rebuild()
Location.model_rebuild()
Person.model_rebuild()
