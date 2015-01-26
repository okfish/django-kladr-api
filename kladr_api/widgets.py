import json
from django import forms
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from .settings import KLADR_API_URL, KLADR_API_TOKEN

class KladrWidget(forms.TextInput):
    """
    Base class for kladr widgets
    
    Subclass and define widget_type. It can be ('city', 'region', 'zip' etc)
    see https://kladr-api.ru/integration/
    """
    # subclasses should override this
    widget_type = None 
    options = {
        'url' : KLADR_API_URL,
        'token' : KLADR_API_TOKEN,
    }
 
    def start_jscript(self, id=None):
        jscode = """<script type="text/javascript">
                        $(document).ready(function() {\n""" 
        if id:
            jscode += """$inp = $(document.getElementById('%(id)s'));
                        $parent = $inp.parents("form");\n""" % { 'id' : id }
        return jscode
    
    def close_jscript(self):
        return "});\n</script>"

    def render_jscript(self, id=None, inner_js=None):
        return self.start_jscript(id) + inner_js + self.close_jscript()
    
    
    def get_options(self):
        """
        Subclass to add/modify options or drop unneccessary.
        
        :return: Dictionary of options to be passed to $('input').kladr plugin
        :rtype: :py:obj:`dict`
        """
        options = dict(self.options)
        if self.widget_type:
            options['type'] = self.widget_type
        return options
                   
    def render(self, name, value, attrs=None):
         
        jscode = ''
        options = self.get_options()
        attrs = self.build_attrs(attrs)
        s = unicode(super(KladrWidget, self).render(name, value, attrs))
        
        if not self.widget_type:
            return s
        
        id_ = attrs.get('id', None)
        
        jscode += "$inp.kladr({ parentInput : $parent });\n" 
        jscode += "$inp.kladr(" + json.dumps(options) + ");\n" 
        jscode = self.render_jscript(id_, jscode)
             
        s += jscode
        return mark_safe(s)

    class Media:
        js = ('kladr_api/js/jquery.kladr.min.js', 
              )
        css = {
               'all': ('kladr_api/css/jquery.kladr.min.css',
                       )
               }
        
class KladrRegionWidget(KladrWidget):
    """
    Russian region select input.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    """
    widget_type = 'region'

class KladrCityWidget(KladrWidget):
    """
    Russian city select input.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    """
    widget_type = 'city'

class KladrStreetWidget(KladrWidget):
    """
    Russian streets select input.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    """
    widget_type = 'street'

class KladrBuildingWidget(KladrWidget):
    """
    Russian streets select input.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    """
    widget_type = 'building'
    
    def get_options(self):
        options = super(KladrBuildingWidget, self).get_options()
        options['verify'] = False
        return options
    
class KladrPostcodeWidget(KladrWidget):
    """
    Russian postcode select input. On change event will try to
    get remaining fields such as region,city,street corresponding to
    entered postcode. 
    
    FIX: There are some issues, works strange.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    
    """
    widget_type = 'zip'
    
    def render(self, name, value, attrs=None):
         
        attrs = self.build_attrs(attrs)
        attrs['autocomplete'] = 'off'
        s = unicode(super(KladrWidget, self).render(name, value, attrs))
        
        id_ = attrs.get('id', None)
        s += self.render_jscript(id_, "$inp.kladrZip($parent);")

        return mark_safe(s)    