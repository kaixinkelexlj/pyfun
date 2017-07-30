#!/usr/bin/env python
#****************************************************************#
# ScriptName: hubble_keyword_script.py
# Author: fangliang@taobao.com
# Create Date: 2013-04-09 16:43
# Modify Author: fangliang@taobao.com
# Modify Date: 2013-04-21 12:24
# Function: 
#***************************************************************#


import httplib
import os
import re
import sys
import time
import traceback

from array import array

OPTIMIZE = False
try:
    # Python 2.5 and above
    from ctypes import *
    OPTIMIZE = True
except ImportError:
    try:
        sys.path.append('/usr/alisys/dragoon/libexec/alimonitor_lib')
        from ctypes import *
        OPTIMIZE = True
    except ImportError, e:
        pass

try:
    from simplejson import _speedups
except ImportError:
    _speedups = None

ESCAPE = re.compile(r'[\x00-\x19\\"\b\f\n\r\t]')
ESCAPE_ASCII = re.compile(r'([\\"/]|[^\ -~])')
ESCAPE_DCT = {
    # escape all forward slashes to prevent </script> attack
    '/': '\\/',
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
for i in range(0x20):
    ESCAPE_DCT.setdefault(chr(i), '\\u%04x' % (i,))

# assume this produces an infinity on all machines (probably not guaranteed)
INFINITY = float('1e66666')

def floatstr(o, allow_nan=True):
    # Check for specials.  Note that this type of test is processor- and/or
    # platform-specific, so do tests which don't depend on the internals.

    if o != o:
        text = 'NaN'
    elif o == INFINITY:
        text = 'Infinity'
    elif o == -INFINITY:
        text = '-Infinity'
    else:
        return str(o)

    if not allow_nan:
        raise ValueError("Out of range float values are not JSON compliant: %r"
            % (o,))

    return text


def encode_basestring(s):
    """
    Return a JSON representation of a Python string
    """
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, s) + '"'

def encode_basestring_ascii(s):
    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        except KeyError:
            n = ord(s)
            if n < 0x10000:
                return '\\u%04x' % (n,)
            else:
                # surrogate pair
                n -= 0x10000
                s1 = 0xd800 | ((n >> 10) & 0x3ff)
                s2 = 0xdc00 | (n & 0x3ff)
                return '\\u%04x\\u%04x' % (s1, s2)
    return '"' + str(ESCAPE_ASCII.sub(replace, s)) + '"'
        
try:
    encode_basestring_ascii = _speedups.encode_basestring_ascii
    _need_utf8 = True
except AttributeError:
    _need_utf8 = False

