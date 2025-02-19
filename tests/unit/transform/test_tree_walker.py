import unittest

from app.definitions.spec import ParseTree
from app.definitions.input import Field
from app.services.transform.tree_walker import TreeWalker


class TreeWalkerTests(unittest.TestCase):

    def test_walk(self):

        tree: ParseTree = {
            "150": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "ADD",
                                "args": {
                                    "values": [
                                        "#001",
                                        "#002",
                                        None,
                                        {
                                            "name": "MULTIPLY",
                                            "args": {
                                                "by": "#003"
                                            }
                                        }
                                    ]
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "#004",
                }
            }
        }

        expected = {
            "150": {
                "name": "ROUND",
                "args": {
                    "value": {
                        "name": "MULTIPLY",
                        "args": {
                            "value": {
                                "name": "ADD",
                                "args": {
                                    "values": [
                                        "001",
                                        "002",
                                        None,
                                        {
                                            "name": "MULTIPLY",
                                            "args": {
                                                "by": "003"
                                            }
                                        }
                                    ]
                                },
                            },
                            "by": "3",
                        }
                    },
                    "precision": "004",
                }
            }
        }

        def base_str(_name: str, field: str, _walker: TreeWalker) -> Field:
            if field.startswith("#"):
                return field[1:]
            return field

        actual = TreeWalker(tree=tree, on_str=base_str).walk_tree()
        self.assertEqual(expected, actual)
