import unittest

from app.definitions import Template, Transforms, ParseTree
from app.interpolate import interpolate_functions, add_implicit_values, interpolate_mappings


class InterpolateTests(unittest.TestCase):

    def test_interpolate_single(self):

        template: Template = {
            "151": "$ROUND"
        }

        transforms: Transforms = {
            "$ROUND": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            }
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            }
        }
        actual = interpolate_functions(template, transforms)
        self.assertEqual(expected, actual)

    def test_interpolate_function_and_literal(self):

        template: Template = {
            "151": "$ROUND",
            "152": "4"
        }

        transforms: Transforms = {
            "$ROUND": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            }
        }

        expected = {
            "151": {
                "name": "ROUND",
                "args": {
                    "precision": "1",
                }
            },
            "152": "4"
        }
        actual = interpolate_functions(template, transforms)
        self.assertEqual(expected, actual)

    def test_interpolate_post_function(self):

        template: Template = {
            "151": "$DIVIDE"
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
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "1",
                }
            }
        }
        actual = interpolate_functions(template, transforms)
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