import unittest
from pyshacl import validate
from os import path

ws = path.dirname(__file__)

dsp_repo_shape = path.join(ws, '../dsp-repository/v1/dsp-repository.shacl.ttl')


with open(path.join(ws, 'test_data/prefix_list.ttl'), 'r') as content_file:
    prefix_list = content_file.read()

with open(path.join(ws, 'test_data/organization.ttl'), 'r') as content_file:
    test_organization = content_file.read()

with open(path.join(ws, 'test_data/project.ttl'), 'r') as content_file:
    test_project = content_file.read()

with open(path.join(ws, 'test_data/person.ttl'), 'r') as content_file:
    test_person = content_file.read()

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
    testData = prefix_list + test_person + test_organization + test_project +\
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
    def test_dataset_hasAlternativeTitle_as_String(self):
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
    def test_dataset_hasAbstract_as_URL(self):
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

####### Tests for hasTypeOfData property of dataset #######
class datasethasTypeOfDataTestCase(unittest.TestCase):

    # should accept json as type of data
    def test_dataset_hasTypeOfData_json(self):
        testDataSet = DataSet()
        testDataSet.hasTypeOfData = '"json"'
        test_data = makeDataset(testDataSet)

        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

        # TODO: add more tests for hasTypeOfData here


## TODO: Add tests for remaining properties #####

if __name__ == '__main__':
    unittest.main()