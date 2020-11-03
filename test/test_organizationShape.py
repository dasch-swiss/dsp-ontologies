import unittest
from pyshacl import validate
from os import path

dsp_repo_shape = '../dsp-repository/v1/dsp-repository.shacl.ttl'
shape_file = path.abspath(dsp_repo_shape)

with open('test_data/prefix_list.ttl', 'r') as content_file:
    prefix_list = content_file.read()

class Organization:
    def __init__(self):
        self.hasName = '"test"^^xsd:string'
        self.hasEmail = '<test@example.com>'
        self.hasAddress = '''[
                            a schema:PostalAddress ;
                            schema:streetAddress "University of Toronto Street"^^xsd:string ;
                            schema:postalCode "40000"^^xsd:string ;
                            schema:addressLocality "Toronto"^^xsd:string ;
                            ]'''

        self.hasURL =  '''[
                           a schema:URL ;
                           schema:url "http://www.utoronto.ca/" ;
                        ]'''



def makeOrganizationData(testOrganization):

    organizationData = prefix_list + '''<test-funder> rdf:type dsp-repo:Organization .\n'''

    if hasattr(testOrganization, 'hasName'):
        organizationData += '''<test-funder> dsp-repo:hasName''' + testOrganization.hasName + ' .\n'

    if hasattr(testOrganization, 'hasEmail'):
        organizationData += '''<test-funder> dsp-repo:hasEmail''' + testOrganization.hasEmail + ' .\n'

    if hasattr(testOrganization, 'hasAddress'):
        organizationData += '''<test-funder> dsp-repo:hasAddress''' + testOrganization.hasAddress + ' .\n'

    if hasattr(testOrganization, 'hasURL'):
        organizationData += '''<test-funder> dsp-repo:hasURL''' + testOrganization.hasURL + ' .\n'

    return organizationData


############################################################
######### TEST CLASSES FOR ORGANIZATION PROPERTIES ##############
############################################################

####### Tests for name of organization  #######
class organizationNameTestCase(unittest.TestCase):

    # should accept name as string
    def test_organizationHasName_As_String(self):
        testOrganization = Organization()
        testOrganization.hasName = '"a name"^^xsd:string'
        test_data = makeOrganizationData(testOrganization)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for name here

####### Tests for email of organization  #######
class organizationEmailTestCase(unittest.TestCase):

    # should accept email given as IRI
    def test_organizationHasEmail_As_IRI(self):
        testOrganization = Organization()
        testOrganization.hasEmail = '<test@example.com>'
        test_data = makeOrganizationData(testOrganization)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # TODO: add more tests for email here

####### Tests for address of organization  #######
class organizationAddressTestCase(unittest.TestCase):

    # should not accept the address as string
    def test_organizationHasAddress_As_String(self):
        testOrganization = Organization()
        testOrganization.hasAddress = '"Outer Rim territories, Naboo"^^xsd:string'
        test_data = makeOrganizationData(testOrganization)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for address here

####### Tests for URL of organization  #######
class organizationURLTestCase(unittest.TestCase):

    # should accept the URL as string
    def test_organizationHasURL_As_String(self):
        testOrganization = Organization()
        testOrganization.hasURL = '"http://www.jediSchool.org/"^^xsd:string'
        test_data = makeOrganizationData(testOrganization)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for URL here

if __name__ == '__main__':
    unittest.main()
