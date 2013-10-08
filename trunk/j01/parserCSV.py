from pyrser.grammar import Grammar
from pyrser.error import ParseError
from pyrser import meta
from pyrser.parsing.node import Node
from pyrser.parsing.parserStream import Stream
import collections

class   parserCSV(Grammar):
    grammar = """ 
                Ini ::= [[[Base.id ';'] | [Base.id | ';'] | Base.eol | Base.eof]:data #magic(_,data)]*
                ;
                """
    entry = "Ini"

    def parse(self, source=None, entry=None):
        """Parse source using the grammar"""
        self.pop_ignore()
        if source is not None:
            self.parsed_stream(source)
        if entry is None:
            entry = self.entry
        if entry is None:
            raise ValueError("No entry rule name defined for {}".format(
                self.__class__.__name__))
        res = self.eval_rule(entry)
        if not res:
            raise error.ParseError(
                "Parse error with the rule {rule!r}",
                stream_name=self._stream.name,
                rule=entry,
                pos=self._stream._cursor.max_readed_position,
                line=self._stream.last_readed_line)
        return res

    def parse_file(self, filename: str, entry=None):
        """Parse filename using the grammar"""
        import os.path
        self.pop_ignore()
        if os.path.exists(filename):
            f = open(filename, 'r')
            self.parsed_stream(f.read(), os.path.abspath(filename))
        if entry is None:
            entry = self.entry
        if entry is None:
            raise ValueError("No entry rule name defined for {}".format(
                self.__class__.__name__))
        res = self.eval_rule(entry)
        if not res:
            raise error.ParseError(
                "Parse error with the rule {rule!r}",
                stream_name=self._stream.name,
                rule=entry,
                pos=self._stream._cursor.max_readed_position,
                line=self._stream.last_readed_line)
        return res

@meta.hook(parserCSV)
def magic(self, ret, data):
    if not hasattr(ret, "lines"):
        ret.lines = []
    if not hasattr(self, "line"):
        self.line = []
    if not hasattr(self, "l"):
        self.l = []
    if data.value == '\n' or data.value == "":
        if self.l != []:
            sstr = self.l.pop()
            if sstr.find(';') != -1:
                self.l.append(sstr)
                self.l.append("")
            else:
                self.l.append(sstr)
            for word in self.l:
                self.line.append(word.replace(';', ''))
        ret.lines.append(self.line)
        self.line = []
        self.l = []
        if data.value == "":
            return False
    else:
        self.l.append(data.value)
    return True
