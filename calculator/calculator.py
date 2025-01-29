from calculator.alphabet import (charValues, charValuesInverted, charConsonantValuesInverted, charConsonantValues, units,
                                 tens, teens, scores, types, traceur)
import re


class Calculator:
    """Main Class of the AlphaNumeric Calculator"""

    def __init__(self):
        self.charValues = charValues
        self.charConsonantValues = charConsonantValues
        self.charInvertedValues = charValuesInverted
        self.charConsonantInvertedValues = charConsonantValuesInverted

    def perform_task(self, input_main):
        """Takes the main input and returns the final pronostics"""

        # ToDo- 1: Output the combinations
        combination_list = self.make_combination_list(input_string=input_main)

        results = []  # Initialize result
        # ToDo- 2: Execute AlphaNum process
        for combination in combination_list:
            # call def alpha_num_process
            output = self.alpha_num_process(combination=combination)

            # ToDo- 3: Check if item of output list is in the predefined Traceur list
            for item in output:
                if int(item) in traceur:
                    item_traceur = [combination, item]
                    results.append(item_traceur)
        return results

    def alpha_num_process(self, combination):
        """Take the main input and process the alphanumeric calculation"""

        # Todo- 1: Extract Number from main input
        numbers = self.extract_all_numbers_from_string(combination)

        # Todo- 2 Replace figures by french letter in the main input
        words = ''
        if numbers:
            for number in numbers:
                number_to_letter = self.convert_to_french(int(number))  # convert number to french letter
                updated_combination = combination.replace(number, number_to_letter)
                words += updated_combination.upper().strip()
        else:
            words = combination.upper().strip()

        # ToDo - 3 Calculate the sum of letters
        sum_char = 0
        sum_char_inverted = 0
        sum_consonant = 0
        sum_consonant_inverted = 0

        output = []  # Initialize a list container

        if words:
            # loop through each word  words
            for word in words.split():
                # loop through each character in each word
                for char in word:
                    # For normal alphabet
                    if char in charValues:
                        sum_char += charValues[char]

                    # For inverted alphabet
                    if char in charValuesInverted:
                        sum_char_inverted += charValuesInverted[char]

                    # For consonant
                    if char in charConsonantValues:
                        sum_consonant += charConsonantValues[char]

                    # For inverted consonant
                    if char in charConsonantValuesInverted:
                        sum_consonant_inverted += charConsonantValuesInverted[char]

        output.extend([sum_char, sum_consonant, sum_char_inverted, sum_consonant_inverted])
        return output

    def make_combination_list(self, input_string):
        """Takes the French converted string and return a list of combination"""

        combination_list = []

        for my_type in types:
            for score in scores:
                combination = input_string + ' ' + my_type + ' ' + score[0] + ' ' + score[1]
                combination_list.append(combination)

        return combination_list

    def extract_all_numbers_from_string(self, input_string):
        """
        Extracts all numbers from the input string.

        Args:
            input_string (str): The string to extract numbers from.

        Returns:
            list: A list of all numeric parts as strings.
        """
        # Use a regular expression to find all numbers
        number_parts = re.findall(r'\d+', input_string)
        return number_parts

    def convert_to_french(self, number):
        """Takes an integer and return its converted French spelling"""

        if number < 0 or number > 999999:
            return "Nombre hors limite"  # Handle numbers outside the range

        if number == 0:
            return units[0]

        words = ""

        # Handle thousands
        if number // 1000 > 0:
            thousands = number // 1000
            if thousands == 1:
                words += "mille "
            else:
                words += self.convert_to_french(thousands) + " mille "
            number %= 1000

        # Handle hundreds
        if number // 100 > 0:
            hundreds = number // 100
            if hundreds == 1:
                words += "cent "
            else:
                words += units[hundreds] + " cent "

            if number % 100 == 0:
                return words.strip()  # If the number is an exact hundred

            words += "" if number % 100 != 0 else " "
            number %= 100

        # Handle tens and units
        if number > 0:
            if number < 10:
                words += units[number]
            elif number < 20:
                words += teens[number]
            else:
                ten = number // 10
                unit = number % 10

                if ten in (7, 9):
                    words += tens[ten] + " " + teens[unit]
                else:
                    words += tens[ten]
                    if unit > 0:
                        if ten == 8:
                            words += "-" + units[unit]  # Avoid 'quatre-vingt-un'
                        elif unit == 1:
                            words += "-et-un"  # Handle cases like 21, 31, 41...
                        else:
                            words += "-" + units[unit]

        return words.strip()




