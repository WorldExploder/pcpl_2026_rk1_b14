"""Проверки результатов трех запросов РК1."""

import unittest

from main import CDDisc, CDLibrary, LibraryDisc, make_test_data, query_b1, query_b2, query_b3


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
        self.assertEqual(
            rows,
            [
                ("Иванов", "Акустические истории", ["Музыкальная медиатека", "Центральная фонотека"]),
                ("Петров", "Городские ритмы", ["Центральная фонотека"]),
                ("Смирнов", "Джазовые вечера", ["Музыкальная медиатека"]),
            ],
        )

    def test_empty_collections_and_library_without_discs(self):
        self.assertEqual(query_b1([], []), [])
        self.assertEqual(query_b2([], []), [])
        self.assertEqual(query_b2([], [CDLibrary(9, "Пустая")]), [("Пустая", 0)])
        self.assertEqual(query_b3([], [], []), [])

    def test_b3_preserves_discs_without_links_and_uses_ids(self):
        discs = [
            CDDisc(1, "Одинаковое название", "ИВАНОВ", 40, 1),
            CDDisc(2, "Одинаковое название", "Иванов", 42, 2),
        ]
        libraries = [CDLibrary(1, "Первая"), CDLibrary(2, "Вторая")]
        self.assertEqual(
            query_b3(discs, libraries, [LibraryDisc(2, 2)]),
            [
                ("ИВАНОВ", "Одинаковое название", []),
                ("Иванов", "Одинаковое название", ["Вторая"]),
            ],
        )

    def test_b3_requires_suffix_at_end(self):
        discs = [
            CDDisc(1, "Первый", "Иванова", 40, 1),
            CDDisc(2, "Второй", "СИДОРОВ", 42, 1),
        ]
        self.assertEqual(query_b3(discs, [CDLibrary(1, "Фонд")], []),
                         [("СИДОРОВ", "Второй", [])])


if __name__ == "__main__":
    unittest.main()
