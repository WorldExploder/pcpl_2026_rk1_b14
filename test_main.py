"""Проверки результатов трех запросов РК1."""

import unittest

from main import make_test_data, query_b1, query_b2, query_b3


class QueryTests(unittest.TestCase):
    def setUp(self):
        self.discs, self.libraries, self.library_discs = make_test_data()

    def test_b1_uses_one_to_many_and_sorts_by_disc(self):
        rows = query_b1(self.discs, self.libraries)
        self.assertEqual([row[0] for row in rows], sorted(d.title for d in self.discs))
        self.assertEqual(rows[0], ("Акустические истории", "Центральная фонотека"))

    def test_b2_counts_one_to_many_and_sorts_by_count(self):
        self.assertEqual(
            query_b2(self.discs, self.libraries),
            [
                ("Библиотека редких записей", 1),
                ("Музыкальная медиатека", 1),
                ("Центральная фонотека", 2),
            ],
        )

    def test_b3_uses_many_to_many_and_filters_surname(self):
        rows = query_b3(self.discs, self.libraries, self.library_discs)
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(surname.endswith("ов") for surname, _, _ in rows))
        self.assertEqual(
            {library for surname, _, library in rows if surname == "Иванов"},
            {"Центральная фонотека", "Музыкальная медиатека"},
        )


if __name__ == "__main__":
    unittest.main()
