"""РК1 по ПиКЯП: вариант Б-14 (CD-диск — библиотека CD-дисков)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CDDisc:
    id: int
    title: str
    performer_surname: str
    duration_minutes: int
    library_id: int  # Внешний ключ для связи «один-ко-многим».


@dataclass(frozen=True)
class CDLibrary:
    id: int
    name: str


@dataclass(frozen=True)
class LibraryDisc:
    disc_id: int
    library_id: int  # Связь «многие-ко-многим».


def make_test_data():
    libraries = [
        CDLibrary(1, "Центральная фонотека"),
        CDLibrary(2, "Музыкальная медиатека"),
        CDLibrary(3, "Библиотека редких записей"),
    ]
    discs = [
        CDDisc(1, "Акустические истории", "Иванов", 48, 1),
        CDDisc(2, "Городские ритмы", "Петров", 42, 1),
        CDDisc(3, "Джазовые вечера", "Смирнов", 57, 2),
        CDDisc(4, "Симфония света", "Соколова", 63, 3),
    ]
    library_discs = [
        LibraryDisc(1, 1),
        LibraryDisc(1, 2),
        LibraryDisc(2, 1),
        LibraryDisc(3, 2),
        LibraryDisc(4, 3),
    ]
    return discs, libraries, library_discs


def query_b1(discs, libraries):
    """Все пары диск/библиотека по связи 1:N, по названию диска."""
    library_by_id = {library.id: library for library in libraries}
    pairs = [
        (disc.title, library_by_id[disc.library_id].name)
        for disc in discs
        if disc.library_id in library_by_id
    ]
    return sorted(pairs, key=lambda pair: (pair[0].casefold(), pair[1].casefold()))


def query_b2(discs, libraries):
    """Библиотеки и число их дисков по связи 1:N, по возрастанию."""
    counts = [
        (library.name, sum(disc.library_id == library.id for disc in discs))
        for library in libraries
    ]
    return sorted(
        counts,
        key=lambda pair: (pair[1], pair[0].casefold()),
    )


def query_b3(discs, libraries, library_discs):
    """Каждый диск исполнителя на «ов» и его библиотеки по связи M:N."""
    library_by_id = {library.id: library for library in libraries}
    matching_discs = sorted(
        (disc for disc in discs if disc.performer_surname.casefold().endswith("ов")),
        key=lambda disc: (disc.performer_surname.casefold(), disc.title.casefold(), disc.id),
    )
    return [
        (
            disc.performer_surname,
            disc.title,
            sorted(
                [
                    library_by_id[link.library_id].name
                    for link in library_discs
                    if link.disc_id == disc.id and link.library_id in library_by_id
                ],
                key=str.casefold,
            ),
        )
        for disc in matching_discs
    ]


def main():
    discs, libraries, library_discs = make_test_data()

    print("Б1. Диски и библиотеки (1:N), сортировка по дискам")
    for title, library in query_b1(discs, libraries):
        print(f"  {title} — {library}")

    print("\nБ2. Число дисков в библиотеках (1:N), по возрастанию")
    for library, count in query_b2(discs, libraries):
        print(f"  {library}: {count}")

    print("\nБ3. Исполнители на «ов» и библиотеки (M:N)")
    for surname, title, library_names in query_b3(discs, libraries, library_discs):
        print(f"  {surname} — {title}: {', '.join(library_names) or 'нет библиотек'}")


if __name__ == "__main__":
    main()
