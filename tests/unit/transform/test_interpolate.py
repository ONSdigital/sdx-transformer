import unittest

from app.definitions import Template, Transforms, ParseTree, BuildSpecError
from app.transform.interpolate import interpolate, expand_nested_transforms, invert_post_transforms, map_template


class InterpolateTests(unittest.TestCase):

    def test_full_interpolation(self):

        template: Template = {
            "150": "#150",
            "151": "#149",
            "152": "$ROUND",
            "153": "$DIVIDE",
            "154": "$ADD",
            "156": "$ADD_MANY"
        }

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                },
                "post": "$MULTIPLY"
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
                "post": "$ROUND"
            },
            "ROUND": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "ADD": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#161", "#162"]
                }
            },
            "ADD_MANY": {
                "name": "ADD_MANY",
                "args": {
                    "values": ["#161", "#163", "$MULTIPLY"]
                }
            },
        }

        expected = {
            "150": "#150",
            "151": "#149",
            "152": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "153": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "DIVIDE",
                                "args": {
                                    "by": "2"
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            },
            "154": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#161", "#162"]
                },
            },
            "156": {
                "name": "ADD_MANY",
                "args": {
                    "values": [
                        "#161",
                        "#163",
                        {
                            "name": "ROUND",
                            "args": {
                                "value": {
                                    "name": "MULTIPLY",
                                    "args": {
                                        "by": "3",
                                    }
                                },
                                "precision": "1",
                            }
                        }
                    ]
                },
            }
        }

        actual = interpolate(template, transforms)
        self.assertEqual(expected, actual)


class ExpandNestedTransformsTests(unittest.TestCase):

    def test_nested_as_value(self):

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": "$MULTIPLY",
                    "by": "2"
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            }
        }

        expected: ParseTree = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "by": "3",
                        },
                    },
                    "by": "2"
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            }
        }

        actual = expand_nested_transforms(transforms)
        self.assertEqual(expected, actual)

    def test_nested_in_list(self):

        transforms: Transforms = {
            "ADD": {
                "name": "ADD",
                "args": {
                    "values": ["$MULTIPLY", "$DIVIDE"]
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            },
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                }
            }
        }

        expected = {
            "ADD": {
                "name": "ADD",
                "args": {
                    "values": [
                        {
                            "name": "MULTIPLY",
                            "args": {
                                "by": "3"
                            }
                        },
                        {
                            "name": "DIVIDE",
                            "args": {
                                "by": "2"
                            }
                        }
                    ]
                }
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            },
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                }
            }
        }

        actual = expand_nested_transforms(transforms)
        self.assertEqual(expected, actual)

    def test_double_nested(self):

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": "$MULTIPLY",
                    "by": "2"
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "value": "$ROUND",
                    "by": "3",
                },
            },
            "ROUND": {
                "name": "ROUND",
                "args": {
                    "nearest": "1",
                },
            }
        }

        expected: ParseTree = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "ROUND",
                                "args": {
                                    "nearest": "1",
                                },
                            },
                            "by": "3",
                        },
                    },
                    "by": "2"
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "value": {
                        "name": "ROUND",
                        "args": {
                            "nearest": "1",
                        },
                    },
                    "by": "3",
                },
            },
            "ROUND": {
                "name": "ROUND",
                "args": {
                    "nearest": "1",
                },
            }
        }

        actual = expand_nested_transforms(transforms)
        self.assertEqual(expected, actual)

    def test_missing_transform_raises_error(self):

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": "$ADD",
                    "by": "2"
                },
            },
            "MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            }
        }

        with self.assertRaises(BuildSpecError):
            expand_nested_transforms(transforms)


class MapTemplateTests(unittest.TestCase):

    def test_mapping(self):

        template: Template = {
            "150": "#150",
            "151": "$ROUND",
            "152": "$DIVIDE",
            "153": "$ROUND",
        }

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "by": "3",
                        },
                    },
                    "by": "2"
                },
            },
            "ROUND": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                },
            }
        }

        expected: ParseTree = {
            "150": "#150",
            "151": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "152": {
                "name": "DIVIDE",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "by": "3",
                        }
                    },
                    "by": "2"
                }
            },
            "153": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            }
        }

        actual = map_template(template, transforms)
        self.assertEqual(expected, actual)

    def test_mapping_for_prepop_template(self):

        template: Template = {
            "schema_version": "v1",
            "identifier": "#ruref",
            "items": {
                "local-units": [
                    {
                        "identifier": "#luref",
                        "lu_name": "$1",
                        "lu_address": [
                            "$2", "$3"
                        ]
                    }
                ]
            }
        }

        transforms: Transforms = {
            "1": {
                "name": "CONCAT",
                "args": {
                    "value": "#name1",
                    "values": ["#name2", "#name3"],
                    "seperator": " "
                },
            },
            "2": {
                "name": "ROUND",
                "args": {
                    "value": "#age",
                    "precision": "1",
                },
            },
            "3": {
                "name": "ROUND",
                "args": {
                    "value": "#profit",
                    "precision": "10",
                },
            }
        }

        expected: ParseTree = {
            "schema_version": "v1",
            "identifier": "#ruref",
            "items": {
                "local-units": [
                    {
                        "identifier": "#luref",
                        "lu_name": {
                            "name": "CONCAT",
                            "args": {
                                "value": "#name1",
                                "values": ["#name2", "#name3"],
                                "seperator": " "
                            },
                        },
                        "lu_address": [
                            {
                                "name": "ROUND",
                                "args": {
                                    "value": "#age",
                                    "precision": "1",
                                },
                            },
                            {
                                "name": "ROUND",
                                "args": {
                                    "value": "#profit",
                                    "precision": "10",
                                },
                            }
                        ]
                    }
                ]
            }
        }

        actual = map_template(template, transforms)
        self.assertEqual(expected, actual)

    def test_missing_mapping_raises_error(self):

        template: Template = {
            "150": "#150",
            "151": "$ROUND",
        }

        transforms: Transforms = {
            "DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2"
                }
            }
        }

        with self.assertRaises(BuildSpecError):
            map_template(template, transforms)


class InvertPostTransformsTest(unittest.TestCase):

    def test_nested(self):

        tree: ParseTree = {
            '150': {
                'name': 'DIVIDE',
                'args': {'by': '2'},
                'post': {
                    'name': 'MULTIPLY',
                    'args': {'by': '3'},
                    'post': {
                        'name': 'ROUND',
                        'args': {'precision': '1'}
                    }
                }
            }
        }

        expected: ParseTree = {
            '150': {
                'name': 'ROUND',
                'args': {
                    'precision': '1',
                    'value': {
                        'name': 'MULTIPLY',
                        'args': {
                            'by': '3',
                            'value': {
                                'name': 'DIVIDE',
                                'args': {'by': '2'}
                            }
                        }
                    }
                }
            }
        }

        actual = invert_post_transforms(tree)
        self.assertEqual(expected, actual)
