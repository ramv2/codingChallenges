import unittest
from mass_calculator import MassCalculator

class testMassCalculator(unittest.TestCase):

    def setUp(self):
        self.mc = MassCalculator()

    def tearDown(self):
        self.mc = None

    def test_simple(self):
        json ="""
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1.6,
                        "units": "kilograms"
                    }, {
                        "name": "sulfur",
                        "mass": 36,
                        "units": "mol"
                    }, {
                        "name": "oxygen",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            } 

        """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("3625.34", mg)
        self.assertEquals("7.99", mlb)

    def test_malformed(self):
        # Second component doesn't have mass.
        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1.6,
                        "units": "kilograms"
                    }, {
                        "name": "sulfur",                        
                        "units": "mol"
                    }, {
                        "name": "oxygen",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            }

            """
        with self.assertRaises(ValueError):
            self.mc.calculate_mass(json)

        # Unusual characters present in units of the first component.
        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1.6,
                        "units": "ki%%lograms"
                    }, {
                        "name": "sulfur",
                        "mass": 36,                        
                        "units": "mol"
                    }, {
                        "name": "oxygen",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            }

            """
        with self.assertRaises(ValueError):
            self.mc.calculate_mass(json)

        # Mass of the first component is not a number.
        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1.6n,
                        "units": "kilograms"
                    }, {
                        "name": "sulfur",
                        "mass": 36,                        
                        "units": "mol"
                    }, {
                        "name": "oxygen",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            }

            """
        with self.assertRaises(Exception):
            self.mc.calculate_mass(json)

        # Element name of the third component is invalid.
        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1.6,
                        "units": "kilograms"
                    }, {
                        "name": "sulfur",
                        "mass": 36,                        
                        "units": "mol"
                    }, {
                        "name": "oxygene",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            }

            """
        with self.assertRaises(ValueError):
            self.mc.calculate_mass(json)

    def test_various_units(self):
        json = """
            {
                "components": [{
                        "name": "sulfur",
                        "mass": 100,
                        "units": "kilomol"
                    }
                ]
            } 

            """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("3206500.00", mg)
        self.assertEquals("7069.12", mlb)

        json = """
            {
                "components": [{
                        "name": "sulfur",
                        "mass": 100,
                        "units": "kilomoles"
                    }
                ]
            } 

            """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("3206500.00", mg)
        self.assertEquals("7069.12", mlb)

        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1,
                        "units": "megagrams"
                    }
                ]
            } 

            """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("1000000.00", mg)
        self.assertEquals("2204.62", mlb)

        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 10000,
                        "units": "millipound"
                    }
                ]
            } 

            """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("4535.92", mg)
        self.assertEquals("10.00", mlb)

        json = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1,
                        "units": "gigaounces"
                    }
                ]
            } 

            """
        mg, mlb = self.mc.calculate_mass(json)
        self.assertEquals("28349523125.00", mg)
        self.assertEquals("62500000.00", mlb)