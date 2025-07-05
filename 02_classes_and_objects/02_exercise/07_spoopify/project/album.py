from project.song import Song


class Album:
    def __init__(self, name:str, *args):
        self.name = name
        self.published:bool = False
        self.songs:list = list(args)

    def add_song(self, song: Song):
        if self.published:
            return "Cannot add songs. Album is published."
        if song.single:
            return f"Cannot add {song.name}. It's a single"
        if song in self.songs:
            return "Song is already in the album."
        self.songs.append(song)
        return f"Song {song.name} has been added to the album {self.name}."

    def remove_song(self, song_name: str):
        song = next((s for s in self.songs if s.name == song_name), None)
        if self.published:
            return "Cannot remove songs. Album is published."
        if not song:
            return "Song is not in the album."
        self.songs.remove(song)
        return f"Removed song {song.name} from album {self.name}."

    def publish(self):
        if self.published:
            return f"Album {self.name} is already published."
        self.published = True
        return f"Album {self.name} has been published."

    def details(self):
        song_info = '\n'.join(f" == {song.get_info()}" for song in self.songs)
        return f"Album {self.name}\n{song_info}"