import unittest
import os
from importlib import import_module

class GeneralTestCase(unittest.TestCase):
    def __init__(self, methodName, day: int):
        super(GeneralTestCase, self).__init__(methodName)
        self.day = day
        self.path_to_data = os.path.join(os.path.dirname(__package__), f"data/day_{day}/data.txt")
        self.part_1_solution = get_solution_record(day, 1)
        self.part_2_solution =  get_solution_record(day, 2)

    def part1Test(self):
        module = import_module(f"solutions.day_{self.day}.part1")
        result = module.solve(self.path_to_data)
        self.assertEqual(str(result), self.part_1_solution)

    def part2Test(self):
        module = import_module(f"solutions.day_{self.day}.part2")
        result = module.solve(self.path_to_data)
        self.assertEqual(str(result), self.part_2_solution)


def load_tests(loader, tests, pattern):

    days_with_solutions = 1

    test_suite = unittest.TestSuite()
    for i in range(1, days_with_solutions+1):
        test_suite.addTest(GeneralTestCase('part1Test', i))
        test_suite.addTest(GeneralTestCase('part2Test', i))
    return test_suite

def path_to_data(day):
    return os.path.join(os.path.dirname(__package__), f"data/day_{day}/my_data.txt")

def get_solution_record(day: int, part: int):
    record_location = os.path.join(os.path.dirname(__package__), f"data/day_{day}/part{part}_solution.txt")
    with open(record_location) as file:
        recorded_solution = file.read().strip()
    return recorded_solution

# def test_case(day: int, part: int):
#     def test(self):
#         module = import_module(f"solutions.day_{day}.part{part}")
#         path = path_to_data(day)
#         with open(path_to_solution(day, part)) as file:
#             expected = file.read().strip()
#         result = str(module.solve(path)).strip()
#         self.assertEqual(result, expected)
#     return test

# def generate_tests(days_with_soluions: int):
#     for pt in range(1, 3):
#         for i in range(1, days_with_soluions+1):
#             test_name: str = f"test_day_{i}_part_{pt}" 
#             test = test_case(i, pt)
#             setattr(TestDay, test_name, test)
#             TestDays.addTest(TestDay)

if __name__ == '__main__':
    unittest.main()