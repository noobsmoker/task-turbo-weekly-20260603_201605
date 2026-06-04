#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
VERSION = "1.0.0"
TASKS_FILE = os.path.expanduser('~/.taskturbo/tasks.json')

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE) as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Task Turbo')
    parser.add_argument('command', choices=['add', 'list', 'done', 'remove'])
    parser.add_argument('task', nargs='?')
    parser.add_argument('-p', '--priority', choices=['low', 'medium', 'high'], default='medium')
    args = parser.parse_args()
    tasks = load_tasks()
    if args.command == 'add':
        if not args.task:
            parser.error("Task description required")
        task = {'id': len(tasks) + 1, 'description': args.task, 'priority': args.priority, 'created': str(datetime.now()), 'completed': False}
        tasks.append(task)
        save_tasks(tasks)
        print(f"Added task #{task['id']}")
    elif args.command == 'list':
        for t in tasks:
            status = '✓' if t['completed'] else '○'
            print(f"{status} [{t['priority']}] {t['description']}")
    elif args.command == 'done':
        for t in tasks:
            if str(t['id']) == args.task:
                t['completed'] = True
                save_tasks(tasks)
                print(f"Task #{t['id']} completed")
                return
        print("Task not found")
    elif args.command == 'remove':
        tasks = [t for t in tasks if str(t['id']) != args.task]
        save_tasks(tasks)
        print("Task removed")
if __name__ == '__main__':
    main()
