# -*- coding: utf-8 -*-
# pylint: disable=import-error
import renpy.exports

from modloader import modinfo
from modloader.modclass import Mod, loadable_mod

@loadable_mod
class AwSWMod(Mod):
    name = "RemyKeepIt"
    version = "0.01"
    author = "4onen"
    nsfw = False
    dependencies = ["MagmaLink"]

    @classmethod
    def mod_load(cls):
        import jz_magmalink as ml
        import remykeepit
        remykeepit.define_wrapper_images()
        remykeepit.link_images(ml)

    @classmethod
    def mod_complete(cls):
        pass
