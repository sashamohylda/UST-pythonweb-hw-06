"""
main.py — CLI CRUD program for the university database.

Usage examples:
  python main.py -a create -m Teacher -n 'Boris Johnson'
  python main.py -a list -m Teacher
  python main.py -a update -m Teacher --id 3 -n 'Andry Bezos'
  python main.py -a remove -m Teacher --id 3
  python main.py -a create -m Group -n 'AD-101'
  python main.py -a create -m Student -n 'John Doe' --group_id 1
  python main.py -a create -m Subject -n 'Physics' --teacher_id 2
"""

import argparse
import sys

from database import get_session
from models import Teacher, Group, Student, Subject, Grade


MODEL_MAP = {
    "Teacher": Teacher,
    "Group": Group,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}


# ─── CRUD helpers ─────────────────────────────────────────────────────────────

def action_create(args):
    session = get_session()
    model_cls = MODEL_MAP[args.model]
    try:
        kwargs = {}
        if args.model == "Teacher":
            kwargs["fullname"] = args.name
        elif args.model == "Group":
            kwargs["name"] = args.name
        elif args.model == "Student":
            kwargs["fullname"] = args.name
            if args.group_id is None:
                print("Error: --group_id required for Student")
                sys.exit(1)
            kwargs["group_id"] = args.group_id
        elif args.model == "Subject":
            kwargs["name"] = args.name
            if args.teacher_id is None:
                print("Error: --teacher_id required for Subject")
                sys.exit(1)
            kwargs["teacher_id"] = args.teacher_id
        else:
            print(f"Create not supported for {args.model}")
            sys.exit(1)

        obj = model_cls(**kwargs)
        session.add(obj)
        session.commit()
        print(f"Created {args.model}: {obj}")
    finally:
        session.close()


def action_list(args):
    session = get_session()
    model_cls = MODEL_MAP[args.model]
    try:
        rows = session.query(model_cls).all()
        if not rows:
            print(f"No {args.model} records found.")
        for row in rows:
            print(row)
    finally:
        session.close()


def action_update(args):
    session = get_session()
    model_cls = MODEL_MAP[args.model]
    try:
        if args.id is None:
            print("Error: --id required for update")
            sys.exit(1)
        obj = session.get(model_cls, args.id)
        if obj is None:
            print(f"{args.model} with id={args.id} not found.")
            sys.exit(1)

        if args.model in ("Teacher", "Group", "Student", "Subject"):
            if args.name:
                attr = "fullname" if args.model in ("Teacher", "Student") else "name"
                setattr(obj, attr, args.name)
        if args.model == "Student" and args.group_id:
            obj.group_id = args.group_id
        if args.model == "Subject" and args.teacher_id:
            obj.teacher_id = args.teacher_id

        session.commit()
        print(f"Updated {args.model}: {obj}")
    finally:
        session.close()


def action_remove(args):
    session = get_session()
    model_cls = MODEL_MAP[args.model]
    try:
        if args.id is None:
            print("Error: --id required for remove")
            sys.exit(1)
        obj = session.get(model_cls, args.id)
        if obj is None:
            print(f"{args.model} with id={args.id} not found.")
            sys.exit(1)
        session.delete(obj)
        session.commit()
        print(f"Removed {args.model} with id={args.id}")
    finally:
        session.close()


ACTION_MAP = {
    "create": action_create,
    "list": action_list,
    "update": action_update,
    "remove": action_remove,
}


def main():
    parser = argparse.ArgumentParser(description="University DB CLI")
    parser.add_argument("-a", "--action", required=True, choices=ACTION_MAP.keys(),
                        help="CRUD action: create | list | update | remove")
    parser.add_argument("-m", "--model", required=True, choices=MODEL_MAP.keys(),
                        help="Model to operate on: Teacher | Group | Student | Subject | Grade")
    parser.add_argument("-n", "--name", help="Name / fullname value")
    parser.add_argument("--id", type=int, help="Record ID (for update / remove)")
    parser.add_argument("--group_id", type=int, help="Group ID (for Student)")
    parser.add_argument("--teacher_id", type=int, help="Teacher ID (for Subject)")

    args = parser.parse_args()
    ACTION_MAP[args.action](args)


if __name__ == "__main__":
    main()
