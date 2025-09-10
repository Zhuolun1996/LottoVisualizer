from django.test import TestCase
from django.template import Context, Template


class SplitFilterTests(TestCase):
    def render(self, tpl, ctx=None):
        ctx = ctx or {}
        return Template(tpl).render(Context(ctx))

    def test_split_default_comma(self):
        out = self.render("{% load visualizer_extras %}{% for x in s|split %}{{ x }}-{% endfor %}", {"s": "a,b,c"})
        self.assertEqual(out, "a-b-c-")

    def test_split_custom_delimiter(self):
        out = self.render("{% load visualizer_extras %}{% for x in s|split:'|' %}{{ x }} {% endfor %}", {"s": "a|b|c"})
        self.assertEqual(out, "a b c ")

    def test_split_strips_and_ignores_empty(self):
        out = self.render("{% load visualizer_extras %}{% for x in s|split:',' %}[{{ x }}]{% endfor %}", {"s": " 1, 2,, 3 , ,"})
        self.assertEqual(out, "[1][2][3]")

    def test_split_none(self):
        out = self.render("{% load visualizer_extras %}{% for x in s|split %}{{ x }}{% empty %}empty{% endfor %}", {"s": None})
        self.assertEqual(out, "empty")
