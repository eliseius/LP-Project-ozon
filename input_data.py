import argparse

from dateutil.parser import parse

from output import get_color_message


def get_input_data():
    parser = argparse.ArgumentParser(description='Get data for report OZON')

    parser.add_argument('date_start', help='Date from which the report starts, format: day/month/year')
    parser.add_argument('date_finish', help='Date on which the report ends, format: day/month/year')
    parser.add_argument("-s", dest='status', default=None, help='Departure status, format: -s [your status] ')

    args = parser.parse_args()

    date_start = parse(args.date_start, dayfirst=True)
    date_finish = parse(args.date_finish, dayfirst=True)
    status = args.status

    if date_start >= date_finish:
        get_color_message(('Некорректные даты. Дата начала отчета должна быть раньше даты окончания.'), 'error')
        get_color_message((f'Дата начала отчета: {date_start}'), 'info')
        get_color_message((f'Дата окончания отчета: {date_finish}'), 'info')
        get_color_message((f'Статус отправления: {status}'), 'info')
        return None
    else:
        return date_start, date_finish, status
