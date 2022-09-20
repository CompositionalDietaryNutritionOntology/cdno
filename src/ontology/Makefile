# ----------------------------------------
# Makefile for cdno
# Generated using ontology-starter-kit
# ODK Version: v1.2.22
# ----------------------------------------
# <do not edit above this line>

# ----------------------------------------
# Standard Constants
# ----------------------------------------
# these can be overwritten on the command line

URIBASE=                    http://purl.obolibrary.org/obo
ONT=                        cdno
ONTBASE=                    $(URIBASE)/$(ONT)
EDIT_FORMAT=                owl
SRC =                       $(ONT)-edit.$(EDIT_FORMAT)
CATALOG=                    catalog-v001.xml
ROBOT=                      robot --catalog $(CATALOG)
RELEASEDIR=                 ../..
REPORTDIR=                  reports
TMPDIR=                     tmp
SPARQLDIR =                 ../sparql
REPORT_FAIL_ON =            None
OBO_FORMAT_OPTIONS =
SPARQL_VALIDATION_CHECKS =  equivalent-classes trailing-whitespace owldef-self-reference xref-syntax nolabels
SPARQL_EXPORTS =            basic-report class-count-by-prefix edges xrefs obsoletes synonyms
ODK_VERSION =               v1.2.22

TODAY ?= $(shell date +%Y-%m-%d)
OBODATE ?= $(shell date +'%d:%m:%Y %H:%M')
# seed.txt contains all referenced entities
IMPORTSEED=seed.txt
SRCMERGED=tmp/merged-$(SRC)
SIMPLESEED=simple_seed.txt
PRESEED=tmp/pre_seed.txt

FORMATS = $(sort  owl obo owl)
FORMATS_INCL_TSV = $(sort $(FORMAT) tsv)
RELEASE_ARTEFACTS = $(sort  full base base full)

# ----------------------------------------
# Top-level targets
# ----------------------------------------

.PHONY: .FORCE
all: odkversion all_imports all_main all_subsets sparql_test all_reports all_assets
test: odkversion sparql_test all_reports
	$(ROBOT) reason --input $(SRC) --reasoner ELK  --equivalent-classes-allowed all --exclude-tautologies structural --output test.owl && rm test.owl && echo "Success"

odkversion:
	echo "ODK Makefile version: $(ODK_VERSION) (this is the version of the ODK with which this Makefile was generated, not the version of the ODK you are running)" &&\
	echo "ROBOT version (ODK): " && $(ROBOT) --version

$TMPDIR:
	mkdir -p $@

## -- main targets --
##
## By default this is the cross-product of {ont, ont-base} x FORMATS

MAIN_PRODUCTS = $(sort $(foreach r,$(RELEASE_ARTEFACTS), $(ONT)-$(r)) $(ONT))
MAIN_GZIPPED =
MAIN_FILES = $(foreach n,$(MAIN_PRODUCTS), $(foreach f,$(FORMATS), $(n).$(f))) $(MAIN_GZIPPED)

all_main: $(MAIN_FILES)

## -- import targets --
##
## By default this is the cross-product of IMPORT_MODULES x FORMATS


IMPORTS = ro bfo pato obi uo envo po agro foodon #chebi

IMPORT_ROOTS = $(patsubst %, imports/%_import, $(IMPORTS))
IMPORT_OWL_FILES = $(foreach n,$(IMPORT_ROOTS), $(n).owl)
IMPORT_FILES = $(IMPORT_OWL_FILES)


all_imports: $(IMPORT_FILES)

## -- subset targets --
##
## By default this is the cross-product of SUBSETS x FORMATS
## Note we also include TSV as a format


SUBSETS =

SUBSET_ROOTS = $(patsubst %, subsets/%, $(SUBSETS))
SUBSET_FILES = $(foreach n,$(SUBSET_ROOTS), $(foreach f,$(FORMATS_INCL_TSV), $(n).$(f)))

all_subsets: $(SUBSET_FILES)

OBO_REPORT = $(SRC)-obo-report
REPORTS = $(OBO_REPORT)
REPORT_FILES = $(patsubst %, $(REPORTDIR)/%.tsv, $(REPORTS))

