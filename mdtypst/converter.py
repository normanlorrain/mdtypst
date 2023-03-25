import commonmark
from .typst import Renderer
from .typst import log


class Converter:
    def __init__(self, outputFileName):
        self.parser = commonmark.Parser()
        self.renderer = Renderer()

    def convert(self, inputFileNames):
        for inputFile in inputFileNames:
            log.info(inputFile)
            mdFile = open(inputFile, "r", encoding="utf-8")
            entireFile = mdFile.read()
            ast = self.parser.parse(entireFile)
            self.renderer.render(ast)
