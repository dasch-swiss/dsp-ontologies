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

class Project:
    def __init__(self):
        self.hasName = '"test"^^xsd:string'
        self.hasDescription = '"testen"^^xsd:string'
        self.keywords = '"mathematics"^^xsd:string'
        self.hasDiscipline = '''
                                [
                                   a schema:URL ;
                                   schema:propertyID [
                                       a schema:PropertyValue ;
                                       schema:propertyID "SKOS UNESCO Nomenclature" ;
                                   ] ;
                                   schema:url "http://skos.um.es/unesco6/11" ;
                                ]'''

        self.hasStartDate = '"2000-07-26T21:32:52"^^xsd:dateTime'
        self.hasTemporalCoverage = '''
                                [
                                   a schema:URL ;
                                   schema:propertyID [
                                       a schema:PropertyValue ;
                                       schema:propertyID "Chronontology Dainst" ;
                                   ] ;
                                   schema:url "http://chronontology.dainst.org/period/Ef9SyESSafJ1" ;
                                ]'''

        self.hasFunder = "<test-funder>"
        self.hasURL =  '''
                            [
                               a schema:URL ;
                               schema:url "https://test.dasch.swiss/" ;
                            ]'''

        self.hasShortcode = '"0000"^^xsd:string'

        self.hasSpatialCoverage = '''
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



def makeProjectData(testProject):

    projectData = prefix_list + test_Funder + \
        '''
            <test-project> rdf:type dsp-repo:Project .
        ''' + \
        '''
            <test-project> dsp-repo:hasName
        ''' + testProject.hasName + ' .' + \
        '''
            <test-project> dsp-repo:hasDescription
        ''' + testProject.hasDescription + ' .' + \
        '''
            <test-project> dsp-repo:hasKeywords
        ''' + testProject.keywords + ' .' + \
        '''
            <test-project> dsp-repo:hasDiscipline
        ''' + testProject.hasDiscipline + ' .' + \
        '''
            <test-project> dsp-repo:hasStartDate
        ''' + testProject.hasStartDate  + ' .' + \
        '''
            <test-project> dsp-repo:hasTemporalCoverage
        ''' + testProject.hasTemporalCoverage  + ' .' + \
        '''
            <test-project> dsp-repo:hasSpatialCoverage
        ''' + testProject.hasSpatialCoverage + ' .' + \
        '''
            <test-project> dsp-repo:hasFunder
        ''' + testProject.hasFunder + ' .' + \
        '''
            <test-project> dsp-repo:hasURL
        ''' + testProject.hasURL + ' .' + \
        '''
            <test-project> dsp-repo:hasShortcode
        ''' + testProject.hasShortcode + ' .'

    return projectData


############################################################
######### TEST CLASSES FOR PROJECT PROPERTIES ##############
############################################################

####### Tests for project name #######
class ProjectNameTestCase(unittest.TestCase):

    # should accept name as string
    def test_projectHasName_with_String(self):
        testProject = Project()
        testProject.hasName = '"a name"^^xsd:string'
        test_data = makeProjectData(testProject)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail for name as IRI
    def test_projectHasName_with_IRI(self):
        testProject = Project()
        testProject.hasName = '<anIRI>'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # should fail for empty name
    def test_projectHasName_empty(self):
        testProject = Project()
        testProject.hasName = '""^^xsd:string'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

####### Tests for project shortcode #######
class ProjectShortCodeTestCase(unittest.TestCase):
    # should accept shortcode as string
    def test_projectShortCode_String(self):
        testProject = Project()
        testProject.hasShortcode = '"0801"^^xsd:string'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail for shortcode as integer
    def test_projectShortCode_integer(self):
        testProject = Project()
        testProject.hasShortcode = '"0801"^^xsd:int'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # should fail for empty shortcode
    def test_projectShortCode_empty(self):
        testProject = Project()
        testProject.hasShortcode = '""^^xsd:string'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

if __name__ == '__main__':
    unittest.main()
