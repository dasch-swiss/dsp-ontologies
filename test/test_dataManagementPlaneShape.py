import unittest
from pyshacl import validate
from os import path

with open('test_data/prefix_list.ttl', 'r') as content_file:
    prefix_list = content_file.read()

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

    # should not accept URL as string
    def test_planHasURL_As_String(self):
        testDMPlan = DataManagementPlan()
        testDMPlan.hasURL = '"http://example.com/"^^xsd:string'
        test_data = makeDataManagementPlanData(testDMPlan)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

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