# -*- coding: utf-8 -*-
# pylint: disable=import-error
from renpy.display.core import Displayable
from renpy.display.layout import Null
from renpy.display import im
import renpy.exports
import renpy.ast

from modloader import modast

class ConditionalDisplayable(Displayable):
    __slots__ = ('conditions', 'children', 'child')
    nosave = ['child']

    def after_setstate(self):
        self.child = self.children[0]

    def __init__(self, *args, **kwargs):
        super(ConditionalDisplayable, self).__init__()

        if len(args) & 1 == 1:
            raise ValueError("%s requires an even number of arguments."%(self.__class__,))

        self.conditions = tuple(((arg,) if isinstance(arg,basestring) else () if arg is None else arg for arg in args[0::2]))
        self.children = tuple((renpy.easy.displayable(d) if d is not None else Null() for d in args[1::2]))
        self.child = None

    def _duplicate(self, args):
        if not self._duplicatable:
            return self

        rv = self._copy(args)
        rv.children = tuple((c._duplicate(args) for c in self.children))
        rv.child = None

        return rv

    def _in_current_store(self):
        new_children = tuple((c._in_current_store() for c in self.children))

        if all((c is old for c, old in zip(new_children, self.children))):
            return self

        rv = self._copy()
        rv.children = new_children
        rv.child = None

        return rv

    def get_current_child(self, update=False):
        if update or self.child is None:
            for condition, child in zip(self.conditions, self.children):
                if all(getattr(renpy.store, attr, False) for attr in condition):
                    self.child = child
                    return child
            raise ValueError("No child matched ConditionalDisplayable current conditions: %s"%(self.conditions,))

        return self.child

    def render(self, width, height, st, at):
        return self.get_current_child().render(width,height,st,at)

    def event(self, ev, x, y, st):
        return self.get_current_child().event(ev, x, y, st)

    def set_style_prefix(self, prefix, root):
        super().set_style_prefix(prefix, root)

        for i in self.visit():
            i.set_style_prefix(prefix, root)

    def get_placement(self):
        return self.get_current_child().get_placement()

    def visit(self):
        return self.children

    def per_interact(self):
        old_value = self.child
        self.get_current_child(update=True) # Sets self.child
        if self.child != old_value:
            renpy.display.render.redraw(self, 0)

    def predict_one(self):
        renpy.display.predict.displayable(self.get_current_child())

    def _clear(self):
        self.child = None
        self.children = ()
        self.conditions = ()

known_expressions = {
    (u'angry',): ("cr/remy_angry.png","cr/remy_angry_c.png"),
    (u'look',): ("cr/remy_look.png","cr/remy_look_c.png"),
    (u'normal',): ("cr/remy_normal.png","cr/remy_normal_c.png"),
    (u'sad',): ("cr/remy_sad.png","cr/remy_sad_c.png"),
    (u'shy',): ("cr/remy_shy.png","cr/remy_shy_c.png"),
    (u'smile',): ("cr/remy_smile.png","cr/remy_smile_c.png"),
    (u'angry',u'b'): ("cr/remy_angry_b.png", "cr/remy_angry_d.png"),
    (u'look',u'b'): ("cr/remy_look_b.png", "cr/remy_look_d.png"),
    (u'normal',u'b'): ("cr/remy_normal_b.png", "cr/remy_normal_d.png"),
    (u'sad',u'b'): ("cr/remy_sad_b.png", "cr/remy_sad_d.png"),
    (u'shy',u'b'): ("cr/remy_shy_b.png", "cr/remy_shy_d.png"),
    (u'smile',u'b'): ("cr/remy_smile_b.png", "cr/remy_smile_d.png"),
}

def define_wrapper_images():
    for (attributes, image_bases) in known_expressions.items():
        renpy.exports.image(
            (u'remy',u'remykeepitc',)+attributes,
            # (u'remy',)+attributes,
            ConditionalDisplayable(
                "remykeepit_4onen_enabled", image_bases[1],
                None, image_bases[0],
            ),
        )
        renpy.exports.image(
            (u'remy',u'remykeepitc',)+attributes+(u'flip',),
            # (u'remy',)+attributes+(u'flip',),
            ConditionalDisplayable(
                "remykeepit_4onen_enabled", im.Flip(image_bases[1],horizontal=True),
                None, im.Flip(image_bases[0],horizontal=True),
            ),
        )


def attributes_known(attributes):
    if attributes is None or len(attributes) < 1:
        return False
    return attributes in known_expressions or (attributes[-1] == u'flip' and attributes[:-1] in known_expressions)

def link_images_from_node(start_node,max_depth=10000):
    node_queue = [(start_node,0)]
    while node_queue:
        node, depth = node_queue.pop(0)
        if depth > max_depth:
            print "Max depth reached, dropping node from", node.filename, node.linenumber
            continue
        if isinstance(node, renpy.ast.Label) and node.name in [u'chapter1chars',u'chapter2chars',u'chapter3chars',u'chapter4chars',u'_call_syscheck_105',u'_call_syscheck_106']:
            continue # Don't recurse into chapter select menu
        if node.next:
            node_queue.append((node.next, depth + 1))
        # When we show Remy, show the remykeepit expression
        if isinstance(node, (renpy.ast.Scene,renpy.ast.Show)):
            old_imspec = node.imspec
            old_attributes = old_imspec[0]
            if old_attributes[0] != u'remy':
                continue
            if attributes_known(old_attributes[1:]):
                new_imspec = ((u'remy',u'remykeepitc',) + old_attributes[1:],) + old_imspec[1:]
                node.imspec = new_imspec
        # When we say something, show the remykeepit expression
        if isinstance(node, (renpy.ast.Say)):
            old_attributes = node.attributes
            if node.who == u'Ry' and attributes_known(node.attributes):
                node.attributes = (u'remykeepitc',) + node.attributes
        # Branch on if statements to all paths
        if isinstance(node, renpy.ast.If):
            for _condition, block in node.entries:
                node_queue.append((block[0],depth+1))
        # Branch on menu statements to all paths
        if isinstance(node, renpy.ast.Menu):
            for _label, _condition, block in node.items:
                node_queue.append((block[0],depth+1))
        # Branch to the block of any node with one
        if isinstance(node, (renpy.ast.Label, renpy.ast.While, renpy.ast.UserStatement, renpy.ast.TranslateBlock)) and len(node.block) > 0:
            node_queue.append((node.block[0],depth+1))

def link_images(ml):
    # Three points in the game to start the search from
    # - Remy chooses to keep the lipstick on
    # - Remy5
    # - The true ending
    lipstick_choice_menu = ( ml.find_label('remy4')
        .search_menu()
        .search_say()
    )

    link_images_from_node(lipstick_choice_menu.node)
    link_images_from_node(modast.find_label('remy5'))
    link_images_from_node(modast.find_label('trueendings'))