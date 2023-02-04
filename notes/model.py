# Заметка должна содержать идентификатор, заголовок, тело заметки и дату/время создания
# или последнего изменения заметки.
import datetime as dt


class Note:
    """
    Protected structure and updater
    """

    def __init__(self, id=0, title='', body='', created=dt.datetime.now(), updated=dt.datetime.now()):
        # To do: value checks
        self.__id = id
        self.__title = title
        self.__body = body
        self.__created = created
        self.__updated = updated

    def update(self, title='', body=''):
        self.__title = title
        self.__body = body
        updated = dt.datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def body(self):
        return self.__body

    @property
    def created(self):
        return self.__created

    @property
    def updated(self):
        return self.__updated

    def __str__(self):
        return f'{self.__id} \t {self.__title} \t {self.__updated.isoformat()} '