#############################################################
#### -- dosdp pattern targets -- ####

## DOSDP pattern targets modified from ENVO version
MODS = chemical_concentration
ALL_MODS_OWL = $(patsubst %, modules/%.owl, $(MODS)) # in CDNO mods dir is for the owl files envo's mod dir is both owl files and their csvs. maybe want to rename ALL_MODS_OWL because it's not all owl files in modules that will be complied this way perhaps we'll see when we add the the robot compile lines to make.
ALL_MODS_CSV = $(patsubst %, modules/%.csv, $(MODS))

## Modules make targets modified from ENVO's version
all_modules: all_modules_owl #all_modules_obo
all_modules_owl: $(ALL_MODS_OWL)


# Targets for DOSDP modules #this will work when it's only the DOSDP but it'll will maybe apply this same pattern to all owl files in modules/ or at least those called from all_modules
modules/%.owl: templates/%.csv patterns/%.yaml curie_map.yaml
	if [ true = true ]; then dosdp-tools generate --table-format=csv --template=patterns/$*.yaml --outfile=modules/$*.tmp.owl --obo-prefixes=true --infile=templates/$*.csv; fi
	$(ROBOT) annotate --input modules/$*.tmp.owl -O http://purl.obolibrary.org/obo/cdno/modules/$*.owl --output modules/$*.owl && rm modules/$*.tmp.owl



all_reports: all_reports_onestep $(REPORT_FILES)

## -- all files/assets --

ASSETS = \
  $(IMPORT_FILES) \
  $(MAIN_FILES) \
  $(REPORT_FILES) \
  $(SUBSET_FILES)

all_assets: $(ASSETS)

show_assets:
	echo $(ASSETS)
	du -sh $(ASSETS)


# ----------------------------------------
# Release Management
# ----------------------------------------

KEEPRELATIONS=keeprelations.txt
ONTOLOGYTERMS=ontologyterms.txt

# This should be executed by the release manager whenever time comes to make a release.
# It will ensure that all assets/files are fresh, and will copy to release folder
prepare_release: $(ASSETS) $(PATTERN_RELEASE_FILES)
	rsync -R $(ASSETS) $(RELEASEDIR) &&\
  rm -f $(MAIN_FILES) $(SRCMERGED) &&\
  echo "Release files are now in $(RELEASEDIR) - now you should commit, push and make a release on your git hosting site such as GitHub or GitLab"

prepare_initial_release: prepare_release
	cd $(RELEASEDIR) && git add $(ASSETS)

# ----------------------------------------
# Export formats
# ----------------------------------------


$(ONT)-full.obo: $(ONT)-full.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
$(ONT)-base.obo: $(ONT)-base.owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
# Main release artefacts
$(ONT).owl: $(ONT)-full.owl
	$(ROBOT) annotate --input $< --ontology-iri $(URIBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ \
		convert -o $@.tmp.owl && mv $@.tmp.owl $@

$(ONT).obo: $(ONT).owl
	$(ROBOT) convert --input $< --check false -f obo $(OBO_FORMAT_OPTIONS) -o $@.tmp.obo && grep -v ^owl-axioms $@.tmp.obo > $@ && rm $@.tmp.obo
# ----------------------------------------
# Initiating Step: Reason over source
# ----------------------------------------

ANNOTATE_VERSION_IRI = annotate -V $(ONTBASE)/releases/$(TODAY)/$@.owl

# by default we use ELK to perform a reason-relax-reduce chain
# after that we annotate the ontology with the release versionInfo

OTHER_SRC =


$(ONTOLOGYTERMS): $(SRC) $(OTHER_SRC)
	touch $(ONTOLOGYTERMS) && \
	$(ROBOT) query --use-graphs true -f csv -i $< --query ../sparql/cdno_terms.sparql $@








# base: OTHER sources of interest, such as definitions owl
$(ONT)-base.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) remove --input $< --select imports --trim false \
		merge $(patsubst %, -i %, $(OTHER_SRC)) \
		annotate --annotation http://purl.org/dc/elements/1.1/type http://purl.obolibrary.org/obo/IAO_8000001 \
		--ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ \
		--output $@.tmp.owl && mv $@.tmp.owl $@

