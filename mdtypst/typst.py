# inspired from
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/html.py
# https://github.com/readthedocs/commonmark.py/blob/master/commonmark/render/renderer.py

import re

from . import log


# For images, we are looking for a pattern in the alt text,
# e.g. Some text { width =31% }
# grab the number for image scale, and grab the remainder for the caption.
# This should be "compatible" with other Markdown variants.
# e.g. Pandoc uses alt text for image caption.
imageWidthRe = re.compile(r"(.*){.*width\s*=\s*(\d+)%.*}")
# https://regex101.com/r/8zgA9P/2


class Renderer:
    def __init__(self):
        pass
        self.output = ""

    def __del__(self):
        pass
        print(self.output)

    def render(self, ast):
        for node, entering in ast.walker():
            print(f"{'ENTER' if entering else 'EXIT'}-{node.t}: {node.literal}")
            getattr(self, node.t)(node, entering)
        return

    def block_quote(self, node, entering):
        # attrs = self.attrs(node)
        if entering:
            self.output += '"'
        else:
            self.output += '"'

    def code(self, node, entering):
        self.output += "`"
        self.output += node.literal
        self.output += "`"

    def code_block(self, node, entering):
        if entering:
            self.output += node.literal

    def document(self, node, entering):
        if entering:
            pass
        else:
            pass

    def emph(self, node, entering):
        if entering:
            self.output += "_"

        else:
            self.output += "_"

    def escape(self, text):
        return text

    def findSource(self, node):
        if node.sourcepos:
            return node.sourcepos[1][0]
        else:
            return self.findSource(node.parent)

    def heading(self, node, entering):
        if not hasattr(node.first_child, "literal"):
            self.markdownError(node, "Empty heading")
            return

        if entering:
            self.output += "=" * node.level + " "
        else:
            self.output += "\n"

    def image(self, node, entering):
        if entering:
            pass

    def item(self, node, entering):
        # attrs = self.attrs(node)
        if entering:
            if node.parent.list_data["type"] == "ordered":
                self.output += f"+ "
            else:
                self.output += f"- "
        else:
            pass

    def linebreak(self, node=None, entering=None):
        self.cr("linebreak")

    def link(self, node, entering):
        if entering:
            pass  # node.destination  # TODO: deal with "#fragments"
        else:
            pass

    def list(self, node, entering):
        # node.list_data
        if entering:
            self.output += "\n"
        else:
            pass

    def markdownError(self, node, msg):
        log.error(f"{self.infile}:{self.findSource(node)}: {msg}")

    def paragraph(self, node, entering):
        if entering:
            if node.parent is not None:
                if node.parent.t == "block_quote":
                    return
            if node.parent.parent is not None:
                if node.parent.parent.t == "list":
                    # if grandparent.list_data["tight"]:
                    # TODO maybe deal with tight/loose lists
                    return
            self.output += "\n"
        else:
            self.output += "\n"

    # Softbreaks are just CRs in the input, within paragraph
    # it becomes a space.   #TODO might not need this for Typst
    def softbreak(self, node=None, entering=None):
        self.output += " "

    def strong(self, node, entering):
        if entering:
            self.output += "*"
        else:
            self.output += "*"

    def tag(self, name, attrs=None, selfclosing=None):
        return

    def text(self, node, entering=None):
        # TODO: what to do with text in image "alt" field?
        # we are currently using it for non-standard "width"
        # and remaining text could be printed.  For now, drop it.
        if node.parent is not None:
            if node.parent.t == "image":
                self.output += f'#figure(image("{node.parent.destination}"),caption: [{node.literal}],)'
                return
        self.output += node.literal

    def thematic_break(self, node, entering):
        # attrs = self.attrs(node)
        pass

        # node.title

    # From spec: Text between < and > that looks like an HTML tag is parsed
    # as a raw HTML tag and will be rendered in HTML without escaping. Tag
    # and attribute names are not limited to current HTML tags, so custom
    # tags (and even, say, DocBook tags) may be used.

    def html_inline(self, node, entering):
        self.output += node.literal

    def html_block(self, node, entering):
        self.output += node.literal

    def custom_inline(self, node, entering):
        self.output += node.literal

    def custom_block(self, node, entering):
        self.output += node.literal
