import json 

from rest_framework.renderers import JSONRenderer


class APIJSONRenderer(JSONRenderer):
    charset = 'utf-8'
    
    def render(self, data, media_type=None, renderer_context=None):
        
        response_status_code = renderer_context['response'].status_code
        
        response_data = {'status_code': response_status_code, "data": data}
        
        return super().render(response_data, media_type, renderer_context)