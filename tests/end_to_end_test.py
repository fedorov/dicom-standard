import subprocess

import pytest

import dicom_standard.parse_lib as pl


@pytest.fixture(scope='module')
def make_standard():
    subprocess.run(['make', 'all'])


@pytest.fixture(scope='module')
def ciods(make_standard):
    return pl.read_json_to_dict('standard/ciods.json')


@pytest.fixture(scope='module')
def modules(make_standard):
    return pl.read_json_to_dict('standard/modules.json')


@pytest.fixture(scope='module')
def attributes(make_standard):
    return pl.read_json_to_dict('standard/attributes.json')


@pytest.fixture(scope='module')
def ciod_module_relationship(make_standard):
    return pl.read_json_to_dict('standard/ciod_to_modules.json')


@pytest.fixture(scope='module')
def module_attribute_relationship(make_standard):
    return pl.read_json_to_dict('standard/module_to_attributes.json')


@pytest.mark.endtoend
def test_valid_foreign_keys_ciod_module(ciod_module_relationship, ciods, modules):
    for pair in ciod_module_relationship:
        assert pair['ciod'] in ciods
        assert pair['module'] in modules


@pytest.mark.endtoend
def test_valid_foreign_keys_module_attribute(module_attribute_relationship, modules, attributes):
    for pair in module_attribute_relationship:
        assert pair['module'] in modules
        assert pair['path'].split(':')[-1] in attributes


@pytest.mark.endtoend
def test_vertical_samples_from_standard(ciods, modules, attributes):
    test_ciod = {
        "us-multi-frame-image": {
            "description": "<p>\nThe Ultrasound (US) Multi-frame Image Information Object Definition specifies a Multi-frame image that has been created by an ultrasound imaging device.</p>",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.7.4.html#table_A.7-1",
            "name": "US Multi-frame Image",
            "id": "us-multi-frame-image",
        }
    }
    test_module = {
        "patient": {
            "name": "Patient",
            "id": "patient",
            "description": "<p>\n<span href=\"#table_C.7-1\">This module </span> specifies the Attributes of the Patient that describe and identify the Patient who is the subject of a Study.\n            This Module contains Attributes of the patient that are needed for interpretation of the Composite Instances and are common for all studies performed on the patient. It contains Attributes that are also included in the Patient Modules in <a href=\"http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.2.html#sect_C.2\" target=\"_blank\">Section\u00a0C.2</a>.</p>",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#table_C.7-1"
        }
    }
    test_attribute = {
        "00100010": {
            "tag": "(0010,0010)",
            "retired": False,
            "keyword": "PatientName",
            "name": "Patient's Name",
            "valueMultiplicity": "1",
            "valueRepresentation": "PN"
        },
        "00080034": {
            "tag": "(0008,0034)",
            "retired": True,
            "keyword": "OverlayTime",
            "name": "Overlay Time",
            "valueMultiplicity": "1",
            "valueRepresentation": "TM"
        },
        "00080108": {
            "tag": "(0008,0108)",
            "retired": False,
            "keyword": "ExtendedCodeMeaning",
            "name": "Extended Code Meaning",
            "valueMultiplicity": "1",
            "valueRepresentation": "LT"
        }
    }
    assert test_ciod["us-multi-frame-image"] == ciods["us-multi-frame-image"]
    assert test_module["patient"] == modules["patient"]
    assert test_attribute["00100010"] == attributes["00100010"]
    assert test_attribute["00080034"] == attributes["00080034"]
    assert test_attribute["00080108"] == attributes["00080108"]


