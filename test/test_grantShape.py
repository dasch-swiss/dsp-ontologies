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


with open('test_data/prefix_list.ttl', 'r') as content_file:
    prefix_list = content_file.read()

with open('test_data/organization.ttl', 'r') as content_file:
    test_organization = content_file.read()

with open('test_data/person.ttl', 'r') as content_file:
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