#
# Imports
#
import os
import sys
import control
import utils


#
# Main class
#
class Main:
    def __init__(self):
        utils.set_no_sort()

        # All
        utils.add_directory(control.lang(30401), "%s/all.png" % control.imagesPath, None,
                            "%s?action=list-all" % (sys.argv[0]))
        # Live
        utils.add_directory(control.lang(30407), "%s/event.png" % control.imagesPath, None,
                            "%s?action=browse-live" % (sys.argv[0]))
        # Events
        utils.add_directory(control.lang(30405), "%s/event.png" % control.imagesPath, None,
                            "%s?action=browse-event" % (sys.argv[0]))
        # Shows
        utils.add_directory(control.lang(30403), "%s/tv.png" % control.imagesPath, None,
                            "%s?action=browse-shows" % (sys.argv[0]))
        # Series
        utils.add_directory(control.lang(30404), "%s/tv.png" % control.imagesPath, None,
                            "%s?action=browse-series" % (sys.argv[0]))
        # Tags
        utils.add_directory(control.lang(30402), "%s/tag.png" % control.imagesPath, None,
                            "%s?action=browse-tags" % (sys.argv[0]))
        # Blogs
        utils.add_directory(control.lang(30406), "%s/blog.png" % control.imagesPath, None,
                            "%s?action=browse-blogs" % (sys.argv[0]))
        # Authors
        utils.add_directory(control.lang(30408), "%s/user.png" % control.imagesPath, None,
                            "%s?action=browse-authors" % (sys.argv[0]))
        # Search
        utils.add_directory(control.lang(30409), "%s/search.png" % control.imagesPath, None,
                            "%s?action=search" % (sys.argv[0]))

        control.directory_end()
