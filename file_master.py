#!/usr/bin/env python3
import os, json

def build(path):
    tree = {}
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if os.path.isdir(full):
            tree[name] = build(full)
        else:
            tree[name] = 'file'
    return tree

if __name__ == '__main__':
    data = {
        'LOCAL': build('directory_GPT'),
        'VIRTUAL': build('virtual')
    }
    with open('file_tree.json', 'w') as f:
        json.dump(data, f, indent=2)
    print('file_tree.json generated')
