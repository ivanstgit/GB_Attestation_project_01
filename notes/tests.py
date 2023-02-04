import datetime as dt
import time
from manager import NotesManager


def test():
    time_start = dt.datetime.now()
    time.sleep(1)
    nm = NotesManager()
    id1 = nm.add_note("title001", "body001")
    id2 = nm.add_note("title002", "body002")
    time.sleep(1)
    time_2 = dt.datetime.now()
    res = nm.update_note(id2, "title002fix", "body002fix")
    print(nm.get_note_as_text(id2))
    id3 = nm.add_note("title003", "body003")
    print("\n".join(nm.get_list()))
    print("\n".join(nm.get_list(changedto=time_start)))
    print("\n".join(nm.get_list(changedfrom=time_start -
          dt.timedelta(seconds=1), changedto=time_2)))
    res = nm.delete_note(id3)
    res = nm.save_all()
    nm2 = NotesManager()
    res = nm2.get_list() == nm.get_list() and \
        len(nm.get_list(changedfrom=time_start -
            dt.timedelta(seconds=1), changedto=time_2)) == 2
    # nm2.delete_all()
    nm2.delete_note(id1)
    nm2.delete_note(id2)
    nm2.save_all()
    return res


if __name__ == '__main__':
    print(test())
