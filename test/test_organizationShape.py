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

class Organization:
    def __init__(self):
        self.hasName = '"test"^^xsd:string'
        self.hasEmail = '"test@example.com"^^xsd:string'
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

    # should accept the address as string
    def test_organizationHasAddress_As_String(self):
        testOrganization = Organization()
        testOrganization.hasAddress = '"Outer Rim territories, Naboo"^^xsd:string'
        test_data = makeOrganizationData(testOrganization)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

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
        self.assertTrue(conforms)

    # TODO: add more tests for URL here

if __name__ == '__main__':
    unittest.main()