class JSONEncoder(object):
   
    __all__ = ['__init__', 'default', 'encode', 'iterencode']
    item_separator = ', '
    key_separator = ': '
    def __init__(self, skipkeys=False, ensure_ascii=True,
            check_circular=True, allow_nan=True, sort_keys=False,
            indent=None, separators=None, encoding='utf-8'):
        
        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.sort_keys = sort_keys
        self.indent = indent
        self.current_indent_level = 0
        if separators is not None:
            self.item_separator, self.key_separator = separators
        self.encoding = encoding

    def _newline_indent(self):
        return '\n' + (' ' * (self.indent * self.current_indent_level))

    def _iterencode_list(self, lst, markers=None):
        if not lst:
            yield '[]'
            return
        if markers is not None:
            markerid = id(lst)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = lst
        yield '['
        if self.indent is not None:
            self.current_indent_level += 1
            newline_indent = self._newline_indent()
            separator = self.item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            separator = self.item_separator
        first = True
        for value in lst:
            if first:
                first = False
            else:
                yield separator
            for chunk in self._iterencode(value, markers):
                yield chunk
        if newline_indent is not None:
            self.current_indent_level -= 1
            yield self._newline_indent()
        yield ']'
        if markers is not None:
            del markers[markerid]

    def _iterencode_dict(self, dct, markers=None):
        if not dct:
            yield '{}'
            return
        if markers is not None:
            markerid = id(dct)
            if markerid in markers:
                raise ValueError("Circular reference detected")
            markers[markerid] = dct
        yield '{'
        key_separator = self.key_separator
        if self.indent is not None:
            self.current_indent_level += 1
            newline_indent = self._newline_indent()
            item_separator = self.item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = self.item_separator
        first = True
        if self.ensure_ascii:
            encoder = encode_basestring_ascii
        else:
            encoder = encode_basestring
        allow_nan = self.allow_nan
        if self.sort_keys:
            keys = dct.keys()
            keys.sort()
            items = [(k, dct[k]) for k in keys]
        else:
            items = dct.iteritems()
        _encoding = self.encoding
        _do_decode = (_encoding is not None
            and not (_need_utf8 and _encoding == 'utf-8'))
        for key, value in items:
            if isinstance(key, str):
                if _do_decode:
                    key = key.decode(_encoding)
            elif isinstance(key, basestring):
                pass
            # JavaScript is weakly typed for these, so it makes sense to
            # also allow them.  Many encoders seem to do something like this.
            elif isinstance(key, float):
                key = floatstr(key, allow_nan)
            elif isinstance(key, (int, long)):
                key = str(key)
            elif key is True:
                key = 'true'
            elif key is False:
                key = 'false'
            elif key is None:
                key = 'null'
            elif self.skipkeys:
                continue
            else:
                raise TypeError("key %r is not a string" % (key,))
            if first:
                first = False
            else:
                yield item_separator
            yield encoder(key)
            yield key_separator
            for chunk in self._iterencode(value, markers):
                yield chunk
        if newline_indent is not None:
            self.current_indent_level -= 1
            yield self._newline_indent()
        yield '}'
        if markers is not None:
            del markers[markerid]

    def _iterencode(self, o, markers=None):
        if isinstance(o, basestring):
            if self.ensure_ascii:
                encoder = encode_basestring_ascii
            else:
                encoder = encode_basestring
            _encoding = self.encoding
            if (_encoding is not None and isinstance(o, str)
                    and not (_need_utf8 and _encoding == 'utf-8')):
                o = o.decode(_encoding)
            yield encoder(o)
        elif o is None:
            yield 'null'
        elif o is True:
            yield 'true'
        elif o is False:
            yield 'false'
        elif isinstance(o, (int, long)):
            yield str(o)
        elif isinstance(o, float):
            yield floatstr(o, self.allow_nan)
        elif isinstance(o, (list, tuple)):
            for chunk in self._iterencode_list(o, markers):
                yield chunk
        elif isinstance(o, dict):
            for chunk in self._iterencode_dict(o, markers):
                yield chunk
        else:
            if markers is not None:
                markerid = id(o)
                if markerid in markers:
                    raise ValueError("Circular reference detected")
                markers[markerid] = o
            for chunk in self._iterencode_default(o, markers):
                yield chunk
            if markers is not None:
                del markers[markerid]

    def _iterencode_default(self, o, markers=None):
        newobj = self.default(o)
        return self._iterencode(newobj, markers)

    def default(self, o):
        
        raise TypeError("%r is not JSON serializable" % (o,))

    def encode(self, o):
        
        # This is for extremely simple cases and benchmarks...
        if isinstance(o, basestring):
            if isinstance(o, str):
                _encoding = self.encoding
                if (_encoding is not None 
                        and not (_encoding == 'utf-8' and _need_utf8)):
                    o = o.decode(_encoding)
            return encode_basestring_ascii(o)
        # This doesn't pass the iterator directly to ''.join() because it
        # sucks at reporting exceptions.  It's going to do this internally
        # anyway because it uses PySequence_Fast or similar.
        chunks = list(self.iterencode(o))
        return ''.join(chunks)

    def iterencode(self, o):
        
        if self.check_circular:
            markers = {}
        else:
            markers = None
        return self._iterencode(o, markers)

__all__ = ['JSONEncoder']

def dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        encoding='utf-8', **kw):
    
    # cached encoder
    if (skipkeys is False and ensure_ascii is True and
        check_circular is True and allow_nan is True and
        cls is None and indent is None and separators is None and
        encoding == 'utf-8' and not kw):
        return _default_encoder.encode(obj)
    if cls is None:
        cls = JSONEncoder
    return cls(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, encoding=encoding,
        **kw).encode(obj)

_default_encoder = JSONEncoder(
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    indent=None,
    separators=None,
    encoding='utf-8'
)

