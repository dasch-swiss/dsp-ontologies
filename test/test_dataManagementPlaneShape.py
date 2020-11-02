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

class DataManagementPlan:
    def __init__(self):
        self.hasURL = '''[
                   a schema:URL ;
                   schema:url "https://snf.ch" ;
                ]'''
        self.isAvailable = '"false"^^xsd:boolean'


def makeDataManagementPlanData(test_plan):
    testData = prefix_list + '''<test-plan> rdf:type dsp-repo:DataManagementPlan .\n'''

    if hasattr(test_plan, 'hasURL'):
        testData += '''<test-plan> dsp-repo:hasURL''' + test_plan.hasURL + ' .\n'

    if hasattr(test_plan, 'isAvailable'):
        testData += '''<test-plan> dsp-repo:isAvailable''' + test_plan.isAvailable + ' .\n'

    return testData


#########################################################################
######### TEST CLASSES FOR DATA MANAGEMENT PLAN PROPERTIES ##############
#########################################################################

####### Tests for name of data management plan  #######
class planURLTestCase(unittest.TestCase):

    # should accept URL as string
    def test_planHasURL_As_String(self):
        testDMPlan = DataManagementPlan()
        testDMPlan.hasURL = '"http://example.com/"^^xsd:string'
        test_data = makeDataManagementPlanData(testDMPlan)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for name here


####### Tests for availability of data management plan  #######
class planAvailabilityTestCase(unittest.TestCase):

    # should accept isAvailable as boolean
    def test_planIsAvailable_As_Boolean(self):
        testDMPlan = DataManagementPlan()
        testDMPlan.isAvailable = '"true"^^xsd:boolean'
        test_data = makeDataManagementPlanData(testDMPlan)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail when isAvailable is given as string
    def test_planIsAvailable_As_String(self):
        testDMPlan = DataManagementPlan()
        testDMPlan.isAvailable = '"Yes"^^xsd:string'
        test_data = makeDataManagementPlanData(testDMPlan)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

        #TODO: add more tests for name here

if __name__ == '__main__':
    unittest.main()