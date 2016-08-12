from gi.repository import Nautilus, GObject

class TmsuTagsExtension(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider, Nautilus.MenuProvider):
    def __init__(self):
        pass

    def get_columns(self):
        return Nautilus.Column(name="NautilusPython::block_size_column",
                               attribute="block_size",
                               label="Block size",
                               description="Get the block size"),

    def update_file_info(self, file):
        if file.get_uri_scheme() != 'file':
            return

        filename = urllib.unquote(file.get_uri()[7:])

        file.add_string_attribute('block_size', str(os.stat(filename).st_blksize))

    def get_file_items(self, window, files):
        top_menuitem = Nautilus.MenuItem(name='ExampleMenuProvider::Foo',
                                         label='Foo',
                                         tip='',
                                         icon='')

        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        sub_menuitem = Nautilus.MenuItem(name='ExampleMenuProvider::Bar',
                                         label='Bar',
                                         tip='',
                                         icon='')
        submenu.append_item(sub_menuitem)

        return top_menuitem,

    def get_background_items(self, window, file):
        submenu = Nautilus.Menu()
        submenu.append_item(Nautilus.MenuItem(name='ExampleMenuProvider::Bar2',
                                         label='Bar2',
                                         tip='',
                                         icon=''))

        menuitem = Nautilus.MenuItem(name='ExampleMenuProvider::Foo2',
                                         label='Foo2',
                                         tip='',
                                         icon='')
        menuitem.set_submenu(submenu)

        return menuitem,