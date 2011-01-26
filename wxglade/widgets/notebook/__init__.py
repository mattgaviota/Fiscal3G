# __init__.py: notebook widget module initialization
# $Id: __init__.py,v 1.8 2007/03/27 07:01:56 agriggio Exp $
#
# Copyright (c) 2002-2007 Alberto Griggio <agriggio@users.sourceforge.net>
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY

def initialize():
    import common
    import codegen
    codegen.initialize()
    if common.use_gui:
        import notebook
        return notebook.initialize()