class WuManber:
  def __init__(self,keys,text,so='wumanber.so'):
    """ Initialise the WuManber object with required parameters
        Use __loadText__ and __loadKeywords__ to generate CTypes
        @keys:  list, string or filename
        @text:  string, url or filename
        @so:    name of the shared library linked to
    """
    self.so = CDLL('/usr/alisys/dragoon/libexec/alimonitor_lib/wumanber-x86_64.so')
    self.keywords =  None
    self.clist_of_cstrings = None # NOT A PYTHON TYPE
    self.len_clist_of_strings = None # NOT A PYTHON TYPE
    self.clist_of_counts = None # NOT A PYTHON TYPE
    self.ctext = None # NOT A PYTHON TYPE
    self.len_ctext = None # NOT A PYTHON TYPE
    self.text = None
    self.nocase = None # NOT A PYTHON TYPE
    self.wm = None # NOT A PYTHON TYPE
    self.keydict = {}
    self.__loadText__(text)
    self.__loadKeywords__(keys)
        
  def __loadText__(self,text):
    """ Parse the text provided by __init__. Depending on the type
        and whether the text is actually a URL, read the text into
        memory and create a CType c_char_p
        @text: string,url or filename
    """
    self.ctext = c_char_p(text)
    self.len_ctext = c_int(len(text))
      
  def __loadKeywords__(self,keys):
    """ Depending on the type() of keys, first create a Python list of
        keywords and then convert that to a C array of CType c_char_p
        @keys:  list, string or filename
    """
    self.keywords = keys
    self.clist_of_cstrings = (c_char_p*(len(self.keywords)))()
    self.len_clist_of_strings = c_int(len(self.clist_of_cstrings))
    self.clist_of_counts = (c_ulonglong*(len(self.keywords)))()
    i = 0
    for pystring in self.keywords:
      self.clist_of_cstrings[i] = c_char_p(pystring)
      self.keydict[i] = array('l', [])
      i+=1
  
  def __search_init__(self):
    """ Initialise the WuManber search by asking the shared library to
        prepare and return a WuManber struct. This struct is not actually
        used by this Python WuManber object or methods except to feed back
        into the shared library in the search_text method
    """
    if not self.clist_of_cstrings:
      raise StandardError,"CList of keywords not generated..."
    elif not self.len_clist_of_strings:
      raise StandardError,"CLength of keyword list not generated..."
    else:
      redundant_pointer = c_char_p('redundant')
      wm_ret = self.so.wm_search_init2( self.clist_of_cstrings,
                                        self.len_clist_of_strings,
                                        self.clist_of_counts,
                                        self.nocase,
                                        redundant_pointer
                                      )
      wm_long = c_ulonglong(wm_ret)
      self.wm = wm_ret
      
  def __callback__(self,idx,ptr):
    """ This callback is called by the C shared library every time a match
        is found in the text to be searched. Read this method in conjunction
        with WM_CALLBACK which is defined at the beginning of this file
    """
    idx = idx-1 # C starts counting at 1?
    self.keydict[idx].append(ptr)
    return 0
      
  def search_text(self,nocase=True,verbose=False):
    """ search_text is responsible for actually performing the text search
        @nocase:  boolean, whether to use case sensitive searching or not
        @verbose  boolean, whether to use the callback to print results or not
        @returns: int, the number of matches found in the text
    """
    s = time.time()
    if nocase:
      self.nocase = c_int(1)
    else:
      self.nocase = c_int(0)
    self.__search_init__()
    null_ptr1,null_ptr2 = POINTER(c_int)(), POINTER(c_int)()
    cb = null_ptr1
    wm_ret = self.so.wm_search_text(self.wm,self.ctext,self.len_ctext,cb,null_ptr2)
    return wm_ret

def analyseparam():
    if len(sys.argv) != 4:
        errmsg = "argv error.",str(sys.argv)
        errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":{}}
        print errstr
        sys.exit(1)
    filepath = sys.argv[1]
    keywords = []
    keywordstr=sys.argv[2]
    keywordstr=eval('"'+keywordstr+'"')
    keywordstr=keywordstr.decode('utf-8','ignore').encode('utf-8')
    varray = keywordstr.split(chr(2))
    if len(varray) == 1:
        sarray = varray[0].split(chr(1))
        if len(sarray) == 1:
            oldarray = keywordstr.split(",")
            for var in oldarray:
                v = var.split("@")
                if len(v) != 2:
                    errmsg = "keyword parm pattern err1 ",var
                    errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":{}}
                    print errstr
                    sys.exit(1)
                keywords.append({'k':v[0],'t':v[1],'n':0,'v':0})
        elif len(sarray) == 2:
            keywords.append({'k':sarray[0],'t':sarray[1],'n':0,'v':0})
        else:
            errmsg = "keyword parm pattern err2 ",varray[0]
            errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":{}}
            print errstr
            sys.exit(1)
    else:
        for var in varray:
            v = var.split(chr(1))
            if len(v) != 2:
                errmsg = "keyword parm pattern err3 ",var
                errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":{}}
                print errstr
                sys.exit(1)
            keywords.append({'k':v[0],'t':v[1],'n':0,'v':0})
    
    itemId = sys.argv[3]
    return filepath,keywords,itemId

def getfilecontent(filepath,keywords,start,end):
    conn=httplib.HTTPConnection('localhost:15776')
    conn.request('GET','/get?file='+filepath+'&begin='+str(start)+'&end='+str(end))
    result=conn.getresponse()
    resultStatus=result.status
    content=result.read()
    conn.close()
    return resultStatus,content

def getHubFileTest(filepath,itemId):
    #conn=httplib.HTTPConnection('127.0.0.1:8182')
    #conn.request('GET','/tail/'+filepath+'?encode=text&hungry=true&task_id='+str(itemId))
    #result=conn.getresponse()
    resultStatus=200
    f = open(filepath, 'r')
    content = f.read() 

    #print content 
    
    #content=result.read()
    #conn.close()
    return resultStatus,content,len(content)

