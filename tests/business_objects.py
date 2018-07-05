from models.organization import OrganizationModel

Organization = {
    'name': 'Organization',
    'model': OrganizationModel,
    'endpoints': {
        'record': '/organization',
        'activate': None,
        'list': None
    },
    'objects': {
        'get': {
            'organization_name': 'test_o',
            'is_active': True
        },
        'post': {
            'organization_name': 'test_o',
            'is_active': True
        },
        'put': {
            'organization_name': 'new_test_o',
            'is_active': False
        },
        'delete': {
            'organization_name': 'test_o',
            'is_active': True
        }
    },
    'tests': {
        'system': {
            'record': {
                'get': [],
                'post': [
                    'test_post_with_authentication',
                    'test_post_without_authentication',
                    'test_post_not_unique'
                ],
                'put': [],
                'delete': []
            },
            'activate': None,
            'list': None
        }
    }
}
