import unittest
from pyshacl import validate
from os import path

ws = path.dirname(__file__)

dsp_repo_shape = path.join(ws, '../dsp-repository/v1/dsp-repository.shacl.ttl')

with open(path.join(ws, 'test_data/prefix_list.ttl'), 'r') as content_file:
    prefix_list = content_file.read()

with open(path.join(ws, 'test_data/organization.ttl'), 'r') as content_file:
    test_organization = content_file.read()

with open(path.join(ws, 'test_data/person.ttl'), 'r') as content_file:
    test_person = content_file.read()

class Grant:
    def __init__(self):
        self.hasName = '"test"^^xsd:string'
        self.hasNumber = '"0123456789"^^xsd:string'
        self.hasFunder = "<test-funder>"
        self.hasURL =  '''[
                           a schema:URL ;
                           schema:url "http://p3.snf.ch/testproject" ;
                        ]'''


def makeGrantData(testGrant):
    grantData = prefix_list + test_organization + test_person + '''<test-grant> rdf:type dsp-repo:Grant . \n'''

    if hasattr(testGrant, 'hasName'):
        grantData += '''<test-grant> dsp-repo:hasName''' + testGrant.hasName + ' .\n'

    if hasattr(testGrant, 'hasNumber'):
        grantData += '''<test-grant> dsp-repo:hasNumber''' + testGrant.hasNumber + ' .\n'

    if hasattr(testGrant, 'hasFunder'):
        grantData += '''<test-grant> dsp-repo:hasFunder''' + testGrant.hasFunder + ' .\n'

    if hasattr(testGrant, 'hasURL'):
        grantData += '''<test-grant> dsp-repo:hasURL''' + testGrant.hasURL + ' .\n'

    return grantData


############################################################
######### TEST CLASSES FOR GRANT PROPERTIES ##############
############################################################

####### Tests for name of grant  #######
class grantNameTestCase(unittest.TestCase):

    # should accept name as string
    def test_grantHasName_As_String(self):
        testGrant = Grant()
        testGrant.hasName = '"a name"^^xsd:string'
        test_data = makeGrantData(testGrant)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for name here

####### Tests for number of grant  #######
class grantNumberTestCase(unittest.TestCase):

    # should accept name as string
    def test_grantHasNumber_As_Integer(self):
        testGrant = Grant()
        testGrant.hasName = '"123"^^xsd:int'
        test_data = makeGrantData(testGrant)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for number here

####### Tests for name of grant  #######
class grantFunderTestCase(unittest.TestCase):

    # should accept a person as funder
    def test_grantHasFunder_is_person(self):
        testGrant = Grant()
        testGrant.hasFunder = '<test-jones>'
        test_data = makeGrantData(testGrant)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # TODO: add more tests for funder here

####### Tests for URL of grant  #######
class grantURLTestCase(unittest.TestCase):

    # should not accept the URL as string
    def test_organizationHasURL_As_String(self):
        testGrant = Grant()
        testGrant.hasURL = '"http://www.jediSchool.org/"^^xsd:string'
        test_data = makeGrantData(testGrant)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for URL here


if __name__ == '__main__':
    unittest.main()