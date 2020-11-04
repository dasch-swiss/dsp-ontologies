import unittest
from pyshacl import validate
from os import path

ws = path.dirname(__file__)

dsp_repo_shape = path.join(ws, '../dsp-repository/v1/dsp-repository.shacl.ttl')

with open(path.join(ws, 'test_data/prefix_list.ttl'), 'r') as content_file:
    prefix_list = content_file.read()

with open(path.join(ws, 'test_data/organization.ttl'), 'r') as content_file:
    test_funder = content_file.read()


class Project:
    def __init__(self):
        self.hasName = '"test"^^xsd:string'
        self.hasDescription = '"testen"^^xsd:string'
        self.keywords = '"mathematics"^^xsd:string'
        self.hasDiscipline = '''[
                                   a schema:URL ;
                                   schema:propertyID [
                                       a schema:PropertyValue ;
                                       schema:propertyID "SKOS UNESCO Nomenclature" ;
                                   ] ;
                                   schema:url "http://skos.um.es/unesco6/11" ;
                                ]'''

        self.hasStartDate = '"2000-07-26"^^xsd:date'
        self.hasTemporalCoverage = '''[
                                       a schema:URL ;
                                       schema:propertyID [
                                           a schema:PropertyValue ;
                                           schema:propertyID "Chronontology Dainst" ;
                                       ] ;
                                       schema:url "http://chronontology.dainst.org/period/Ef9SyESSafJ1" ;
                                    ]'''

        self.hasFunder = "<test-funder>"
        self.hasURL =  '''[
                               a schema:URL ;
                               schema:url "https://test.dasch.swiss/" ;
                            ]'''

        self.hasShortcode = '"0000"^^xsd:string'

        self.hasSpatialCoverage = '''[
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

    projectData = prefix_list + test_funder + '''<test-project> rdf:type dsp-repo:Project .\n'''

    if hasattr(testProject, 'hasName'):
        projectData += '''<test-project> dsp-repo:hasName''' + testProject.hasName + ' .\n'

    if hasattr(testProject, 'hasDescription'):
        projectData += '''<test-project> dsp-repo:hasDescription''' + testProject.hasDescription + ' .\n'

    if hasattr(testProject, 'keywords'):
        projectData += '''<test-project> dsp-repo:hasKeywords''' + testProject.keywords + ' .\n'

    if hasattr(testProject, 'hasDiscipline'):
        projectData += '''<test-project> dsp-repo:hasDiscipline''' + testProject.hasDiscipline + ' .\n'

    if hasattr(testProject, 'hasStartDate'):
        projectData += '''<test-project> dsp-repo:hasStartDate''' + testProject.hasStartDate  + ' .\n'

    if hasattr(testProject, 'hasTemporalCoverage'):
        projectData += '''<test-project> dsp-repo:hasTemporalCoverage''' + testProject.hasTemporalCoverage  + ' .\n'

    if hasattr(testProject, 'hasSpatialCoverage'):
        projectData += '''<test-project> dsp-repo:hasSpatialCoverage''' + testProject.hasSpatialCoverage + ' .\n'

    if hasattr(testProject, 'hasFunder'):
        projectData += '''<test-project> dsp-repo:hasFunder''' + testProject.hasFunder + ' .\n'

    if hasattr(testProject, 'hasURL'):
        projectData += '''<test-project> dsp-repo:hasURL''' + testProject.hasURL + ' .\n'

    if hasattr(testProject, 'hasShortcode'):
        projectData += '''<test-project> dsp-repo:hasShortcode''' + testProject.hasShortcode + ' .\n'

    return projectData


############################################################
######### TEST CLASSES FOR PROJECT PROPERTIES ##############
############################################################

# ####### Tests for project name #######
class ProjectNameTestCase(unittest.TestCase):

    # should accept name as string
    def test_projectHasName_As_String(self):
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
    def test_projectHasName_As_IRI(self):
        testProject = Project()
        testProject.hasName = '<anIRI>'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    #should fail when name is missing
    def test_projectHasName_missing(self):
        testProject = Project()
        delattr(testProject, 'hasName')
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

#     # Todo: add more tests for name here

####### Tests for project shortcode #######
class ProjectShortCodeTestCase(unittest.TestCase):
    # should accept shortcode as string
    def test_projectShortCode_As_String(self):
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
    def test_projectShortCode_As_integer(self):
        testProject = Project()
        testProject.hasShortcode = '"0801"^^xsd:int'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # should fail when shortcode is missing
    def test_projectHasName_missing(self):
        testProject = Project()
        delattr(testProject, 'hasShortcode')
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for shortcode here

####### Tests for project keywords #######
class ProjectKeywordsTestCase(unittest.TestCase):
    # should accept keywords as string
    def test_projectKeywords_As_String(self):
        testProject = Project()
        testProject.keywords = '"a test keyword"^^xsd:string'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail when no keyword given
    def test_projectKeywords_missing(self):
        testProject = Project()
        delattr(testProject, 'keywords')
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for keywords here

####### Tests for project description #######
class ProjectDescriptionTestCase(unittest.TestCase):
    # should accept description as string
    def test_projectDescription_As_String(self):
        testProject = Project()
        testProject.hasDescription = '"bla bla bla"^^xsd:string'
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    # should fail when no descrition given
    def test_projectKeywords_missing(self):
        testProject = Project()
        delattr(testProject, 'hasDescription')
        test_data = makeProjectData(testProject)
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)


    # should fail when multuiple description given
    def test_projectDescription_multipleEntries(self):
        testProject = Project()
        testProject.hasDescription = '"first description"^^xsd:string'
        test_data = makeProjectData(testProject)
        test_data += '''<test-project> dsp-repo:hasDescription "second description"^^xsd:string .\n'''
        conforms, v_graph, v_text = validate(test_data, shacl_graph=dsp_repo_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

    # TODO: add more tests for description here


## TODO: Add tests for remaining properties #####

if __name__ == '__main__':
    unittest.main()
