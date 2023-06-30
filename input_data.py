import argparse

from dateutil.parser import parse


def get_input_data():
    parser = argparse.ArgumentParser(description='Get data for report OZON')

    parser.add_argument('date_start', help='Date from which the report starts')
    parser.add_argument('date_finish', help='Date on which the report ends')
    parser.add_argument("-s", dest='status', default=None, help='Departure status')

    args = parser.parse_args()

    date_start = parse(args.date_start)
    date_finish = parse(args.date_finish)
    status = args.status

    print(f'Вывели дату начала отчета {date_start}')
    print(f'Вывели дату окончания отчета {date_finish}')
    print(f'Статус отправления {status}')

    return date_start, date_finish, status
