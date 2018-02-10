import json

class MassCalculator:
    """Class to compute the mass of a given list of components.

    Attributes
    ----------
    atomic_weights : dict
        Dictionary containing the names and atomic masses (in grams) of the
        periodic table of elements as keys and values respectively.
    order_prefix : dict
        Dictionary containing the prefixes and the exponent of different
        orders of magnitude as keys and values respectively.
    allowed_units : array-like
        List of allowed mass units for the components.
    """

    atomic_weights = {'hydrogen' : 1.00794, 'helium' : 4.002602, 'lithium' :
                          6.941, 'beryllium' : 9.012182, 'boron' : 10.811,
                      'carbon' : 12.0107, 'nitrogen' : 14.0067, 'oxygen' :
                          15.9994, 'fluorine' : 18.9984032, 'neon' : 20.1797,
                      'sodium' : 22.98977, 'magnesium' : 24.305, 'aluminum' :
                          26.981538, 'silicon' : 28.0855, 'phosphorus' :
                          30.973761, 'sulfur' : 32.065, 'chlorine' : 35.453,
                      'argon' : 39.948, 'potassium' : 39.0983, 'calcium' :
                          40.078, 'scandium' : 44.95591, 'titanium' : 47.867,
                      'vanadium' : 50.9415, 'chromium' : 51.9961, 'manganese' :
                          54.938049, 'iron' : 55.845, 'cobalt' : 58.9332,
                      'nickel' : 58.6934, 'copper' : 63.546, 'zinc' : 65.409,
                      'gallium' : 69.723, 'germanium' : 72.64, 'arsenic' :
                          74.9216, 'selenium' : 78.96, 'bromine' : 79.904,
                      'krypton' : 83.798, 'rubidium' : 85.4678, 'strontium' :
                          87.62, 'yttrium' : 88.90585, 'zirconium' : 91.224,
                      'niobium' : 92.90638, 'molybdenum' : 95.94,
                      'technetium' : 98, 'ruthenium' : 101.07, 'rhodium' :
                          102.9055, 'palladium' : 106.42, 'silver' :
                          107.8682, 'cadmium' : 112.411, 'indium' : 114.818,
                      'tin' : 118.71, 'antimony' : 121.76, 'tellurium' :
                          127.6, 'iodine' : 126.90447, 'xenon' : 131.293,
                      'cesium' : 132.90545, 'barium' : 137.327, 'lanthanum' :
                          138.9055, 'cerium' : 140.116, 'praseodymium' :
                          140.90765, 'neodymium' : 144.24, 'promethium' :
                          145, 'samarium' : 150.36, 'europium' : 151.964,
                      'gadolinium' : 157.25, 'terbium' : 158.92534,
                      'dysprosium' : 162.5, 'holmium' : 164.93032, 'erbium' :
                          167.259, 'thulium' : 168.93421, 'ytterbium' :
                          173.04, 'lutetium' : 174.967, 'hafnium' : 178.49,
                      'tantalum' : 180.9479, 'tungsten' : 183.84, 'rhenium' :
                          186.207, 'osmium' : 190.23, 'iridium' : 192.217,
                      'platinum' : 195.078, 'gold' : 196.96655, 'mercury' :
                          200.59, 'thallium' : 204.3833, 'lead' : 207.2,
                      'bismuth' : 208.98038, 'polonium' : 209, 'astatine' :
                          210, 'radon' : 222, 'francium' : 223, 'radium' :
                          226, 'actinium' : 227, 'thorium' : 232.0381,
                      'protactinium' : 231.03588, 'uranium' : 238.02891,
                      'neptunium' : 237, 'plutonium' : 244, 'americium' :
                          243, 'curium' : 247, 'berkelium' : 247,
                      'californium' : 251, 'einsteinium' : 252, 'fermium' :
                          257, 'mendelevium' : 258, 'nobelium' : 259,
                      'lawrencium' : 262, 'rutherfordium' : 261, 'dubnium' :
                          262, 'seaborgium' : 266, 'bohrium' : 264, 'hassium' :
                          277, 'meitnerium' : 268, 'darmstadtium' : 281,
                      'roentgenium' : 272, 'copernicium' : 285, 'nihonium' :
                          286, 'flerovium' : 289, 'moscovium' : 289,
                      'livermorium' : 293, 'tennessine' : 294, 'oganesson' :
                          294}

    order_prefix = {"yocto" : -24, "zepto" : -21, "atto" : -18, "femto" :
                    -15, "pico" : -12, "nano" : -9, "micro" : -6, "milli" :
                    -3, "centi" : -2, "deci" : -1, "deca" : 1, "hecto" : 2,
                    "kilo" : 3, "mega" : 6, "giga" : 9, "tera" : 12, "peta" :
                    15, "exa" : 18, "zetta" : 21, "yotta" : 24}

    gram_conversion = {"gram" : 1.0, "ounce" : 28.349523125, "pound" :
                    453.59237}

    allowed_units = ["gram", "ounce", "pound", "mol"]

    def calculate_mass(self, json_input):
        """
        Function to compute the mass of a given list of components.

        Parameters
        ----------
        json_input : str
            Input JSON string containing a list of components.

        Returns
        -------
        mass_g : str
            String representation of the total mass in grams rounded to 2
            decimal places.
        mass_lb : str
            String representation of the total mass in pounds rounded to 2
            decimal places.

        Raises
        ------
        ValueError
            If the JSON string couldn't be parsed properly.
            If any of the components is underspecified.
            If the name of the element is invalid.
            If invalid units are specified.

        Exception
            If invalid mass is specified.
        """

        # Try parsing the string.
        try:
            data = json.loads(json_input)
        except ValueError:
            raise ValueError("Couldn't parse input properly. Please check "
                             "input and try again.")

        # Total mass in grams.
        total_mass_g = 0.0

        # Loop through the list and add individual mass to total.
        for comp in data["components"]:

            # Check if component is underspecified.
            if len(comp) < 3:
                raise ValueError("Underspecified component: {}. Please check "
                                 "input and try again.".format(comp))

            if "name" not in comp or "mass" not in comp or "units" not in comp:
                raise ValueError("Underspecified component: {}. Please check "
                                 "input and try again.".format(comp))

            c_name = comp["name"]

            # Check if the name of the element is valid.
            if c_name.strip().lower() not in self.atomic_weights:
                raise ValueError("Invalid element name specified: {}. Please "
                                 "check element name and try again.".format(
                    comp["name"]))

            c_mass = comp["mass"]

            # Check if the mass of the element is valid. Simply multiply by 1
            # to check if any exceptions are raised. If it does raise an
            # exception, then value of comp["mass"] wasn't a number.
            try:
                c_mass *= 1.0
            except Exception:
                raise Exception("Invalid mass specified: {}. Please check "
                                "element mass and try again.".format(str(
                    c_mass)))

            c_units = comp["units"].lower()

            # Check if the units of mass are valid and come from the allowed
            # list of units.
            valid_unit = False
            for unit in self.allowed_units:
                if unit in c_units:
                    valid_unit = True
                    break

            if not valid_unit:
                raise ValueError("Invalid units specified: {}. Please check "
                                "element mass units and try again. Allowed "
                                "units are gram, ounce, pound and "
                                "mol.".format(c_units))

            # We have only checked if the unit specified contains in-part,
            # any of the strings in the list of allowed units. We need to
            # further process it to identify the order of magnitude and the
            # precise unit. Here, I'm assuming that if there are any
            # trailing unescaped special characters, I should simply delete
            # them and process the units as though they were not present.
            order, allowed_unit = self.process_units(c_units)
            # print c_name, order, allowed_unit

            # Unit conversion.
            if allowed_unit == "gram":
                c_mass *= 1.0
            elif allowed_unit == "mol":
                c_mass *= self.atomic_weights[c_name]
            elif allowed_unit == "ounce":
                c_mass *= 28.349523125
            else: # allowed_unit == "pound"
                c_mass *= 453.59237

            c_mass *= (10 ** order)
            total_mass_g += c_mass

        total_mass_lb = total_mass_g / 453.59237

        mass_g = "{:.2f}".format(total_mass_g)
        mass_lb = "{:.2f}".format(total_mass_lb)
        return mass_g, mass_lb


    def process_units(self, units):
        """
        Function to process the units of a component.

        Parameters
        ----------
        units : str
            Raw string containing the units of a component.

        Returns
        -------
        order : int
            Integer denoting the exponent in the order of magnitude, denoted
            by one of a specified number of prefixes.
        unit : str
            String containing one of the allowed units.

        Raises
        ------
        ValueError
            If the prefix term in the order of magnitude is not valid.
        """

        order = 0

        # Remove any trailing spaces or other unescaped characters.
        unit = units.strip()

        # Take care the extra 's' or 'es' at the end of units. Moles and
        # ounces could end in es. So, take care of them separately.
        if unit.endswith("es") and "mol" in units:
            unit = units[:-2]
        elif unit.endswith("s"):
            unit = units[:-1]

        # Now, we are left with exactly one of the allowed units with an
        # order of magnitude prefix.
        prefix = ""
        for u in self.allowed_units:
            if u in unit:
                prefix = unit[:-len(u)]
                unit = u
                break

        if prefix:
            if prefix in self.order_prefix:
                order = self.order_prefix[prefix]
            else:
                raise ValueError("Prefix term for the order of magnitude is "
                                "not specified correctly. Please check "
                                "unit: {} and try again.".format(units))
        return order, unit

if __name__ == "__main__":
    mc = MassCalculator()
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
                        "name": "oxygen",
                        "mass": 871,
                        "units": "grams"
                    }
                ]
            } 

            """
    mg, mlb = mc.calculate_mass(inp)
    print(mg, mlb)