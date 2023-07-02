from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.text import Text

from constants import CITIES_FROM_BE


def create_table(report):
    table = Table(title="Data sell OZON", title_style="#00ab98", expand=True, show_lines=True, style="#f6c42d")

    table.add_column("posting_number", justify="center", overflow='fold', max_width=7)
    table.add_column("shipment_date", justify="center", overflow='fold', max_width=10)
    table.add_column("price", justify="center", max_width=6)
    table.add_column("name", justify="left",  overflow='fold', min_width=15)
    table.add_column("quantity", overflow='fold', justify="center", max_width=7)   
    table.add_column("cluster_delivery",  overflow='fold', justify="left", max_width=10)

    if report is not None:
        for item in report:
            item['shipment_date'] = item.get('shipment_date')[:10]
            item['price'] = '%.1f' % float(item.get('price'))
            text = Text(item['cluster_delivery'])

            if CITIES_FROM_BE & set(item['cluster_delivery'].split()):
                text.stylize("#41a02c")
            else:
                text.stylize("#009ce9")

            table.add_row(item['posting_number'], item['shipment_date'], item['price'],
                          item['name'], str(item['quantity']), text)

        console = Console()
        console.print(table)


def get_color_message(message, tag):
    custom_theme = Theme({
        'info': 'yellow',
        'error': 'red'
    })

    console = Console(theme=custom_theme)
    console.print(message, style=tag)