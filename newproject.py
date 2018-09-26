#!/usr/bin/python
# coding=utf-8

# @author:xulujun


import fnmatch
import os
import re
import shutil

PATH_SEP = '/'

source_project_path = r'~/iworkspace/didi/newproject/dps_demo'
target_project_path = r'~/iworkspace/didi/newproject/dps_test'

artifact_map = {
    "dps-demo": "dps-test",
    "_dps_demo": "_dps_test"
}
package_map = {
    "com.didichuxing.dps.demo": "com.didichuxing.dps.test"
}

excludes = ['*/.git/*', '*/.idea/*', '*/target/*', '*.DS_Store', "*.iml"]
# includes = ["*/pom.xml", "*/CheckApiService.java"]
includes = []
home_dir = os.environ["HOME"]


def read_file(file_path):
    if os.path.isdir(file_path):
        return []
    f = open(file_path)
    lines = f.readlines()
    f.close()
    return lines


def clean_path(path):
    return path.replace("~", os.environ["HOME"])


def accept(path):
    for exclude in excludes:
        if fnmatch.fnmatch(path, exclude):
            return False
    for incude in includes:
        if fnmatch.fnmatch(path, incude):
            return True
    return False if len(includes) > 0 else True


def process_line(line):
    if not len(line):
        return line
    new_line = line
    replace_map = artifact_map.copy()
    replace_map.update(package_map)
    for key, val in replace_map.iteritems():
        if re.search(key, line):
            new_line = re.sub(key, val, new_line)
            # print "%s ==> %s" % (line, new_line)
    return new_line


def package_to_path(s):
    return PATH_SEP.join(s.split("."))


def write_file(target_root, source_root, source_full_path, lines):
    target_full_path = source_full_path.replace(source_root, target_root)
    # 替换关键字
    for key, val in artifact_map.iteritems():
        if target_full_path.find(key):
            target_full_path = target_full_path.replace(key, val)
    # 替换package路径
    for key, val in package_map.iteritems():
        path_pattern = package_to_path(key)
        if target_full_path.find(path_pattern) != -1:
            target_full_path = target_full_path.replace(path_pattern, package_to_path(val))
    print target_full_path
    target_dir = os.path.dirname(target_full_path);
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    f = open(target_full_path, r'w+')
    [f.write(line) for line in lines]
    f.close()


def test(source_dir):
    target_dir = clean_path(target_project_path)
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    # os.mkdir(target_dir)
    source_dir = clean_path(source_dir)
    if not os.path.exists(source_dir):
        raise IOError("source dir not exists, " + source_dir)
    list_dirs = os.walk(source_dir)
    for root, dirs, files in list_dirs:
        for f in files:
            path = os.path.join(root, f)
            if accept(path):
                print path
                new_lines = [process_line(line) for line in read_file(path)]
                write_file(target_dir, source_dir, path, new_lines)


test(source_project_path)
