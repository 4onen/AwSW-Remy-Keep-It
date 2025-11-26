# -*- coding: utf-8 -*-
# pylint: disable=import-error
import renpy.exports

from modloader import modinfo
from modloader.modclass import Mod, loadable_mod

def link_scenes(ml):
    ( ml.find_label('remy4')
        .search_menu()
        .add_choice(
            "Keep it.",
            jump='remykeepit_4onen_enabled',
        )
        .search_say()
        .link_from('remykeepit_4onen_enabled_end')
    )

    ( ml.find_label('remy5')
        .search_say("My body is ready.")
        .hook_to('remykeepit_4onen_c5_ready', return_link=True, condition='remykeepit_4onen_enabled')
    )

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
        link_scenes(ml)

    @classmethod
    def mod_complete(cls):
        pass
