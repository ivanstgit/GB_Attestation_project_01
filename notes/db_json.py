import datetime as dt
import json
import os
from config import GONFIG
from model import Note
from pathlib import Path


class Converter:
    datetime_format = "%Y-%m-%dT%H:%M:%S.%f"

    def note_to_DB(note: Note):
        """ converter to JSON compatible types """
        return {
            "id": note.id,
            "title": note.title,
            "body": note.body,
            "created": note.created.isoformat(),
            "updated": note.updated.isoformat()
        }

    def note_from_DB(note: dict):
        """ converter to JSON compatible types """
        return Note(id=note.get("id"),
                    title=note.get("title"),
                    body=note.get("body"),
                    created=dt.datetime.fromisoformat(note.get("created")),
                    updated=dt.datetime.fromisoformat(note.get("updated"))
                    )


class DB:
    def __init__(self):
        self.__filename = Path(__file__).parent.joinpath(
            GONFIG.get("JSON").get("filename"))
        self.__encoding = GONFIG.get("JSON").get("encoding")

    def load(self):
        if os.path.getsize(self.__filename):  # check file is not empty
            with open(self.__filename, 'r', encoding=self.__encoding) as in_file:
                return json.load(in_file)
        return None

    def save(self, notes) -> int:
        with open(self.__filename, 'w', encoding=self.__encoding) as out_file:
            return json.dump(fp=out_file, obj=notes)
        return None
