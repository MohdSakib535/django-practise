from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # Check if there are errors (DRF typically includes an 'errors' key in the response)
        if 'errors' in data:
            response = {
                'status': 'error',
                'errors': data['errors'],
                'message': data.get('detail', 'Validation failed'),
            }
        else:
            response = {
                'status': 'success',
                'data': data,
            }

        # Return the custom response structure
        return super(CustomJSONRenderer, self).render(response, accepted_media_type, renderer_context)
