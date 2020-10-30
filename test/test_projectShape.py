import unittest
from pyshacl import validate
from os import path

prefix_list = '''
        # Metadata test project
        #

        @prefix dsp-repo: <http://ns.dasch.swiss/repository#> .
        @prefix knora-base: <http://www.knora.org/ontology/knora-base#> .
        @prefix knora-admin: <http://www.knora.org/ontology/knora-admin#> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix xml: <http://www.w3.org/XML/1998/namespace> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        @prefix foaf:<http://xmlns.com/foaf/0.1/> .
        @prefix vowl: <http://purl.org/vowl/spec/v2/> .
        @prefix prov: <http://www.w3.org/ns/prov#> .
        @prefix dc: <http://purl.org/dc/elements/1.1/> .
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix locn: <http://www.w3.org/ns/locn#> .
        @prefix vcard: <http://www.w3.org/2006/vcard/ns#> .
        @prefix schema: <https://schema.org/>.
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix unesco6: <http://skos.um.es/unesco6/> .
        @base <http://ns.dasch.swiss/repository#> .

     '''

dsp_repo_shape = '../dsp-repository/v1/dsp-repository.shacl.ttl'
shape_file = path.abspath(dsp_repo_shape)

default_discipline = '''
                    [
                       a schema:URL ;
                       schema:propertyID [
                           a schema:PropertyValue ;
                           schema:propertyID "SKOS UNESCO Nomenclature" ;
                       ] ;
                       schema:url "http://skos.um.es/unesco6/11" ;
                    ]'''

default_spatialCoverage = '''
                        [
                                a schema:Place ;
                                schema:url [
                                    a schema:URL ;
                                    schema:propertyID [
                                        a schema:PropertyValue ;
                                        schema:propertyID "Geonames" ;
                                    ] ;
                                    schema:url "https://www.geonames.org/6255148/europe.html" ;
                                ]
                        ]'''

default_URL = '''
            [
               a schema:URL ;
               schema:url "https://test.dasch.swiss/" ;
            ]'''

default_temporalCoverage = '''
                        [
                           a schema:URL ;
                           schema:propertyID [
                               a schema:PropertyValue ;
                               schema:propertyID "Chronontology Dainst" ;
                           ] ;
                           schema:url "http://chronontology.dainst.org/period/Ef9SyESSafJ1" ;
                        ]'''

test_Funder = '''
                <test-funder> rdf:type dsp-repo:Organization .
                # <test-funder> dsp-repo:hasIdentifier [
                #        a schema:URL ;
                #        schema:url "https://www.grid.ac/institutes/grid.17063.33" ;
                #    ].
                <test-funder> dsp-repo:hasName "University of Toronto"^^xsd:string .
                <test-funder> dsp-repo:hasEmail "info@universityoftoronto"^^xsd:string .
                <test-funder> dsp-repo:hasAddress [
                    a schema:PostalAddress ;
                    schema:streetAddress "University of Toronto Street"^^xsd:string ;
                    schema:postalCode "40000"^^xsd:string ;
                    schema:addressLocality "Toronto"^^xsd:string ;
                ].

                <test-funder> dsp-repo:hasURL[
                       a schema:URL ;
                       schema:url "http://www.utoronto.ca/" ;
                   ] .
            '''
def makeProjectData(hasName = '"test"^^xsd:string',
                    hasDescription = '"testen"^^xsd:string',
                    keywords = '"mathematics"^^xsd:string',
                    hasDiscipline = default_discipline,
                    hasStartDate = '"2000-07-26T21:32:52"^^xsd:dateTime',
                    hasTemporalCoverage = default_temporalCoverage,
                    hasSpatialCoverage = default_spatialCoverage,
                    hasFunder = "<test-funder>",
                    hasURL = default_URL,
                    hasShortcode = '"0000"^^xsd:string'):

    projectData = prefix_list + test_Funder + \
        '''
            <test-project> rdf:type dsp-repo:Project .
        ''' + \
        '''
            <test-project> dsp-repo:hasName
        ''' + hasName + ' .' + \
        '''
            <test-project> dsp-repo:hasDescription
        ''' + hasDescription + ' .' + \
        '''
            <test-project> dsp-repo:hasKeywords
        ''' + keywords + ' .' + \
        '''
            <test-project> dsp-repo:hasDiscipline
        ''' + hasDiscipline + ' .' + \
        '''
            <test-project> dsp-repo:hasStartDate
        ''' + hasStartDate  + ' .' + \
        '''
            <test-project> dsp-repo:hasTemporalCoverage
        ''' + hasTemporalCoverage  + ' .' + \
        '''
            <test-project> dsp-repo:hasSpatialCoverage
        ''' + hasSpatialCoverage + ' .' + \
        '''
            <test-project> dsp-repo:hasFunder
        ''' + hasFunder + ' .' + \
        '''
            <test-project> dsp-repo:hasURL
        ''' + hasURL + ' .' + \
        '''
            <test-project> dsp-repo:hasShortcode
        ''' + hasShortcode + ' .'

    return projectData


class ProjectShapeTestCase(unittest.TestCase):
    def test_projectHasName_with_String(self):
        test_data = makeProjectData()

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    def test_projectHasName_with_IRI(self):
        name = '<anIRI>'
        test_data = makeProjectData(name)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

if __name__ == '__main__':
    unittest.main()
