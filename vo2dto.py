#!/usr/bin/python
# coding=utf-8

# @author:xulujun


import fnmatch
import os
import re

import sys

PATH_SEP = '/'

home_dir = os.environ["HOME"]

vo_map = {}
vo_map.setdefault("BaseVO", "BaseDTO")
test_vo_file = ''
test_update_file = ''

## 排除的文件
excludes = ['*/.git/*', '*/.idea/*', '*/target/*', '*.DS_Store', "*.iml", "*/generate.py", "*/archetype/*"]
# includes = ["*/pom.xml", "*/CheckApiService.java"]
includes = []
read_me_md = r'*/readme.md'


def read_file(file_path):
    if os.path.isdir(file_path):
        return []
    f = open(file_path)
    lines = f.readlines()
    f.close()
    return lines


def clean_path(path):
    return path.replace("~", home_dir)


def accept(path):
    for exclude in excludes:
        if fnmatch.fnmatch(path, exclude):
            return False
    for include in includes:
        if fnmatch.fnmatch(path, include):
            return True
    return False if len(includes) > 0 else True


def process_line(line):
    if not len(line):
        return line

    new_line = line
    for key, val in vo_map.items():
        new_line = new_line.replace(key, val)

    return new_line


def write_file(target_root, source_root, source_full_path, lines):
    target_full_path = source_full_path.replace(source_root, target_root)
    print(target_full_path)
    target_dir = os.path.dirname(target_full_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    f = open(target_full_path, r'w+')
    [f.write(line) for line in lines]
    f.close()


def register_vo(source_dir):
    list_dirs = os.walk(source_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            path = os.path.join(root, f)
            if accept(path) and (f.endswith("VO.java") or f.endswith("Vo.java")):
                # val = dict(path=path, dto=re.sub('(VO|Vo).java', 'DTO', f))
                vo_map.setdefault(f.replace('.java', ''), re.sub('(VO|Vo).java', 'DTO', f))
                print("register VO:%s" % (path))


def do_vo2dto(source_dir):
    # for key, val in vo_map.items():
    #     print("VO:%s -> DTO:%s" % (key, val["dto"]))
    list_dirs = os.walk(source_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            path = os.path.join(root, f)
            if accept(path) and (test_update_file == f):
                print("try update %s" % (f))
                new_lines = [process_line(line) for line in read_file(path)]
                print(''.join(new_lines))


def vo_to_do(project_path, test_vo_file, test_update_file):
    source_dir = clean_path(project_path)
    if not os.path.exists(source_dir):
        raise IOError("project dir not exists, " + source_dir)
    register_vo(source_dir)
    do_vo2dto(source_dir)

def main():
    if len(sys.argv) < 2 or '-h' in sys.argv or "--help" in sys.argv:
        print('usage: %s <vo2dto project path>' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    global test_vo_file
    global test_update_file
    project_path = sys.argv[1]
    if len(sys.argv) >= 3:
        test_vo_file = sys.argv[2]
    if len(sys.argv) >= 4:
        test_update_file = sys.argv[3]

    print('##### start execute vo2dto project:%s, test_vo_file:%s, test_update_file:%s'
          % (project_path,
             test_vo_file if test_vo_file else '<not_set>',
             test_update_file if test_update_file else '<not_set>'))

    vo_to_do(project_path, test_vo_file, test_update_file)
    print("##### action end")


if __name__ == '__main__':
    main()
