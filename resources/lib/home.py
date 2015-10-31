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
        utils.add_directory(control.lang(30401), utils.icon_all, None,
                            "%s?action=list-all" % (sys.argv[0]))
        # Live
        utils.add_directory(control.lang(30407), utils.icon_event, None,
                            "%s?action=browse-live" % (sys.argv[0]))
        # Events
        utils.add_directory(control.lang(30405), utils.icon_event, None,
                            "%s?action=browse-events" % (sys.argv[0]))
        # Shows
        utils.add_directory(control.lang(30403), utils.icon_tv, None,
                            "%s?action=browse-shows" % (sys.argv[0]))
        # Series
        utils.add_directory(control.lang(30404), utils.icon_tv, None,
                            "%s?action=browse-series" % (sys.argv[0]))
        # Tags
        utils.add_directory(control.lang(30402), utils.icon_tag, None,
                            "%s?action=browse-tags" % (sys.argv[0]))
        # Blogs
        utils.add_directory(control.lang(30406), utils.icon_blog, None,
                            "%s?action=browse-blogs" % (sys.argv[0]))
        # Authors
        utils.add_directory(control.lang(30408), utils.icon_user, None,
                            "%s?action=browse-authors" % (sys.argv[0]))
        # Search
        utils.add_directory(control.lang(30409), utils.icon_search, None,
                            "%s?action=search" % (sys.argv[0]))
        # Search
        utils.add_directory("[B][COLOR green]%s[/COLOR][/B]" % control.lang(30410), utils.icon_cog, None,
                            "%s?action=settings" % (sys.argv[0]))

        control.directory_end()
        return
