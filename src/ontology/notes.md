# Extra steps added for Reasoning chemical concentrations module

After this branch is completed we can merge these extra instructions into our wiki page on compiling CDNO.

## Step 1: Merge

merge modules/nutritional_components_framework_full.owl and modules/chemical_concentration.owl and sugar_derivatives into an intermediate file and reason on it.

```
robot merge --input modules/nutritional_components_framework_full.owl --input modules/chemical_concentration.owl --input modules/sugar_derivatives.owl --output modules/merged_modules/merged_cdno_modules.owl
```

## Step 2: Reason the merged file with create-new-ontology-with-annotations
This works we can do this and merge this into cdno-edit.owl instead of sugar_derivatives chemical_concentration and nutritional_components_framework_full separately as we doing in master.
```
robot reason --reasoner ELK --create-new-ontology-with-annotations true --input modules/merged_modules/merged_cdno_modules.owl annotate --ontology-iri "http://purl.obolibrary.org/obo/cdno/modules/merged_modules/reasoned_cdno_modules.owl" --version-iri "http://purl.obolibrary.org/obo/cdno/modules/merged_modules/reasoned_cdno_modules.owl" --output modules/merged_modules/reasoned_cdno_modules.owl
```


# OLD

## Test Merge reasoned module with chemical_concentration

to see if we put the equivalence axioms back in

```
robot merge --input modules/merged_modules/reasoned_cdno_modules.owl --input modules/chemical_concentration.owl --output modules/merged_modules/merged_cdno_modules_tmp.owl
```




### Command to create new owl file with only reasoned axioms
```
robot reason --reasoner ELK --create-new-ontology true --input cdno-edit.owl annotate --ontology-iri "http://purl.obolibrary.org/obo/cdno/modules/reasoned_axioms.owl" --version-iri "http://purl.obolibrary.org/obo/cdno/modules/reasoned_axioms.owl" --output modules/reasoned_axioms.owl
```

the above sort of worked when we added `/Users/kai/Desktop/software/cdno/src/ontology/modules/reasoned_axioms.owl` as a direct import to CDNO-edit.owl.


# Try without the create-new-ontology
```
robot reason --reasoner ELK --input cdno-edit.owl annotate --ontology-iri "http://purl.obolibrary.org/obo/cdno/modules/reasoned_axioms.owl" --version-iri "http://purl.obolibrary.org/obo/cdno/modules/reasoned_axioms.owl" --output modules/reasoned_axioms_without_create.owl
```

Proposal: reason the modules/chemical_concentration.owl file and make a `modules/chemical_concentration_reasoned.owl` file and import that into CDNO-edit instead of the `chemical_concentration.owl`. To make this work we'd need to reason the chemical with the full `dietary nutritional component` hierarchy but filter only the chemical concentrations.

For this plan to work we'd need subset tags on the chemical_concentration terms. could be done with robot I wonder if we can do it directly in the DOSDP that'd be ideal so we don't have to add another step. Once we have those chemical_concentration terms tagged we merge them with the dietary nutritional component hierarchy in an intermediate file and we reason the whole thing. Then we retrieve just the reasoned chemical_concentration terms using filter and that should be the new module.





# reason the merged file without create true

```
robot reason --reasoner ELK --input temporary/test_merge_ncf_cc_sd.owl --output temporary/reasoned_axioms_without_create.owl
```

# reason the merged file with create true

```
robot reason --reasoner ELK --create-new-ontology true --input temporary/test_merge_ncf_cc_sd.owl --output temporary/reasoned_axioms_with_create.owl
```
