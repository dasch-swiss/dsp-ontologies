import unittest
from pyshacl import validate

prefix_list = '''
                        @prefix dsp-repo: <http://ns.dasch.swiss/repository#> .
                        @prefix knora-base: <http://www.knora.org/ontology/knora-base#> .
                        @prefix knora-admin: <http://www.knora.org/ontology/knora-admin#> .
                        @prefix owl: <http://www.w3.org/2002/07/owl#> .
                        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
                        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
                        @prefix xml: <http://www.w3.org/XML/1998/namespace> .
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
                        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
                        '''

# TODO: Substitute with SHACL file
test_shape = '''
            ##### SHAPES #####
            # DaSCH Metadata

            @prefix sh: <http://www.w3.org/ns/shacl#> .
            @prefix dash: <http://datashapes.org/dash#> .
            ''' + prefix_list + '''
            @base <http://ns.dasch.swiss/repository#> .

            <http://ns.dasch.swiss/repository>
              rdf:type owl:Ontology ;
              owl:imports <http://datashapes.org/dash> .


            ##### PROPERTIES #####
            # http://ns.dasch.swiss/repository#hasName
            dsp-repo:hasName
                a rdf:Property .

            ### --- Shape of dsp-repo:Project ---
            dsp-repo:ProjectShape
                a sh:NodeShape ;
                sh:targetClass dsp-repo:Project ;
                sh:property [
                    sh:path dsp-repo:hasName ;
                    sh:name "Name" ;
                    sh:description "Name of the project"@en ;
                    sh:datatype xsd:string ;
                    sh:maxCount 1 ;
                    sh:minCount 1 ;
                ] ;
                sh:closed true ;
                sh:ignoredProperties (rdf:type) .
            '''

base = '''
     # Metadata test project
     #
     ''' + prefix_list + '''
     @base <http://ns.dasch.swiss/repository#> .

     '''

class ProjectShapeTestCase(unittest.TestCase):
    def test_projectHasName_with_String(self):
        test_data = base + '''
                <test-project> rdf:type dsp-repo:Project .
                <test-project> dsp-repo:hasName "Testprojektname (test)"^^xsd:string .

                '''
        conforms, v_graph, v_text = validate(test_data, shacl_graph=test_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertTrue(conforms)

    def test_projectHasName_with_IRI(self):
        test_data = base + '''
                        <test-project> rdf:type dsp-repo:Project .
                        <test-project> dsp-repo:hasName <an-IRI> .

                        '''
        conforms, v_graph, v_text = validate(test_data, shacl_graph=test_shape,
                                             data_graph_format='turtle',
                                             shacl_graph_format='turtle',
                                             inference='rdfs', debug=True,
                                             serialize_report_graph=True)
        self.assertFalse(conforms)

if __name__ == '__main__':
    unittest.main()
