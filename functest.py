# coding=utf-8
# !/usr/bin/python
import copy
import os
import re
import shutil
from string import Template


# from openpyxl import load_workbook


def testWalkDir(rootDir):
    print rootDir
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        '''
        for d in dirs:
            print os.path.join(root, d)
        '''
        for f in files:
            if f.endswith('.jar'):
                print os.path.join(root, f)
                shutil.copy(os.path.join(root, f), distDir)


def testIO():
    # testio.py
    pass


def testLambda():
    g = lambda x: x * x
    print g(100)


def testRe():
    print [n for n in re.split(r'[,;]', 'xlj;hhq,,,,,,,,,xh') if len(n) > 0];
    m = re.search(r'xlj$xxx', 'this is xlj')
    if m:
        print "match==>%s" % m.start()
    else:
        print 'match <null>'
    m = re.match(r'(.+)xlj$', 'this is xlj')
    if m:
        print m.start(), m.group(0), m.group(1)
    else:
        print 'match <null>'

    arr = re.split(r"[\s+,;]", "this is xlj,hhq,xh;yeye nainai")
    print arr

    arr = re.findall('\w+', 'this is xlj')
    print arr

    print re.sub('xlj$', 'xljlovehhq,xh', 'this is xlj')


def testModule():
    print [n for n in dir(sys) if not n.startswith('_')]
    print copy.__all__
    print copy.__doc__
    print help(copy.copy)


def testYield():
    def flattern(list):
        try:
            try:
                list + ''
            except (TypeError), e:
                # print e
                print type(list)
            else:
                print 'else TypeError'
                raise TypeError
            for sub in list:
                for item in flattern(sub):
                    yield item
        except TypeError:
            yield list

    for num in flattern([1, 2, 3, [4, 5, [10]]]):
        print num


def testClass():
    # 关键，必须继承object，不然不能用super
    class Bird(object):
        song = None

        def __init__(self):
            self.song = 'guava'

        def sing(self):
            print self.song

    class HuangLi(Bird):
        mySong = None

        def __init__(self):
            super(HuangLi, self).__init__()
            self.mySong = 'huangli'

        def sing(self):
            print self.mySong, self.song

    Bird().sing()
    HuangLi().sing()


def testFunctions():
    def fa(x, y, *other):
        print (x, y)
        print other

    def fa(x, y, *other, **map):
        print (x, y)
        print other
        print map

    fa(1, 2, 4, 5, 6, 7, name='xlj', age=30)


def testCondition():
    a = b = 100
    print a is b

    if a is b:
        print 'a is b'
    elif a is not b:
        print 'ok'
    else:
        print 'fuck'

    print a is not b
    print a in [100, 200, 300]

    '''
    c = ''
    while not c:
        c = raw_input('input something:')
    '''

    for i in range(10):
        print i

    arr = [x for x in range(10)]
    print arr

    exec "print 'hello world'"
    print eval('1+2+3')


def testDict():
    map1 = dict(name='xlj', age=30)
    print map1
    map2 = dict([('name', 'xlj'), ('age', 30)])
    print map2
    print map1 == map2

    map = {}.fromkeys(['name', 'unit'])
    map.update({"xxx": "1212121"})
    print map
    print map.setdefault('test', 'N/A')
    map['test'] = 'ok'
    print map.setdefault('test', 'N/A')
    print map.has_key('test')
    print map.get('test')
    print map['test']
    print "map.get('12345')==>%s" % map.get('12345')
    try:
        print "map.get('12345')==>%s" % map['12345']
    except:
        print "error==>map['12345']"
    print map.items()
    print map.iteritems()
    print map.values()
    print map.itervalues()
    for key, val in map.iteritems():
        print 'key:%s,val:%s' % (key, val)
    print '=========================='
    for key in map:
        print 'key:%s,val:%s' % (key, map[key])

    del map['unit']
    print map.items()
    print len(map)


def testArray():
    a = [1]
    a[1:] = [2, 3, 4, 5]
    print a
    a.append([100])
    a.extend([200])
    print a
    print min(a), max(a), len(a), a.count(1)
    a.insert(0, 999)
    print a
    a.reverse()
    print sorted(a)
    print a
    a.sort()
    print a;
    print a.pop(len(a) - 1)
    a.sort(lambda x, y: y - x);
    print a


def testString():
    print 'this is %s %s' % ('hello', 'world')
    print Template('$x is nidaye==>$x,$y').substitute(x='xlj', y='xs')
    print 'this is xlj'.find('xlj')
    print 'this is xlj'.find('hhq')
    print ','.join(['1', '2', '3', '4', '5'])
    print '       this is xlj      '.strip()
    print len('12234232')
    if (bool('')):
        print '<null>'
    else:
        print "'' not null"
    print "FFF".lower()


def testSimple():
    print os.getcwd()
    print os.path.abspath("../")


def main():
    testString()



if __name__ == '__main__':
    main()

print __name__