def getHubFileContent(filepath,itemId):
    conn=httplib.HTTPConnection('127.0.0.1:8182')
    #conn.request('GET','/tail/'+filepath+'?encode=text&hungry=true&task_id='+str(itemId))
    conn.request('GET','/tail?file='+filepath+'&encode=text&hungry=true&task_id='+str(itemId))
    result=conn.getresponse()
    cLength = result.getheader("content-length")
    resultStatus=result.status
    content=result.read()
    conn.close()
    return resultStatus,content,cLength

def origCalculate(content, keywords):
    carray = content.split("\n")
    for line in carray:
        for k in keywords:
            if k['t'] =="c" and line.find(k['k']) != -1:
                k['n'] += 1
            if k['t'] =="s" or k['t'] == "a":
                reg = k['k']+r"\s{0,2}\W\s{0,2}(\d*\.\d*|0\.\d*[1-9]\d*$|\d*)"
                p = re.compile(reg)
                match = p.search(line)
                if match:
                    try:
                        valstr = match.group(1)
                        k['v'] += float(valstr)
                        k['n'] += 1
                    except:
                        pass

if __name__ == '__main__':
        
        filepath,keywords,itemId = analyseparam()

        count_keywords = {}
        aggr_keywords = {}
        for k in keywords:
            if k['t'] == "c":
                count_keywords[k['k']] = k
            elif k['t'] =="s" or k['t'] == "a":
                aggr_keywords[k['k']] = k

        try:
            start = time.time()
            status,content,cLength = getHubFileContent(filepath,itemId)
            #status,content,cLength = getHubFileTest(filepath,itemId)
            try:
                content=content.decode('utf-8').encode('utf-8')
            except Exception,e2:
                content=content.decode('gbk','ignore').encode('utf-8')

            result = []
            if status == 200:
                if OPTIMIZE:
                    try:
                        if count_keywords:
                            wm = WuManber(count_keywords.keys(), content)
                            wm.search_text()
                            for t in wm.keydict.keys():
                                count_keywords[wm.keywords[t]]['n'] = wm.clist_of_counts[t]

                        if aggr_keywords:
                            for k in keywords:
                                if k['t'] =="s" or k['t'] == "a":
                                    reg = k['k']+r"\s{0,2}\W\s{0,2}(\d*\.\d*|0\.\d*[1-9]\d*$|\d*)"
                                    k['reg'] = re.compile(reg)

                            carray = content.split("\n")
                            for line in carray:
                                for k in keywords:
                                    if k['t'] =="s" or k['t'] == "a":
                                        match = k['reg'].search(line)
                                        if match:
                                            try:
                                                valstr = match.group(1)
                                                k['v'] += float(valstr)
                                                k['n'] += 1
                                            except:
                                                pass
                    except:
                        OPTIMIZE = False
                        origCalculate(content, keywords)
                else:
                    origCalculate(content, keywords)

                end = time.time()
                executetime = end - start

                for k in keywords:
                    val = {}
                    ku=k['k']
                    if k['t'] == "c":
                        val = {"keyname":ku,"value":k['n'],"type":"count"}
                    elif k['t'] == "s":
                        val = {"keyname":ku,"value":k['v'],"type":"sum"}
                    elif k['t'] == "a":
                        if k['n'] != 0:
                                tmp = k['v']/k['n']
                        else:
                                tmp = k['v']
                        val = {"keyname":ku,"value":tmp,"type":"avg"}
                    result.append(val)
                    
                rst = {"collection_flag":0,"error_info":"size:"+str(cLength)+",exetime:"+str(executetime)+",optimize:"+str(OPTIMIZE),"MSG":result}
                msgstr=str(rst)
                msgstr=msgstr.replace("'keyname': u'","'keyname': '") 
                print dumps(rst)

            elif status == 304:
                end = time.time()
                executetime = end - start

                for k in keywords:
                    tpstr = ""
                    if k['t'] == "c":
                        tpstr = "count"
                    elif k['t'] == "s":
                        tpstr = "sum"
                    elif k['t'] == "a":
                        tpstr = "avg"
                    val = {"keyname":k['k'],"value":0,"type":tpstr}       
                    result.append(val)
                rst = {"collection_flag":0,"error_info":"size:"+str(cLength)+",exetime:"+str(executetime)+",optimize:"+str(OPTIMIZE),"MSG":result}
                msgstr=str(rst)
                msgstr=msgstr.replace("'keyname': u'","'keyname': '")
                print dumps(rst)
            else:
                errmsg = "return error!"+str(status)+content
                errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":[{}]}
                print errstr
        except Exception,e:
            traceback.print_exc()              
            errmsg = 'except error!',e
            errstr = {"collection_flag":1500,"error_info":errmsg,"MSG":[{}]}
            print errstr