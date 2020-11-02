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

test_project = '''
                ### test project ###
                <test-project> rdf:type dsp-repo:Project .
                <test-project> dsp-repo:hasName "Testprojektname (test)"^^xsd:string .
                <test-project> dsp-repo:hasDescription "Dies ist ein Testprojekt...alle Properties wurden verwendet, um diese zu testen"^^xsd:string .
                <test-project> dsp-repo:hasKeywords "mathematics"^^xsd:string .
                <test-project> dsp-repo:hasDiscipline [
                   a schema:URL ;
                   schema:propertyID [
                       a schema:PropertyValue ;
                       schema:propertyID "SKOS UNESCO Nomenclature" ;
                   ] ;
                   schema:url "http://skos.um.es/unesco6/11" ;
                ] .
                <test-project> dsp-repo:hasStartDate "2000-07-26T21:32:52"^^xsd:dateTime .
                <test-project> dsp-repo:hasEndDate "2001-01-26T21:32:52"^^xsd:dateTime .
                <test-project> dsp-repo:hasTemporalCoverage [
                   a schema:URL ;
                   schema:propertyID [
                       a schema:PropertyValue ;
                       schema:propertyID "Chronontology Dainst" ;
                   ] ;
                   schema:url "http://chronontology.dainst.org/period/Ef9SyESSafJ1" ;
                ] .
                <test-project> dsp-repo:hasSpatialCoverage [
                        a schema:Place ;
                        schema:url [
                            a schema:URL ;
                            schema:propertyID [
                                a schema:PropertyValue ;
                                schema:propertyID "Geonames" ;
                            ] ;
                            schema:url "https://www.geonames.org/6255148/europe.html" ;
                        ]
                    ].
                <test-project> dsp-repo:hasFunder <test-funder> .
                <test-project> dsp-repo:hasURL [
                   a schema:URL ;
                   schema:url "https://test.dasch.swiss/" ;
                ] .
                <test-project> dsp-repo:hasShortcode "0000"^^xsd:string .
            '''

test_organization = '''
                <test-dasch> rdf:type dsp-repo:Organization .
                <test-dasch> dsp-repo:hasName "TEST" .
                <test-dasch> dsp-repo:hasEmail "info@dasch.swiss" .
                <test-dasch> dsp-repo:hasAddress [
                    a schema:PostalAddress ;
                    schema:streetAddress "Teststrasse"^^xsd:string ;
                    schema:postalCode "4000"^^xsd:string ;
                    schema:addressLocality "Basel"^^xsd:string ;
                ].
                <test-dasch> dsp-repo:hasURL [
                       a schema:URL ;
                       schema:url "https://test.swiss" ;
                   ].
            '''

test_person = '''
                <test-jones> rdf:type dsp-repo:Person .
                <test-jones> dsp-repo:hasGivenName "Benjamin"^^xsd:string .
                <test-jones> dsp-repo:hasFamilyName "Jones"^^xsd:string .
                <test-jones> dsp-repo:hasEmail "benjamin.jones@test.ch"^^xsd:string .
                <test-jones> dsp-repo:hasAddress [
                    a schema:PostalAddress ;
                    schema:streetAddress "Teststrasse"^^xsd:string ;
                    schema:postalCode "4000"^^xsd:string ;
                    schema:addressLocality "Basel"^^xsd:string ;
                ].

                <test-jones> dsp-repo:isMemberOf <test-dasch> .
                <test-jones> dsp-repo:hasJobTitle "Dr. des."^^xsd:string .
                # <test-jones> dsp-repo:hasIdentifier [
                #        a schema:URL ;
                #        schema:url "https://orcid.org/0000-0002-1825-0097" ;
                #    ].
                <test-jones> dsp-repo:hasRole "Editor"^^xsd:string .
                '''
class DataSet:
    def __init__(self):
        self.sameAs = '''[
                            a schema:URL ;
                            schema:url "https://test.dasch.swiss/" ;
                        ]'''
        self.hasTitle = '"Testprojekt"'
        self.hasAlternativeTitle = '"alternative title"'
        self.hasAbstract = '"some abstract"'
        self.hasTypeOfData = '"text"'
        self.hasDocumentation = '"wip"'
        self.hasLicense = '''[
                               a schema:URL ;
                               schema:url "https://creativecommons.org/licenses/by/3.0" ;
                            ]'''
        self.hasConditionsOfAccess = '"open source"'
        self.hasHowToCite = '"Testprojekt (test), 2002, https://test.dasch.swiss"'
        self.hasStatus = '"on going"'
        self.hasDatePublished = '"2002-09-24"^^xsd:date'
        self.hasLanguage = '"de"'
        self.isPartOf = '<test-project>'
        self.hasDateCreated = '"2001-09-26"^^xsd:date'
        self.hasDateModified = '"2020-04-26"^^xsd:date'
        self.hasDistribution = '''[
                                a schema:DataDownload ;
                                schema:url "https://test.dasch.swiss" ;
                            ]'''
        self.hasQualifiedAttribution = '''[
                                            a prov:Attribution;
                                            prov:agent <test-jones>;
                                            dsp-repo:hasRole "editor";
                                        ]'''

