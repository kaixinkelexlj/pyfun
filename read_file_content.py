# -*- coding: UTF-8 -*-
import os
import re


def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    return open(file_path).read()


def filter_file(file_patterns, file_name):
    if not file_patterns:
        return True
    for pattern in file_patterns:
        if re.search(pattern, file_name):
            return True
    return False

def read_file_content(dir, filter_patterns = []):
    walk_list = os.walk(dir)
    for root, dirs, files in walk_list:
        for file_name in files:
            if(not filter_file(filter_patterns, file_name)):
                continue
            file_poth = os.path.join(root, file_name)
            print("-------- read content: %s" % (file_poth))
            print(read_file_as_str(file_poth))

'''
如果全部文件都修改了可以不用写pattern，如果是只更新了几个文件，可以制定更新文件pattern
'''
if __name__ == '__main__':
    read_file_content("/Users/xulujun/kworkspace/kuaishou-ad-dmp-api/kuaishou-ad-dmp-component/src/main/java/com/kuaishou/ad/dmp/util/lambda", [".*\.java"])