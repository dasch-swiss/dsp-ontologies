from pyshacl import validate
from os import path

dsp_repo_shape = './dsp-repository/v1/dsp-repository.shacl.ttl'
shape_file = path.abspath(dsp_repo_shape)

dsp_repo_exampleData = './example/example-metadata.ttl'
data_file = path.abspath(dsp_repo_exampleData)

if __name__ == '__main__':

    conforms, v_graph, v_text = validate(data_file, shacl_graph=shape_file,
                                         data_graph_format='turtle',
                                         shacl_graph_format='turtle',
                                         inference='rdfs', debug=True,
                                         serialize_report_graph=True)

    print(conforms)
    print(v_graph)
    print(v_text)
