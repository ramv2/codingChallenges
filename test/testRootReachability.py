import unittest
from root_reachability import RootReachability
import numpy.testing as np_tst

class testRootReachability(unittest.TestCase):
    def test_simple(self):
        rr = RootReachability()
        inp = """
                    {
                        "nodes": [{
                                    "id": "M00"
                                }, {
                                    "id": "M01"
                                }, {
                                    "id": "M02"
                                }
                                ],
                        "edges": [{
                                    "from": "M01",
                                    "to": "M02"
                                    }, {
                                    "from": "M00",
                                    "to": "M02"
                                    }, {
                                    "from": "M01",
                                    "to": "M00"
                                    }
                                ],
                        "root": "M00"
                    }
                    """
        # delete = {"from": "M01", "to": "M02"}
        rr.construct_adjacency_lists(inp)
        rr.delete_edge()
        np_tst.assert_array_equal(["M02"], rr.get_orphan_nodes())

    def test_complex_1(self):
        rr = RootReachability()
        inp = """
            {
            "root": "M00",
            "edges": [{
                    "from": "M02",
                    "to": "M00"
                }, {
                    "from": "M01",
                    "to": "M02"
                }, {
                    "from": "M04",
                    "to": "M02"
                }, {
                    "from": "M10",
                    "to": "M01"
                }, {
                    "from": "M01",
                    "to": "M03"
                }, {
                    "from": "M01",
                    "to": "M04"
                }, {
                    "from": "M07",
                    "to": "M10"
                }, {
                    "from": "M06",
                    "to": "M07"
                }, {
                    "from": "M08",
                    "to": "M07"
                }, {
                    "from": "M03",
                    "to": "M06"
                }, {
                    "from": "M05",
                    "to": "M06"
                }, {
                    "from": "M06",
                    "to": "M08"
                }, {
                    "from": "M06",
                    "to": "M09"
                }, {
                    "from": "M06",
                    "to": "M11"
                }, {
                    "from": "M03",
                    "to": "M05"
                }, {
                    "from": "M11",
                    "to": "M09"
                }, {
                    "from": "M07",
                    "to": "M08"
                }
            ],
            "nodes": [{
                    "id": "M02"
                }, {
                    "id": "M05"
                }, {
                    "id": "M08"
                }, {
                    "id": "M07"
                }, {
                    "id": "M03"
                }, {
                    "id": "M10"
                }, {
                    "id": "M04"
                }, {
                    "id": "M06"
                }, {
                    "id": "M01"
                }, {
                    "id": "M11"
                }, {
                    "id": "M00"
                }, {
                    "id": "M09"
                }
            ]
        }

            """
        # delete = {"from": "M07", "to": "M10"}
        rr.construct_adjacency_lists(inp)
        rr.delete_edge()
        np_tst.assert_array_equal(['M05', 'M08', 'M07', 'M03', 'M06', 'M11',
                                   'M09'], rr.get_orphan_nodes())

    def test_complex_2(self):
        rr = RootReachability()
        inp = """
                    {
                    "root": "M00",
                    "edges": [{
                            "from": "M02",
                            "to": "M00"
                        }, {
                            "from": "M01",
                            "to": "M02"
                        }, {
                            "from": "M04",
                            "to": "M02"
                        }, {
                            "from": "M10",
                            "to": "M01"
                        }, {
                            "from": "M01",
                            "to": "M03"
                        }, {
                            "from": "M01",
                            "to": "M04"
                        }, {
                            "from": "M07",
                            "to": "M10"
                        }, {
                            "from": "M06",
                            "to": "M07"
                        }, {
                            "from": "M08",
                            "to": "M07"
                        }, {
                            "from": "M03",
                            "to": "M06"
                        }, {
                            "from": "M05",
                            "to": "M06"
                        }, {
                            "from": "M06",
                            "to": "M08"
                        }, {
                            "from": "M06",
                            "to": "M09"
                        }, {
                            "from": "M06",
                            "to": "M11"
                        }, {
                            "from": "M03",
                            "to": "M05"
                        }, {
                            "from": "M11",
                            "to": "M09"
                        }, {
                            "from": "M07",
                            "to": "M08"
                        }
                    ],
                    "nodes": [{
                            "id": "M02"
                        }, {
                            "id": "M05"
                        }, {
                            "id": "M08"
                        }, {
                            "id": "M07"
                        }, {
                            "id": "M03"
                        }, {
                            "id": "M10"
                        }, {
                            "id": "M04"
                        }, {
                            "id": "M06"
                        }, {
                            "id": "M01"
                        }, {
                            "id": "M11"
                        }, {
                            "id": "M00"
                        }, {
                            "id": "M09"
                        }
                    ]
                }

                    """
        # delete = {"from": "M04", "to": "M02"}
        rr.construct_adjacency_lists(inp)
        rr.delete_edge()
        np_tst.assert_array_equal(['M04', 'M11', 'M09'], rr.get_orphan_nodes())