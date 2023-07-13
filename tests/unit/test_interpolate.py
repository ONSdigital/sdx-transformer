import unittest

from app.definitions import Template, Transforms, ParseTree, Data
from app.interpolate import add_implicit_values, interpolate_mappings, interpolate, \
    interpolate_nested_functions, invert_post_functions


class InterpolateTests(unittest.TestCase):

    def test_full_interpolation(self):

        data: Data = {
            "150": "10",
            "152": "1.5",
            "153": "80",
            "156": "5",
            "161": "6",
            "162": "7",
        }

        template: Template = {
            "150": "#150",
            "151": "#149",
            "152": "$ROUND",
            "153": "$DIVIDE",
            "154": "$ADD",
            "156": "$ADD_MANY"
        }

        transforms: Transforms = {
            "$DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                },
                "post": "$MULTIPLY"
            },
            "$MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
                "post": "$ROUND"
            },
            "$ROUND": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "$ADD": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#161", "#162"]
                }
            },
            "$ADD_MANY": {
                "name": "ADD_MANY",
                "args": {
                    "values": ["#161", "#163", "$MULTIPLY"]
                }
            },
        }

        expected = {
            "150": "10",
            "151": None,
            "152": {
                "name": "ROUND",
                "args": {
                    "value": "1.5",
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
                                    "by": "2",
                                    "value": "80"
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
                    "values": ["6", "7"]
                },
            },
            "156": {
                "name": "ADD_MANY",
                "args": {
                    "value": "5",
                    "values": [
                        "6",
                        None,
                        {
                            "name": "ROUND",
                            "args": {
                                "value": {
                                    "name": "MULTIPLY",
                                    "args": {
                                        "value": "5",
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

        actual = interpolate(template, transforms, data)
        self.assertEqual(expected, actual)


class NestedFunctionsTests(unittest.TestCase):

    def test_nested(self):

        transforms: Transforms = {
            "$DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "value": "$MULTIPLY",
                    "by": "2"
                },
            },
            "$MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            }
        }

        expected: ParseTree = {
            "$DIVIDE": {
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
            "$MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            }
        }

        actual = interpolate_nested_functions(transforms)
        self.assertEqual(expected, actual)

    def test_interpolate_arg_function(self):

        transforms: Transforms = {
            "$ADD": {
                "name": "ADD",
                "args": {
                    "values": ["$MULTIPLY", "$DIVIDE"]
                },
            },
            "$MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            },
            "$DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                }
            }
        }

        expected = {
            "$ADD": {
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
            "$MULTIPLY": {
                "name": "MULTIPLY",
                "args": {
                    "by": "3",
                },
            },
            "$DIVIDE": {
                "name": "DIVIDE",
                "args": {
                    "by": "2",
                }
            }
        }

        actual = interpolate_nested_functions(transforms)
        self.assertEqual(expected, actual)


class InvertPostFunctionsTest(unittest.TestCase):

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

        actual = invert_post_functions(tree)
        self.assertEqual(expected, actual)


class ImplicitValueTests(unittest.TestCase):

    def test_flat(self):

        parse_tree: ParseTree = {
            "151": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "161": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "171": "#171"
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": "#151",
                    "precision": "1",
                }
            },
            "161": {
                "name": "ROUND",
                "args": {
                    "value": "#161",
                    "precision": "1",
                }
            },
            "171": "#171"
        }

        actual = add_implicit_values(parse_tree)
        self.assertEqual(expected, actual)

    def test_nested(self):

        parse_tree: ParseTree = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "DIVIDE",
                                "args": {
                                    "by": "2",
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            }
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "DIVIDE",
                                "args": {
                                    "by": "2",
                                    "value": "#151"
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            }
        }

        actual = add_implicit_values(parse_tree)
        self.assertEqual(expected, actual)

    def test_blank_value(self):

        parse_tree: ParseTree = {
            "151": "#151",
            "152": "#152",
            "171": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#151", "#152"]
                }
            },
            "172": {
                "name": "ROUND",
                "args": {
                    "value": "#152",
                    "precision": "1"
                }
            }
        }

        expected = {
            "151": "#151",
            "152": "#152",
            "171": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#151", "#152"]
                }
            },
            "172": {
                "name": "ROUND",
                "args": {
                    "value": "#152",
                    "precision": "1"
                }
            }
        }

        actual = add_implicit_values(parse_tree)
        self.assertEqual(expected, actual)

    def test_in_list(self):

        parse_tree: ParseTree = {
            '156': {
                'name': 'ADD_MANY',
                'args': {
                    'value': '',
                    'values': [
                        '#161',
                        '#163',
                        {
                            'name': 'ROUND',
                            'args': {
                                'precision': '1',
                                'value': {
                                    'name': 'MULTIPLY',
                                    'args': {'by': '3'},
                                }
                            }
                        }
                    ]
                }
            }
        }

        expected: ParseTree = {
            '156': {
                'name': 'ADD_MANY',
                'args': {
                    'value': '',
                    'values': [
                        '#161',
                        '#163',
                        {
                            'name': 'ROUND',
                            'args': {
                                'precision': '1',
                                'value': {
                                    'name': 'MULTIPLY',
                                    'args': {
                                        'value': '#156',
                                        'by': '3'
                                    },
                                }
                            }
                        }
                    ]
                }
            }
        }

        actual = add_implicit_values(parse_tree)
        self.assertEqual(expected, actual)


class InterpolateMappingsTests(unittest.TestCase):

    def test_simple(self):
        parse_tree = {
            "100": "#100",
            "200": "#300"
        }

        data = {
            "100": "1",
            "300": "2"
        }

        expected = {
            "100": "1",
            "200": "2"
        }

        actual = interpolate_mappings(parse_tree, data)

        self.assertEqual(expected, actual)

    def test_flat(self):

        parse_tree = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": "#151",
                    "precision": "1",
                }
            },
            "161": {
                "name": "ROUND",
                "args": {
                    "value": "#161",
                    "precision": "1",
                }
            }
        }

        data = {
            "151": "1",
            "161": "10"
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": "1",
                    "precision": "1",
                }
            },
            "161": {
                "name": "ROUND",
                "args": {
                    "value": "10",
                    "precision": "1",
                }
            }
        }

        actual = interpolate_mappings(parse_tree, data)

        self.assertEqual(expected, actual)

    def test_nested(self):
        parse_tree = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "DIVIDE",
                                "args": {
                                    "by": "2",
                                    "value": "#151"
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            },

            "152": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["#153", "#154"]
                },
            }
        }

        data = {
            "151": "1",
            "161": "10",
            "153": "5",
            "154": "9",
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "DIVIDE",
                                "args": {
                                    "by": "2",
                                    "value": "1"
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            },

            "152": {
                "name": "ADD",
                "args": {
                    "value": "",
                    "values": ["5", "9"]
                },
            }
        }

        actual = interpolate_mappings(parse_tree, data)

        self.assertEqual(expected, actual)