# Full: The full artefacts with imports merged, reasoned
$(ONT)-full.owl: $(SRC) $(OTHER_SRC)
	$(ROBOT) merge --input $< \
		reason --reasoner ELK --equivalent-classes-allowed all --exclude-tautologies structural \
		relax \
		reduce -r ELK \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@

# ----------------------------------------
# Import modules
# ----------------------------------------
# Most ontologies are modularly constructed using portions of other ontologies
# These live in the imports/ folder

$(SRCMERGED): $(SRC)
	$(ROBOT) remove --input $< --select imports --trim false \
		merge  $(patsubst %, -i %, $(OTHER_SRC)) -o $@

$(PRESEED): $(SRCMERGED)
	$(ROBOT) query -f csv -i $< --query ../sparql/terms.sparql $@.tmp &&\
	cat $@.tmp | sort | uniq >  $@

$(SIMPLESEED): $(SRCMERGED) $(ONTOLOGYTERMS)
	$(ROBOT) query -f csv -i $< --query ../sparql/simple-seed.sparql $@.tmp &&\
	cat $@.tmp $(ONTOLOGYTERMS) | sort | uniq >  $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SubsetProperty" >> $@ &&\
	echo "http://www.geneontology.org/formats/oboInOwl#SynonymTypeProperty" >> $@


$(IMPORTSEED): $(PRESEED)
	@if [ $(IMP) = true ]; then cat $(PRESEED) | sort | uniq > $@; fi


# Generate terms.txt for each import.  (Assume OBO-style Possibly hacky step?)
# Should be able to drop this if robot can just take a big messy list of terms as input.

imports/%_terms_combined.txt: $(IMPORTSEED) imports/%_terms.txt
	@if [ $(IMP) = true ]; then cat $^ | grep -v ^# | sort | uniq >  $@; fi

# -- Generate Import Modules --
#
# This pattern uses ROBOT to generate an import module
imports/%_import.owl: mirror/%.owl imports/%_terms_combined.txt
	@if [ $(IMP) = true ]; then $(ROBOT) extract -i $< -T imports/$*_terms_combined.txt --force true --method BOT \
		query --update ../sparql/inject-subset-declaration.ru \
		annotate --ontology-iri $(ONTBASE)/$@ --version-iri $(ONTBASE)/releases/$(TODAY)/$@ --output $@.tmp.owl && mv $@.tmp.owl $@; fi
.PRECIOUS: imports/%_import.owl

# convert imports to obo.
# this can be useful for spot-checks and diffs.
# we set strict mode to false by default. For discussion see https://github.com/owlcs/owlapi/issues/752
imports/%_import.obo: imports/%_import.owl
	@if [ $(IMP) = true ]; then $(ROBOT) convert --check false -i $< -f obo -o $@.tmp.obo && mv $@.tmp.obo $@; fi


# ----------------------------------------
# Mirroring upstream ontologies
# ----------------------------------------
#

IMP=true # Global parameter to bypass import generation
MIR=true # Global parameter to bypass mirror generation


## ONTOLOGY: ro
## Copy of ro is re-downloaded whenever source changes
mirror/ro.trigger: $(SRC)

mirror/ro.owl: mirror/ro.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/ro.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: bfo
## Copy of bfo is re-downloaded whenever source changes
mirror/bfo.trigger: $(SRC)

mirror/bfo.owl: mirror/bfo.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/bfo.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: pato
## Copy of pato is re-downloaded whenever source changes
mirror/pato.trigger: $(SRC)

mirror/pato.owl: mirror/pato.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/pato.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: obi
## Copy of obi is re-downloaded whenever source changes
mirror/obi.trigger: $(SRC)

mirror/obi.owl: mirror/obi.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/obi.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: uo
## Copy of uo is re-downloaded whenever source changes
mirror/uo.trigger: $(SRC)

mirror/uo.owl: mirror/uo.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/uo.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: envo
## Copy of envo is re-downloaded whenever source changes
mirror/envo.trigger: $(SRC)

mirror/envo.owl: mirror/envo.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/envo.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl


