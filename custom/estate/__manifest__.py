{
    'name': "Real Estate Advertisement",
    'depends': ['base'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_list_view.xml',
        'views/estate_search_view.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_menus.xml',
        'views/estate_offer_list_view.xml',
        'views/estate_offer_form_view.xml',
        'views/estate_form_view.xml',
    ]
}