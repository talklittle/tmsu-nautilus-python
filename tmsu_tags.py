#
# tmsu_tags.py
# version 0.1.0
#

import gi
gi.require_version('Nautilus', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Nautilus, GObject, Gtk, Gdk
import os
import subprocess
import urllib

class TmsuTagsExtension(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def get_columns(self):
        return Nautilus.Column(name="TmsuTagsExtension::tmsu_tags_column",
                               attribute="tmsu_tags",
                               label="TMSU tags",
                               description="List of TMSU tags"),

    def update_file_info(self, file):
        if file.get_uri_scheme() != 'file':
            return

        filename = urllib.unquote(file.get_uri()[7:])

        try:
            result = subprocess.check_output(['tmsu', 'tags', filename], cwd=os.path.dirname(filename)).strip()
            idx = result.find(': ')
            if idx >= 0:
                file.add_string_attribute('tmsu_tags', result[(idx+2):])
            else:
                file.add_string_attribute('tmsu_tags', '')
        except subprocess.CalledProcessError as e:
            pass

    def get_file_items(self, window, files):
        top_menuitem = Nautilus.MenuItem(name='TmsuTagsExtension::TMSU',
                                         label='TMSU',
                                         tip='TMSU tags')

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        add_tag_menuitem = Nautilus.MenuItem(name='TmsuTagsExtension::Add_Tag',
                                             label='Add tags',
                                             tip='Add tags')
        add_tag_menuitem.connect('activate', self.add_tag_activate_cb, files)
        submenu.append_item(add_tag_menuitem)

        return top_menuitem,

    def get_background_items(self, window, files):
        # TODO tmsu init
        return ()

    def add_tag_activate_cb(self, menu, files):
        win = AddTagsWindow(files)
        win.connect("delete-event", Gtk.main_quit)
        win.show_all()
        Gtk.main()

class AddTagsWindow(Gtk.Window):
    def __init__(self, files):
        self.files = files

        Gtk.Window.__init__(self, title="TMSU")
        self.set_size_request(200, 100)
        self.set_border_width(10)
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        prompt_text = 'Add (space-separated) tags to %d file%s' % (len(files), '' if len(files)==1 else 's')
        self.prompt_label = Gtk.Label(label=prompt_text)
        vbox.pack_start(self.prompt_label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.on_entry_activated)
        vbox.pack_start(self.entry, True, True, 0)

        self.button = Gtk.Button(label="Add")
        self.button.connect("clicked", self.on_button_clicked)
        vbox.pack_start(self.button, True, True, 0)

    def on_entry_activated(self, widget):
        self.add_tags()

    def on_button_clicked(self, widget):
        self.add_tags()

    def add_tags(self):
        tags = self.entry.get_text()
        try:
            subprocess.check_call(['tmsu', 'tag', '--tags={}'.format(tags)] + self.filenames())

            # TODO notify change

            self.close()
        except subprocess.CalledProcessError as e:
            # TODO display error dialog
            print(e)

    def filenames(self):
        filenames = []

        for file in self.files:
            if file.get_uri_scheme() != 'file':
                continue
            filename = urllib.unquote(file.get_uri()[7:])
            filenames.append(filename)

        return filenames
