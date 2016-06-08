import json
from django import forms
from django.utils.safestring import mark_safe

from .settings import KLADR_API_URL, KLADR_API_TOKEN


class KladrWidget(forms.TextInput):
    """
    Base class for kladr widgets
    
    Subclass and define widget_type. It can be ('city', 'region', 'zip' etc)
    see https://kladr-api.ru/integration/
    """
    # subclasses should override this props
    jscode = ''
    widget_type = None 
    options = {
        'url': KLADR_API_URL,
        'token': KLADR_API_TOKEN,
    }
 
    def start_jscript(self, id=None):
        jscode = """<script type="text/javascript">
                        $(document).ready(function() {\n""" 
        return jscode
    
    def close_jscript(self):
        return "});\n</script>"

    def render_jscript(self, id=None, inner_js=None):
        return self.start_jscript(id) + inner_js + self.close_jscript()
    
    def get_options(self):
        """
        Subclass to add/modify options or drop unnecessary.
        :return: Dictionary of options to be passed to $('input').kladr plugin
        :rtype: :py:obj:`dict`
        """
        options = {}
        options.update(self.options)
        if self.widget_type:
            options['type'] = self.widget_type
        return options
                   
    def render(self, name, value, attrs=None):
         
        jscode = self.jscode
        options = self.get_options()
        attrs = self.build_attrs(attrs)
        attrs['autocomplete'] = 'off'
        attrs['data-kladr-type'] = self.widget_type
        
        if self.widget_type:
            id_ = attrs.get('id', None)
            parent_id_ = attrs.get('parent_id', None)
            
            if parent_id_:
                options['parentId'] = parent_id_
                if self.widget_type == 'street':
                    options['parentType'] = 'city'
                elif self.widget_type == 'city':
                    options['verify'] = True
                    options.pop('parentId')
                elif self.widget_type == 'building':
                    options['parentType'] = 'street'    
 
            attrs['data-kladr-options'] = json.dumps(options)
            if jscode:
                jscode = self.render_jscript(id_, jscode) 
        
        s = unicode(super(KladrWidget, self).render(name, value, attrs))
        s += jscode
        return mark_safe(s)

    class Media:
        js = ('kladr_api/js/core.js',  # switched to dev-branch
              'kladr_api/js/kladr.js',
              'kladr_api/js/common.js',
              )
        css = {
               'all': ('kladr_api/css/jquery.kladr.min.css',
                       'kladr_api/css/kladr_api.css',
                       )
               }


class KladrRegionWidget(KladrWidget):
    """
    Russian region select input.
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    """
    widget_type = 'region'

    def render(self, name, value, attrs=None):
         
        attrs = self.build_attrs(attrs)
        attrs['disabled'] = 'true'
        s = unicode(super(KladrRegionWidget, self).render(name, value, attrs))
        return mark_safe(s)
    
    def get_options(self):
        options = super(KladrRegionWidget, self).get_options()
        options['verify'] = True
        return options


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
    
    FIXME: There are some issues, works strange. Temporarily original plugin
    is switched off due to useless...
    
    
    Uses Kladr-api.ru JQuery plugin for suggestions.
    
    """
    widget_type = 'zip'
    
    def get_options(self):
        options = super(KladrPostcodeWidget, self).get_options()
        options['verify'] = False
        return options
#     
#     def render(self, name, value, attrs=None):
#          
#         attrs = self.build_attrs(attrs)
#         attrs['autocomplete'] = 'off'
#         
#         s = unicode(super(KladrWidget, self).render(name, value, attrs))
#         
#         id_ = attrs.get('id', None)
#         #s += self.render_jscript(id_, "$inp.kladrZip($parent);")
# 
#         return mark_safe(s)    