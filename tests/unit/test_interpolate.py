import unittest

from app.definitions import Template, Transforms, ParseTree
from app.interpolate import interpolate_functions, add_implicit_values


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

    def test_single(self):

        parse_tree: ParseTree = {
            "151": {
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
                    "value": "#151",
                    "precision": "1",
                }
            }
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
                                "value": "#151",
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

        actual = add_implicit_values(parse_tree)
        self.assertEqual(expected, actual)