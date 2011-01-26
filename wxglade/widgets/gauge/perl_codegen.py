# perl_codegen.py : perl generator functions for wxGauge objects
# $Id: perl_codegen.py,v 1.4 2005/08/15 07:38:14 crazyinsomniac Exp $
#
# Copyright (c) 2002-2004 D.H. aka crazyinsomniac on sourceforge.net
# License: MIT (see license.txt)
# THIS PROGRAM COMES WITH NO WARRANTY

import common

class PerlCodeGenerator:
    def get_code(self, obj):
        init = []

        plgen = common.code_writers['perl']
        prop = obj.properties
        id_name, id = plgen.generate_code_id(obj)
        g_range = prop.get('range', '10')

        if not obj.parent.is_toplevel:
            parent = '$self->{%s}' % obj.parent.name
        else:
            parent = '$self'

        style = prop.get("style")
        if not style : style = ''

        if id_name: init.append(id_name)

        klass = obj.base;
        if klass != obj.klass : klass = obj.klass; 
        else: klass = klass.replace('wx','Wx::',1);

        init.append('$self->{%s} = %s->new(%s, %s, %s, wxDefaultPosition, \
    wxDefaultSize, %s);\n' %
                    (obj.name, klass, parent, id, g_range, style))
        props_buf = plgen.generate_common_properties(obj)

        return init, props_buf, []

# end of class PerlCodeGenerator

def initialize():
    common.class_names['EditGauge'] = 'wxGauge'

    plgen = common.code_writers.get('perl')
    if plgen:
        plgen.add_widget_handler('wxGauge', PerlCodeGenerator())

