from rich.console import Console
from rich.table import Table


def create_teable(report):
    table = Table(title="Data sell OZON")

    table.add_column("posting_number", justify='right')
    table.add_column("shipment_date", justify='center')
    table.add_column("price", justify='center')
    table.add_column("name", justify='center')
    table.add_column("quantity", justify='center')   
    table.add_column("cluster_delivery", justify='left')

    for item in report:
        table.add_row(item['posting_number'], item['shipment_date'], item['price'],
                      item['name'], str(item['quantity']), item['cluster_delivery'])

    console = Console()
    console.print(table)
