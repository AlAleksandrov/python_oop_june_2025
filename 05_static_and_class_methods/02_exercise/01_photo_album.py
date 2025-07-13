from math import ceil


class PhotoAlbum:
    SIZE_PAGE = 4
    def __init__(self, pages: int):
        self.pages = pages
        self.photos: list[list[str]] = [[] for _ in range(self.pages)]

    @classmethod
    def from_photos_count(cls, photos_count: int):
        return cls(ceil(photos_count/cls.SIZE_PAGE))

    def add_photo(self, label: str):
        for i, page in enumerate(self.photos):
            if len(page) < self.SIZE_PAGE:
                page.append(label)
                return f"{label} photo added successfully on page {i + 1} slot {len(page)}"
        return "No more free slots"

    def display(self):
        separator = "-" * 11
        result = separator
        for page in self.photos:
            result += "\n" + ' '.join("[]" for x in page)
            result += "\n" + separator

        return result



album = PhotoAlbum(2)

print(album.add_photo("baby"))
print(album.add_photo("first grade"))
print(album.add_photo("eight grade"))
print(album.add_photo("party with friends"))
print(album.photos)
print(album.add_photo("prom"))
print(album.add_photo("wedding"))

print(album.display())
