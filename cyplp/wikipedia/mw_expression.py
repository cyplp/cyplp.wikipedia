from chameleon.tales import StructureExpr
from chameleon.codegen import template

from smc.mw import MediaWiki


class MediaWikiExpression(StructureExpr):
    def __call__(self, target, engine):
        compiler = engine.parse(self.expression)
        body = compiler.assign_value(target)

        def mw_render(content):
            return self.wrapper_class(MediaWiki(content).as_string())

        return body + template("from smc.mw import MediaWiki ; target = MediaWiki(target).as_string()",
                               target=target,
                               wrapper=self.wrapper_class)