@pytest.mark.endtoend
def test_trace_from_attribute_to_ciod(ciods, ciod_module_relationship, modules,
                                      module_attribute_relationship, attributes):
    attr = {
        "00080121": {
            "name": "Equivalent Code Sequence",
            "retired": False,
            "valueMultiplicity": "1",
            "keyword": "EquivalentCodeSequence",
            "valueRepresentation": "SQ",
            "tag": "(0008,0121)"
        }
    }
    module_attr = [
        {
            "module": "patient-study",
            "path": "patient-study:00081084:00080121",
            "tag": "(0008,0121)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a",
            "description": "<td colspan=\"1\" rowspan=\"1\">\n<p>\nCodes that are considered equivalent by the creating system.</p>\n<p>\nOne or more Items are permitted in this Sequence.</p>\n<p>\nSee <span href=\"\">Section\u00a08.9</span>.</p>\n</td>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_8.9.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
        {
            "module": "patient-study",
            "path": "patient-study:00101021:00080121",
            "tag": "(0008,0121)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a",
            "description": "<td colspan=\"1\" rowspan=\"1\">\n<p>\nCodes that are considered equivalent by the creating system.</p>\n<p>\nOne or more Items are permitted in this Sequence.</p>\n<p>\nSee <span href=\"\">Section\u00a08.9</span>.</p>\n</td>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_8.9.html#sect_8.9",
                    "title": "Section\u00a08.9"
                },
            ]
        },
    ]
    module = {
        "patient-study": {
            "id": "patient-study",
            "name": "Patient Study",
            "description": "<p>\n<span href=\"#table_C.7-4a\">This module </span> defines Attributes that provide information about the Patient at the time the Study started.</p>",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.2.2.html#table_C.7-4a"
        },
    }
    ciod_module = [
        {
            "ciod": "cr-image",
            "module": "patient-study",
            "usage": "U",
            "conditionalStatement": None,
            "informationEntity": "Study"
        },
    ]
    ciod = {
        "cr-image": {
            "description": "<p>\nThe Computed Radiography (CR) Image Information Object Definition specifies an image that has been created by a computed radiography imaging device.</p>",
            "name": "CR Image",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_A.2.3.html#table_A.2-1",
            "id": "cr-image",
        }
    }
    assert attr["00080121"] == attributes["00080121"]
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    assert module['patient-study'] == modules['patient-study']
    assert ciod_module[0] in ciod_module_relationship
    assert ciod['cr-image'] == ciods['cr-image']


@pytest.mark.endtoend
def test_number_of_attribute_appearances(module_attribute_relationship, attributes):
    module_attr = [
        {
            "module": "patient-demographic",
            "path": "patient-demographic:00100213",
            "tag": "(0010,0213)",
            "type": "None",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.2.3.html#table_C.2-3",
            "description": "<td colspan=\"1\" rowspan=\"1\">\n<p>\nThe nomenclature used for Strain Description (0010,0212). See <span href=\"\">Section\u00a0C.7.1.1.1.4</span>.</p>\n</td>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
        {
            "module": "patient",
            "path": "patient:00100213",
            "tag": "(0010,0213)",
            "type": "3",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#table_C.7-1",
            "description": "<td colspan=\"1\" rowspan=\"1\">\n<p>\nThe nomenclature used for Strain Description (0010,0212). See <span href=\"\">Section\u00a0C.7.1.1.1.4</span>.</p>\n</td>",
            "externalReferences": [
                {
                    "sourceUrl": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.html#sect_C.7.1.1.1.4",
                    "title": "Section\u00a0C.7.1.1.1.4"
                },
            ]
        },
    ]

    attrs = {
        "00100213": {
            "name": "Strain Nomenclature",
            "retired": False,
            "valueMultiplicity": "1",
            "keyword": "StrainNomenclature",
            "valueRepresentation": "LO",
            "tag": "(0010,0213)"
        }
    }
    assert attrs['00100213'] == attributes['00100213']
    assert module_attr[0] in module_attribute_relationship
    assert module_attr[1] in module_attribute_relationship
    all_attribute_appearances = [rel for rel in module_attribute_relationship
                                 if rel['tag'] == '(0010,0213)']
    assert len(all_attribute_appearances) == 2


@pytest.mark.endtoend
def test_number_of_module_appearances(ciods, ciod_module_relationship, modules):
    module = {
        "volume-cropping": {
            "name": "Volume Cropping",
            "linkToStandard": "http://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.11.24.html#table_C.11.24-1",
            "description": "<p>\n<span href=\"#table_C.11.24-1\">This module </span> contains the attributes of the Volume Cropping Module. This Module limits the spatial extent of inputs in Volumetric Presentation State Input Sequence (0070,1201) that are used.</p>",
            "id": "volume-cropping"
        }
    }
    ciod_module = [
        {
            "ciod": "planar-mpr-volumetric-presentation-state",
            "module": "volume-cropping",
            "usage": "C",
            "conditionalStatement": "Required if Global Crop (0070,120B) or any value of Crop (0070,1204) is YES",
            "informationEntity": "Presentation State"
        },
        {
            "ciod": "volume-rendering-volumetric-presentation-state",
            "module": "volume-cropping",
            "usage": "C",
            "conditionalStatement": "Required if Global Crop (0070,120B) or any value of Crop (0070,1204) is YES",
            "informationEntity": "Presentation State"
        },
    ]
    assert module['volume-cropping'] == modules['volume-cropping']
    for ciod_module_pair in ciod_module:
        assert ciod_module_pair in ciod_module_relationship
    all_module_appearances = [rel for rel in ciod_module_relationship
                              if rel['module'] == 'volume-cropping']
    assert len(all_module_appearances) == 2
