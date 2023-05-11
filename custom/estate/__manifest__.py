{
    'name': "Real Estate Advertisement",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_list_view.xml',
        'views/estate_form_view.xml',
        'views/estate_search_view.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml'
    ]
}