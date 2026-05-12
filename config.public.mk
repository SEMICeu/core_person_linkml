# config.public.mk

# This file is public in git. No sensitive info allowed.

###### schema definition variables, used by justfile

# Note:
# - just works fine with quoted variables of dot-env files like this one
LINKML_SCHEMA_NAME="core_person"
LINKML_SCHEMA_AUTHOR="Nico Matentzoglu <nicolas.matentzoglu@gmail.com>"
LINKML_SCHEMA_DESCRIPTION="LinkML approximation of SEMIC Core Person Vocabulary 2.1.1"
LINKML_SCHEMA_SOURCE_DIR="src/core_person/schema"

###### linkml generator variables, used by justfile

## gen-project configuration file
LINKML_GENERATORS_CONFIG_YAML=config.yaml

## pass args if gendoc ignores config.yaml (i.e. --no-mergeimports)
LINKML_GENERATORS_DOC_ARGS=

## pass args to workaround genowl rdfs config bug (linkml#1453)
##   (i.e. --no-type-objects --no-metaclasses --metadata-profile=rdfs)
# LINKML_GENERATORS_OWL_ARGS="--no-type-objects --no-metaclasses --metadata-profile=rdfs"
#
# --no-use-native-uris flips class/slot OWL subjects from the schema-internal
# `cpv:` namespace to the external SEMIC IRIs (`person:Person`, `m8g:`,
# `foaf:`, …), matching the upstream Core Person OWL surface. See CLAUDE.md
# and COMPARISON.md ("OWL: what does not match") for the residual
# `skos:exactMatch cpv:Foo` class back-pointer this flag does not fix.
LINKML_GENERATORS_OWL_ARGS="--no-use-native-uris"

## pass args to pydantic generator which isn't supported by gen-project
## https://github.com/linkml/linkml/issues/2537
LINKML_GENERATORS_PYDANTIC_ARGS=
