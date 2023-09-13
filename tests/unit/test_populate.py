import unittest

from app.definitions import ParseTree
from app.populate import populate_mappings, resolve_value_fields


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

        actual = resolve_value_fields(parse_tree)
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

        actual = resolve_value_fields(parse_tree)
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

        actual = resolve_value_fields(parse_tree)
        self.assertEqual(expected, actual)

    def test_in_list(self):

        parse_tree: ParseTree = {
            '156': {
                'name': 'ADD_MANY',
                'args': {
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
                    'value': '#156',
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

        actual = resolve_value_fields(parse_tree)
        self.assertEqual(expected, actual)

    def test_hash_value(self):

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
                                    "value": "#value"
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

        actual = resolve_value_fields(parse_tree)
        self.assertEqual(expected, actual)

    def test_hash_value_as_non_value_arg(self):

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
                            "by": "#value",
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
                            "by": "#151",
                        }
                    },
                    "precision": "1",
                }
            }
        }

        actual = resolve_value_fields(parse_tree)
        self.assertEqual(expected, actual)


class PopulateMappingsTests(unittest.TestCase):

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

        actual = populate_mappings(parse_tree, data)

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

        actual = populate_mappings(parse_tree, data)

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

        actual = populate_mappings(parse_tree, data)

        self.assertEqual(expected, actual)
