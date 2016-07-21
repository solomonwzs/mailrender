#!/usr/bin/python2
# encoding: utf-8

__author__ = "Solomon Ng"
__license__ = 'MIT'

import markdown
from markdown.extensions import tables as exttables

from os import path
from bs4 import BeautifulSoup


def wrap_italic(s):
    return "*%s*" % s


def wrap_bold(s):
    return "**%s**" % s


def wrap_quote(s):
    return "`%s`" % s


def wrap_red_text(s):
    return "<span class=\"red\">%s</span>" % s


class SimpleRender(object):
    def __init__(self, style="default"):
        self.__md = ""
        self.__soup = None

    def __soup_append_style(self, css_select, style):
        for cs in css_select.split(","):
            for i in self.__soup.select(cs.strip()):
                i["style"] = i.get("style", "") + style

    def __soup_render_table_row(self):
        for table in self.__soup.select(".markdown-body table"):
            i = 0
            for row in table.select("tbody tr"):
                if i % 2 == 0:
                    row["style"] = row.get("style", "") + \
                        "background-color:#f8f8f8;"
                i += 1

    def render(self):
        html = markdown.markdown(
            self.__md,
            extensions=[exttables.TableExtension()])
        html = "<div class=\"markdown-body\">%s</div>" % html
        self.__soup = BeautifulSoup(html)
        self.__soup_append_style(
            ".markdown-body",
            ('font-family:"Helvetica Neue",Helvetica,"Segoe UI",Arial,'
             'freesans,sans-serif,"Apple Color Emoji","Segoe UI Emoji",'
             '"Segoe UI Symbol";'
             'font-size:16px;'
             'line-height:1.6;'
             'word-wrap:break-word;'
             'width:1280px;'
             'margin:auto;'
             'color:#333;')
        )
        self.__soup_append_style(
            (".markdown-body p,"
             ".markdown-body blockquote,"
             ".markdown-body ul,"
             ".markdown-body ol,"
             ".markdown-body dl,"
             ".markdown-body table,"
             ".markdown-body pre"),
            'margin-top:0;margin-bottom:16px;'
        )
        self.__soup_append_style(
            "h1, h2, h3, h4",
            ("margin-top:1em;"
             "margin-bottom:16px;"
             "font-weight:bold;"
             "line-height:1.4;")
        )
        self.__soup_append_style(
            ".markdown-body h1",
            ("padding-bottom:0.3em;"
             "font-size:2.25em;"
             "line-height:1.2;"
             "border-bottom:1px solid #eee;")
        )
        self.__soup_append_style(
            ".markdown-body h2",
            ("padding-bottom:0.3em;"
             "font-size:1.75em;"
             "line-height:1.225;"
             "border-bottom:1px solid #eee;")
        )
        self.__soup_append_style(
            ".markdown-body h3",
            ("font-size:1.5em;"
             "line-height:1.43;")
        )
        self.__soup_append_style(".markdown-body h4", "font-size:1.25em;")
        self.__soup_append_style(
            ".markdown-body table",
            ("display:block;"
             "width:100%;"
             "overflow:auto;"
             "word-break:normal;"
             "word-break:keep-all;"
             "border-spacing:0;"
             "border-collapse:collapse;")
        )
        self.__soup_append_style(
            ".markdown-body table th, .markdown-body table td",
            "padding:6px 13px;border:1px solid #ddd;"
        )
        self.__soup_append_style(
            ".markdown-body table th",
            "font-weight:bold;"
        )
        self.__soup_append_style(
            ".markdown-body ul",
            "padding-left:2em;"
        )
        self.__soup_append_style(
            ".markdown-body code",
            ('font-family:Consolas,"Liberation Mono",Menlo,Courier,monospace;'
             "padding:0.2em 0.4em;"
             "margin:0;"
             "font-size:85%;"
             "background-color:rgba(0,0,0,0.04);"
             "border-radius:3px;")
        )
        self.__soup_append_style(
            ".markdown-body span.red",
            ("color:#f33;"
             "padding:0.2em 0.4em;"
             "margin:0;"
             "background-color:rgba(200,32,32,0.15);"
             "border-radius:3px;")
        )
        self.__soup_render_table_row()
        return self.__soup.extract()

    def add_header1(self, header=""):
        self.__md += ("# %s\n" % header)

    def add_header2(self, header=""):
        self.__md += ("## %s\n" % header)

    def add_header3(self, header=""):
        self.__md += ("### %s\n" % header)

    def add_header4(self, header=""):
        self.__md += ("#### %s\n" % header)

    def add_text(self, text=""):
        self.__md += ("\n%s\n\n" % text)

    def add_table(self, theader=[], trows=[{}], align=None):
        table = "|%s|\n" % "|".join(theader)
        style = {"c": ":---:", "l": ":---", "r": "---:"}
        if align is None:
            table += "|%s|\n" % "|".join(["---"] * len(theader))
        else:
            table += "|%s|\n" % "|".join([style.get(a, "---")
                                          for a in align])
        for row in trows:
            l = []
            for h in theader:
                l.append(str(row.get(h, " ")))
            table += "|%s|\n" % "|".join(l)
        self.__md += (table + "\n")

    def add_list(self, text_list=[]):
        def f(ll, wcnt):
            text = ""
            for l in ll:
                if isinstance(l, tuple):
                    text += ("%s* %s\n" % (" " * wcnt, l[0]))
                    text += f(l[1], wcnt + 4)
                else:
                    text += ("%s* %s\n" % (" " * wcnt, l))
            return text
        self.__md += f(text_list, 0)

    def add_md_text(self, text):
        self.__md += text


if __name__ == "__main__":
    r = SimpleRender()
    r.add_header1("hello")
    r.add_header2("world")
    r.add_header3("world")
    r.add_text("text1")
    r.add_text("text2")
    r.add_table(["a", "b"], [{"a": 112, "b": 5463}, {"a": 3.05245}, {"b": 545},
                             {"a": 6.01, "b": 0.7}, {"b": wrap_italic(112)},
                             {"a": wrap_bold(45), "b": wrap_quote(0.98)},
                             {"a": wrap_bold(45), "b": wrap_red_text(123)},
                             ],
                ["r", "r"])
    r.add_list(["as", ("asda", ["123", "345"]), "asdas"])
    print r.render()
