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

### Test Suit

The python Unittest framework uses [pySHACL](https://github.com/RDFLib/pySHACL) library for SHACL validations. 
To install the requirements, run:

```
$ make install-requirements
```

The unit tests can be executed standalone in a python environment or using [Bazel](https://bazel.build/) build tools. 
If you would like to run the tests using Bazel, [install Bazel build tools](https://docs.bazel.build/versions/master/install.html). On macOs run:

```
$ brew install bazel
```

Alternatively, you can install Bazel build tools using 
[bazelisk](https://github.com/bazelbuild/bazelisk) which is
a wrapper to the `bazel` binary. It will, when `bazel` is run on the command line,
automatically install the supported Bazel version, defined in the `.bazelversion`
file in the root of the `dsp-ontologies` repository. With npm installed, you can get bazelisk with
 
```
$ npm install -g @bazel/bazelisk
```
 
Having Bazel and pySHACL installed, to run all tests, do:

```
$ make test
```

To run a specific test using bazel, for example `test_projectShape`, run:

```
$ bazel test //test:test_projectShape
```