## ONTOLOGY: po
## Copy of po is re-downloaded whenever source changes
mirror/po.trigger: $(SRC)

mirror/po.owl: mirror/po.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/po.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl



## ONTOLOGY: agro
## Copy of agro is re-downloaded whenever source changes
mirror/agro.trigger: $(SRC)

mirror/agro.owl: mirror/agro.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/agro.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl



## ONTOLOGY: foodon
## Copy of foodon is re-downloaded whenever source changes
mirror/foodon.trigger: $(SRC)

mirror/foodon.owl: mirror/foodon.trigger
	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/foodon.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi

.PRECIOUS: mirror/%.owl



## ONTOLOGY: chebi
## Copy of chebi is re-downloaded whenever source changes
#mirror/chebi.trigger: $(SRC)
#
#mirror/chebi.owl: mirror/chebi.trigger
#	@if [ $(MIR) = true ] && [ $(IMP) = true ]; then $(ROBOT) convert -I $(URIBASE)/chebi.owl -o $@.tmp.owl && mv $@.tmp.owl $@; fi
#
#.PRECIOUS: mirror/%.owl

# ENVO Makefile's verion of CHEBI import
# chebi.owl is large and the owlapi often times out when reading it; use the obo instead
#mirror/chebi-local.owl:
#	wget --no-check-certificate $(URIBASE)/chebi.owl -O $@ && touch $@
#mirror/chebi.owl: mirror/chebi-local.owl
#	owltools  --no-debug $< --log-debug --remove-annotation-assertions -l --remove-dangling-annotations --make-subset-by-properties -f $(KEEPRELS)  -o $@
#.PRECIOUS: mirror/%.owl

mirror/chebi-local.owl:
	wget --no-check-certificate $(URIBASE)/chebi.owl -O $@ && touch $@
mirror/chebi.owl: mirror/chebi-local.owl
	owltools  --no-debug $< --log-debug -o $@
.PRECIOUS: mirror/%.owl


# ----------------------------------------
# Subsets
# ----------------------------------------
subsets/%.tsv: subsets/%.owl
	$(ROBOT) query -f tsv -i $< -s ../sparql/labels.sparql $@
subsets/%.owl: $(ONT).owl
	owltools --use-catalog $< --extract-ontology-subset --fill-gaps --subset $* -o $@.tmp.owl && mv $@.tmp.owl $@


# ----------------------------------------
# Release
# ----------------------------------------
# copy from staging area (this directory) to top-level
release: $(ONT).owl $(ONT).obo
	cp $^ $(RELEASEDIR) && cp imports/* $(RELEASEDIR)/imports

# ----------------------------------------
# Sparql queries: Q/C
# ----------------------------------------

# these live in the ../sparql directory, and have suffix -violation.sparql
# adding the name here will make the violation check live.
# NOTE: these will soon be phased out and replaced by robot-report

#  run all violation checks
SPARQL_VALIDATION_QUERIES = $(foreach V,$(SPARQL_VALIDATION_CHECKS),$(SPARQLDIR)/$V-violation.sparql)
sparql_test: $(SRC)
	$(ROBOT) verify  --catalog catalog-v001.xml -i $< --queries $(SPARQL_VALIDATION_QUERIES) -O reports/

# ----------------------------------------
# ROBOT report
# ----------------------------------------
reports/%-obo-report.tsv: %
	$(ROBOT) report -i $< --fail-on $(REPORT_FAIL_ON) --print 5 -o $@

# ----------------------------------------
# Sparql queries: Exports
# ----------------------------------------

SPARQL_EXPORTS_ARGS = $(foreach V,$(SPARQL_EXPORTS),-s $(SPARQLDIR)/$V.sparql reports/$V.tsv)
# This combines all into one single command
all_reports_onestep: $(SRC)
	$(ROBOT) query -f tsv -i $< $(SPARQL_EXPORTS_ARGS)


# ----------------------------------------
# Docker (experimental)
# ----------------------------------------
IM=build-$(ONT)
build-docker:
	docker build -t $(ONT) .



update_repo:
	sh ../scripts/update_repo.sh

include cdno.Makefile
