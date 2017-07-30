#!/usr/bin/python
#coding=utf-8
import __init__
import sys
from openpyxl import load_workbook


#reload(sys)
#sys.setdefaultencoding('utf-8')

def testReadExcel():
	wb = load_workbook(r'c:\Users\lujun.xlj\Desktop\data\dictchannel.xlsx')
	ws = wb[wb.get_sheet_names()[0]]
	for row in ws.rows:
		cells = [c.value if c.value else '<null>' for c in row]
		print ",".join(cells)

def main():
	testReadExcel()

if __name__ == '__main__':
	main()
