#!/usr/bin/python
# coding=utf-8

def hit(a1, b1, b2, A, B):
    a2 = round(round(A * B / 1.17 - a1 * b1) / b2);
    hit = False;
    if (abs(a1 - a2) <= 200):
        if (int(round(a1 * b1 * 1.17)) + int(round(a2 * b2 * 1.17)) == A * B):
            hit = True;
            print("success ==> a1=%s,a2=%s,b1=%s,b2=%s\na1*b1*1.17+a2*b2*1.17=%s" % (a1, a2, b2, b2,
                int(round(a1 * b1 * 1.17)) + int(round(a2 * b2 * 1.17))));
    return hit


A = ''
while not A:
    try:
        A = long(raw_input("input A:"))
    except:
        pass
B = ''
while not B:
    try:
        B = long(raw_input("input B:"))
    except:
        pass

print 'A:%s, B:%s' % (A, B)

a1 = int(round(A / 1.17))
find = False
for b1 in range(1, B + 1):
    b2 = B - b1
    if not find:
        find = hit(a1, b1, b2, A, B)

if not find:
    print 'no result available'