def makeDataset(test_dataset):
    testData = prefix_list + test_person + test_organization + test_project + test_Funder +\
               '''<test-dataset> rdf:type dsp-repo:Dataset .\n'''

    if hasattr(test_dataset, 'sameAs'):
        testData += '''<test-dataset> dsp-repo:sameAs''' + test_dataset.sameAs + ' .\n'

    if hasattr(test_dataset, 'hasTitle'):
        testData += '''<test-dataset> dsp-repo:hasTitle''' + test_dataset.hasTitle + ' .\n'

    if hasattr(test_dataset, 'hasAlternativeTitle'):
        testData += '''<test-dataset> dsp-repo:hasAlternativeTitle''' + test_dataset.hasAlternativeTitle + ' .\n'

    if hasattr(test_dataset, 'hasAbstract'):
        testData += '''<test-dataset> dsp-repo:hasAbstract''' + test_dataset.hasAbstract + ' .\n'

    if hasattr(test_dataset, 'hasDocumentation'):
        testData += '''<test-dataset> dsp-repo:hasDocumentation''' + test_dataset.hasDocumentation + ' .\n'

    if hasattr(test_dataset, 'hasTypeOfData'):
        testData += '''<test-dataset> dsp-repo:hasTypeOfData''' + test_dataset.hasTypeOfData + ' .\n'

    if hasattr(test_dataset, 'hasLicense'):
        testData += '''<test-dataset> dsp-repo:hasLicense''' + test_dataset.hasLicense + ' .\n'

    if hasattr(test_dataset, 'hasConditionsOfAccess'):
        testData += '''<test-dataset> dsp-repo:hasConditionsOfAccess''' + test_dataset.hasConditionsOfAccess + ' .\n'

    if hasattr(test_dataset, 'hasHowToCite'):
        testData += '''<test-dataset> dsp-repo:hasHowToCite''' + test_dataset.hasHowToCite + ' .\n'

    if hasattr(test_dataset, 'hasStatus'):
        testData += '''<test-dataset> dsp-repo:hasStatus''' + test_dataset.hasStatus + ' .\n'

    if hasattr(test_dataset, 'hasDatePublished'):
        testData += '''<test-dataset> dsp-repo:hasDatePublished''' + test_dataset.hasDatePublished + ' .\n'

    if hasattr(test_dataset, 'hasLanguage'):
        testData += '''<test-dataset> dsp-repo:hasLanguage''' + test_dataset.hasLanguage + ' .\n'

    if hasattr(test_dataset, 'isPartOf'):
        testData += '''<test-dataset> dsp-repo:isPartOf''' + test_dataset.isPartOf + ' .\n'

    if hasattr(test_dataset, 'hasDateCreated'):
        testData += '''<test-dataset> dsp-repo:hasDateCreated''' + test_dataset.hasDateCreated + ' .\n'

    if hasattr(test_dataset, 'hasDateModified'):
        testData += '''<test-dataset> dsp-repo:hasDateModified''' + test_dataset.hasDateModified + ' .\n'

    if hasattr(test_dataset, 'hasDistribution'):
        testData += '''<test-dataset> dsp-repo:hasDistribution''' + test_dataset.hasDistribution + ' .\n'

    if hasattr(test_dataset, 'hasQualifiedAttribution'):
        testData += '''<test-dataset> dsp-repo:hasQualifiedAttribution''' + test_dataset.hasQualifiedAttribution + ' .\n'

    return testData

#########################################################################
######### TEST CLASSES FOR DATASET PROPERTIES ##############
#########################################################################

####### Tests for title of dataset #######
class datasetHasTitleTestCase(unittest.TestCase):

    # should not accept title as integer
    def test_dataset_title_as_int(self):
        testDMPlan = DataSet()
        testDMPlan.hasTitle = '"1"^^xsd:int'
        test_data = makeDataset(testDMPlan)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for title here

####### Tests for project that dataset belongs to #######
class datasetIsPartOfTestCase(unittest.TestCase):

    # should not accept title as integer
    def test_dataset_isPartOf_missing(self):
        testDataSet = DataSet()
        delattr(testDataSet, 'isPartOf')
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for isPartOf here

####### Tests for documentation of dataset #######
class datasetDocumentationTestCase(unittest.TestCase):

    # should accept URL of documentation
    def test_dataset_documentation_as_URL(self):
        testDataSet = DataSet()
        testDataSet.hasDocumentation = '''
                                        [
                                           a schema:URL ;
                                           schema:url "https://knora.org" ;
                                        ]
                                        '''
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for hasDocumentation here


####### Tests for hasLicense of dataset #######
class datasethasLicenseTestCase(unittest.TestCase):

    # should accept license of documentation as string
    def test_dataset_license_as_String(self):
        testDataSet = DataSet()
        testDataSet.hasDocumentation = '"https://creativecommons.org/licenses/by/3.0"^^xsd:string'
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    #TODO: add more tests for hasLicense here

####### Tests for sameAs property of dataset #######
class datasetSameAsTestCase(unittest.TestCase):

    # should accept sameAs URL of documentation as string
    def test_dataset_sameAs_as_String(self):
        testDataSet = DataSet()
        testDataSet.sameAs = '"https://test.dasch.swiss/"^^xsd:string'
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #TODO: add more tests for sameAs here

####### Tests for hasAlternativeTitle property of dataset #######
class datasethasAlternativeTitleTestCase(unittest.TestCase):

    # dataset might have an alternative title
    def test_dataset_sameAs_as_String(self):
        testDataSet = DataSet()
        testDataSet.hasAlternativeTitle = '"another title"^^xsd:string'
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)


    # dataset might not have an alternative title
    def test_dataset_sameAs_as_String(self):
        testDataSet = DataSet()
        delattr(testDataSet, 'hasAlternativeTitle')
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

        # TODO: add more tests for hasAlternativeTitle here

####### Tests for hasAbstract property of dataset #######
class datasethasAbstractTestCase(unittest.TestCase):

    # should accept abstract as URL
    def test_dataset_sameAs_as_String(self):
        testDataSet = DataSet()
        testDataSet.hasAbstract ='''
                                    [
                                       a schema:URL ;
                                       schema:url "https://abstract.org" ;
                                    ]
                                '''
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

        # TODO: add more tests for hasAbstract here



if __name__ == '__main__':
    unittest.main()