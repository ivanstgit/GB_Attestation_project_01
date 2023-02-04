# Реализовать консольное приложение заметки, с сохранением, чтением,
# добавлением, редактированием и удалением заметок.
# python cli.py add --title "новая заметка" –msg "тело новой заметки"
# Приложение должно запускаться без ошибок, должно уметь сохранять данные
# в файл, уметь читать данные из файла, делать выборку по дате, выводить на
# экран выбранную запись, выводить на экран весь список записок, добавлять
# записку, редактировать ее и удалять.

import argparse
import datetime as dt
from manager import NotesManager

nm = NotesManager()

# Functions for controller launch, with result printing


def add_note(args):
    res = nm.add_note(title=args.title,
                      body=args.body)
    print(f'New note added with id: {res}')
    nm.save_all()


def edit_note(args):
    res = nm.update_note(id=args.id,
                         title=args.title,
                         body=args.body)
    if res:
        print(f'Note updated')
    else:
        print(f'Note not found')
    nm.save_all()


def delete_note(args):
    res = nm.delete_note(id=args.id)
    if res:
        print(f'Note deleted')
    else:
        print(f'Note not found')
    nm.save_all()


def read_note(args):
    print(nm.get_note_as_text(id=args.id))


def show_list(args):
    if args.changedfrom:
        try:
            ch_from = dt.datetime.fromisoformat(args.changedfrom)
        except ValueError:
            print(f'Incorrect ISO format: {args.changedfrom}')
            return
    else:
        ch_from = dt.datetime.min
    if args.changedto:
        try:
            ch_to = dt.datetime.fromisoformat(args.changedto)
        except ValueError:
            print(f'Incorrect ISO format: {args.changedto}')
            return
    else:
        ch_to = dt.datetime.min
    print("\n".join(nm.get_list(changedfrom=ch_from, changedto=ch_to)))

# Command line interface


def cli():
    parser = argparse.ArgumentParser(description='Note manager')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_add = subparsers.add_parser('add', help='add new note')
    parser_add.add_argument('-t', '--title', type=str, dest='title',
                            help='note title', required=True)
    parser_add.add_argument('-b', '--body', type=str, dest='body',
                            help='note body', required=True)
    parser_add.set_defaults(func=add_note)

    parser_edit = subparsers.add_parser('edit', help='edit existing note')
    parser_edit.add_argument('-id', '--id', type=int, dest='id',
                             help='note id', required=True)
    parser_edit.add_argument('-t', '--title', type=str, dest='title',
                             help='note title', required=True)
    parser_edit.add_argument('-b', '--body', type=str, dest='body',
                             help='note body', required=True)
    parser_edit.set_defaults(func=edit_note)

    parser_delete = subparsers.add_parser(
        'delete', help='delete existing note')
    parser_delete.add_argument('-id', '--id', type=int, dest='id',
                               help='note id', required=True)
    parser_delete.set_defaults(func=delete_note)

    parser_read = subparsers.add_parser('read', help='read existing note')
    parser_read.add_argument('-id', '--id', type=int, dest='id',
                             help='note id', required=True)
    parser_read.set_defaults(func=read_note)

    parser_show_list = subparsers.add_parser(
        'show_list', help='show notes in list [in date interval]')
    parser_show_list.add_argument('-from', '--changedfrom', type=str, dest='changedfrom',
                                  help='note changed from (iso like 2024-02-04T23:00:29)', required=False)
    parser_show_list.add_argument('-to', '--changedto', type=str, dest='changedto',
                                  help='note changed from (iso like "2024-02-04T23:00:29.496840")', required=False)
    parser_show_list.set_defaults(func=show_list)

    args = parser.parse_args()
    if args:
        args.func(args)
    else:
        parser.print_help()
