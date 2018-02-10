import unittest
from mass_calculator import MassCalculator

class testMassCalculator(unittest.TestCase):
    def test_simple(self):
        inp ="""
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
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("3625.34", mg)
        self.assertEquals("7.99", mlb)

    def test_malformed(self):
        # Second component doesn't have mass.
        inp = """
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
        mc = MassCalculator(input_from_user=False, json_input=inp)
        with self.assertRaises(ValueError):
            mc.calculate_mass()

        # Unusual characters present in units of the first component.
        inp = """
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
        mc = MassCalculator(input_from_user=False, json_input=inp)
        with self.assertRaises(ValueError):
            mc.calculate_mass()

        # Element name of the third component is invalid.
        inp = """
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
        mc = MassCalculator(input_from_user=False, json_input=inp)
        with self.assertRaises(ValueError):
            mc.calculate_mass()

    def test_various_units(self):
        inp = """
            {
                "components": [{
                        "name": "sulfur",
                        "mass": 100,
                        "units": "kilomol"
                    }
                ]
            } 

            """
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("3206500.00", mg)
        self.assertEquals("7069.12", mlb)

        inp = """
            {
                "components": [{
                        "name": "sulfur",
                        "mass": 100,
                        "units": "kilomoles"
                    }
                ]
            } 

            """
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("3206500.00", mg)
        self.assertEquals("7069.12", mlb)

        inp = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1,
                        "units": "megagrams"
                    }
                ]
            } 

            """
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("1000000.00", mg)
        self.assertEquals("2204.62", mlb)

        inp = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 10000,
                        "units": "millipound"
                    }
                ]
            } 

            """
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("4535.92", mg)
        self.assertEquals("10.00", mlb)

        inp = """
            {
                "components": [{
                        "name": "carbon",
                        "mass": 1,
                        "units": "gigaounces"
                    }
                ]
            } 

            """
        mc = MassCalculator(input_from_user=False, json_input=inp)
        mg, mlb = mc.calculate_mass()
        self.assertEquals("28349523125.00", mg)
        self.assertEquals("62500000.00", mlb)