import unittest
from Parse_Methods.google_parser_struct import GoogleParser
from Parse_Methods.yandex_parser_struct import YandexParser
from Parse_Methods.google_webdriver import GoogleWebDriver
from Parse_Methods.yandex_webdriver import YandexWebDriver
from Classes.Patent import Patent
import Problem_Solution.test_prob_sol as sol
import Translation.translation as translate


class TestModule(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        link = "https://patents.google.com/patent/RU2011116043A/ru"
        google_driver = GoogleWebDriver()
        google_parser = GoogleParser(google_driver)
        cls.p = Patent(link, google_parser)

    def test_get_assignee(self):
        asignee = self.p.get_assignee()
        self.assertEqual(asignee, 'Открытое акционерное общество "Волжский трубный завод" (RU)')

    def test_get_authors(self):
        author = self.p.get_authors()
        self.assertEqual(author, 'Дмитрий Юрьевич Звонарёв\n')

    def test_get_struct(self):
        test_list_1 = ['При использовании изобретения обеспечивается повышение пыле- и газоулавливания неорганизованных выбросов '
                       'от металлургического агрегата.']
        test_list_2 = ['Задачей данного изобретения является усовершенствование описанной линии для повышения качества поперечных швов и,'
                       ' следовательно, работоспособности спирально-шовных труб в целом.']

        problems_1 = sol.get_struct(1)
        problems_2 = sol.get_struct(12)
        self.assertEqual(problems_1, test_list_1)
        self.assertEqual(problems_2, test_list_2)

    def test_translate_text(self):
        solution = translate.translate_text(4)
        self.assertEqual(solution, 'Метод и устройства процесса завивки с четырьмя роликами симметричного выражения')

if __name__ == "__main__":
    unittest.main()