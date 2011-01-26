# __init__.py: list box widget module initialization
# $Id: __init__.py,v 1.8 2007/03/27 07:01:58 agriggio Exp $
#
# Copyright (c) 2002-2007 Alberto Griggio <agriggio@users.sourceforge.net>
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY

def initialize():
    import common
    import codegen
    codegen.initialize()
    if common.use_gui:
        import list_box
        return list_box.initialize()
