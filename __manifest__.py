{
    'name': 'Stock Forecast',
    'version': '1.0',
    'summary': 'Módulo para predecir el agotamiento de stock',
    'description': 'Muestra una tabla con los productos en stock, incluyendo el promedio de venta mensual y el mes aproximado de agotamiento.',
    'author': 'Tu Nombre',
    'depends': ['stock'],
    'data': [
        'views/stock_forecast_views.xml',
    ],
    'installable': True,
    'application': True,
}