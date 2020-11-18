import unittest
from pyshacl import validate
from os import path

ws = path.dirname(__file__)

dsp_repo_shape = path.join(ws, '../dsp-repository/v1/dsp-repository.shacl.ttl')

with open(path.join(ws, 'test_data/prefix_list.ttl'), 'r') as content_file:
    prefix_list = content_file.read()

galacticEmpire_organization = '''
                            <galactic-empire> rdf:type dsp-repo:Organization .
                            <galactic-empire> dsp-repo:hasName "Galactic Empire"^^xsd:string .
                            <galactic-empire> dsp-repo:hasEmail <info@galactic-empire.com> .
                            <galactic-empire> dsp-repo:hasAddress [
                                a schema:PostalAddress ;
                                schema:streetAddress "Death Star"^^xsd:string ;
                                schema:postalCode "0000"^^xsd:string ;
                                schema:addressLocality "In a galaxy far far away"^^xsd:string ;
                            ].

                            <galactic-empire> dsp-repo:hasURL[
                                   a schema:URL ;
                                   schema:url "http://www.galactic-empire.com/" ;
                               ] .
                            '''

class Person:
    def __init__(self):
        self.sameAs = '''[
                            a schema:URL ;
                            schema:url "https://darth-vador.galactic-empire.com" ;
                        ]'''
        self.hasGivenName = '"Anakin"'
        self.hasFamilyName = '"Skywalker"'
        self.hasEmail = '<darthVador@galactic-empire.com>'
        self.hasAddress = '''
                            [
                                a schema:PostalAddress ;
                                schema:streetAddress "Devastator, Imperial Navy"^^xsd:string ;
                                schema:postalCode "0000"^^xsd:string ;
                                schema:addressLocality "Galactic Republic"^^xsd:string ;
                            ]'''
        self.isMemberOf = '<galactic-empire>'
        self.hasJobTitle = '"Sith Lord"'
        # self.hasRole = '"Emperors Enforcer"'


def makePersonData(testPerson):

    testData = prefix_list + galacticEmpire_organization +\
               '''<darthVador> rdf:type dsp-repo:Person .\n'''

    if hasattr(testPerson, 'sameAs'):
        testData += '''<darthVador> dsp-repo:sameAs''' + testPerson.sameAs + ' .\n'

    if hasattr(testPerson, 'hasGivenName'):
        testData += '''<darthVador> dsp-repo:hasGivenName''' + testPerson.hasGivenName + ' .\n'

    if hasattr(testPerson, 'hasFamilyName'):
        testData += '''<darthVador> dsp-repo:hasFamilyName''' + testPerson.hasFamilyName + ' .\n'

    if hasattr(testPerson, 'hasEmail'):
        testData += '''<darthVador> dsp-repo:hasEmail''' + testPerson.hasEmail + ' .\n'

    if hasattr(testPerson, 'hasAddress'):
        testData += '''<darthVador> dsp-repo:hasAddress''' + testPerson.hasAddress + ' .\n'

    if hasattr(testPerson, 'isMemberOf'):
        testData += '''<darthVador> dsp-repo:isMemberOf''' + testPerson.isMemberOf + ' .\n'

    if hasattr(testPerson, 'hasJobTitle'):
        testData += '''<darthVador> dsp-repo:hasJobTitle''' + testPerson.hasJobTitle + ' .\n'

    # if hasattr(testPerson, 'hasRole'):
    #     testData += '''<darthVador> dsp-repo:hasRole''' + testPerson.hasRole + ' .\n'

    return testData

#########################################################################
######### TEST CLASSES FOR PERSON PROPERTIES ##############
#########################################################################


####### Tests for sameAs property of person #######
class personHasGivenNameTestCase(unittest.TestCase):

    # should not accept sameAs value as string
    def test_person_sameAs_as_String(self):
        person = Person()
        person.sameAs = '"http://anakin-skywalker.jedi.org"^^xsd:string '
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for sameAs here


####### Tests for given name of person #######
class personHasGivenNameTestCase(unittest.TestCase):

    # should not missing given name
    def test_person_givenName_missing(self):
        person = Person()
        delattr(person, 'hasGivenName')
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for given name here

####### Tests for family name of person #######
class personHasFamilyNameTestCase(unittest.TestCase):

    # should not missing family name
    def test_person_familyName_missing(self):
        person = Person()
        delattr(person, 'hasFamilyName')
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for family name here

####### Tests for email property of person #######
class personHasEmailTestCase(unittest.TestCase):

    # should accept email value as IRI
    def test_person_hasEmail_as_IRI(self):
        person = Person()
        person.hasEmail = '<anakinSkywalker@jedi.org>'
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail for email value as String
    def test_person_hasEmail_as_String(self):
        person = Person()
        person.hasEmail = '"anakinSkywalker@jedi.org"^^xsd:string'
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for hasEmail here

####### Tests for address of person #######
class personHasAddressTestCase(unittest.TestCase):

    # should accept more than one address given for a person
    def test_person_hasAddress_multiple(self):
        person = Person()
        test_data = makePersonData(person)
        test_data += '''<darthVador> dsp-repo:hasAddress [
                                                            a schema:PostalAddress ;
                                                            schema:streetAddress "Tatooine"^^xsd:string ;
                                                            schema:postalCode "xxxx"^^xsd:string ;
                                                            schema:addressLocality "in a galaxy far far away"^^xsd:string ;
                                                        ] .'''
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for address here

####### Tests for isMemberOf property of person #######
class personIsMemberOfTestCase(unittest.TestCase):

    # should fail when person's membership of organization is missing
    def test_person_isMemberOf_missing(self):
        person = Person()
        delattr(person, 'isMemberOf')
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for isMemberOf here

####### Tests for hasJobTitle property of person #######
class personHasJobTitleTestCase(unittest.TestCase):

    # should fail when hasJobTitle of person is missing
    def test_person_hasJobTitle_missing(self):
        person = Person()
        delattr(person, 'hasJobTitle')
        test_data = makePersonData(person)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for hasJobTitle here




if __name__ == '__main__':
    unittest.main()
