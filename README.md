# dsp-ontologies
DaSCH Service Platform Ontologies

## Ontologies

### dsp-repository

The `dsp-repository` ontology models project specific metadata.

Each project hosted on the DSP (DaSCH Service Platform) must provide metadata conforming to this ontology.
This will allow project data hosted on the DSP to be findable and searchable by a well-defined set of metadata.  
It will furthermore provide human-readable information that can be displayed to the user browsing the DSP.


## Other Data

### Examples

A valid example set of project metadata is provided in `example/example-metadata.ttl`.
Projects can model their data according to this example.

### Test Suit

A set of deliberately invalid data is yet to be added.  
This data can then be used for validation test suits.


## Validation

Ontologies and example data can be validated, using Apache Jena's RIOT and SHACL validator.

### Prerequisites

Requires:
- GNU make
- GNU wget

Install:  
Before validating for the fist time, install the Jena tools, by running `make install`.

### Validate

To validate the ontology and example data, run `make validate`.

If the data validates, you should get
```shell
@prefix rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix sh:    <http://www.w3.org/ns/shacl#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .

[ a            sh:ValidationReport ;
  sh:conforms  true
] .
```
