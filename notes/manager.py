# Main controller
#
import datetime as dt
from model import Note
from config import GONFIG

if GONFIG.get("DB") == "JSON":
    from db_json import *


class NotesManager:
    """
    Manages list of notes in memory and in file
    """

    def __init__(self):
        self.__notes = dict()
        try:
            content = DB().load()
            if content:
                notes = [Converter.note_from_DB(line) for line in content]
                if notes:
                    self.__notes = dict({note.id: note for note in notes})
        except FileNotFoundError:
            self.__notes = dict()

    def add_note(self, title='', body='') -> int:
        """
        returns id of added note
        """
        id = max(self.__notes.keys()) + 1 if self.__notes else 1
        self.__notes[id] = Note(id, title, body)
        return id

    def delete_note(self, id: int) -> bool:
        """
        returns True if deleted, False if not found
        """
        if id in self.__notes.keys():
            self.__notes.pop(id)
            return True
        else:
            return False

    def update_note(self, id, title='', body='') -> bool:
        """
        returns True if updated, False if not found
        """
        edited_note = self.__notes.get(id)
        if edited_note:
            edited_note.update(title, body)
            return True
        else:
            return False

    def get_list(self, changedfrom=dt.datetime.min,
                 changedto=dt.datetime.max) -> list():
        """
        returns list of notes (as text)
        """
        selected_notes = [note for note in self.__notes.values()
                          if (note.updated >= changedfrom and note.updated <= changedto)]
        return list(map(str, selected_notes))

    def save_all(self) -> int:
        """
        saves notes to file
        returns count of updated rows
        """
        notes_tmp = list([Converter.note_to_DB(note)
                         for note in self.__notes.values()])
        DB().save(notes_tmp)
        return len(notes_tmp)

    def delete_all(self) -> int:
        """
        delete notes from memory
        returns count of deleted rows
        """
        cnt = 0
        for id in list(self.__notes.keys()):
            self.delete_note(id)
            cnt += 1
        return cnt

    def get_note_as_text(self, id) -> str:
        edited_note = self.__notes.get(id)
        if edited_note:
            return f'{edited_note}:\n{edited_note.body}'
        else:
            return None
