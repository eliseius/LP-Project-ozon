from collections import Counter

from constants import COUNTRIES_SHIPMENT


def filter_by_shipment_countries(short_report):
    report_with_filter_city = []
    for item_sold in short_report:
        for one_cou in COUNTRIES_SHIPMENT:
            cluster = set(item_sold['cluster_delivery'].split())
            if cluster & COUNTRIES_SHIPMENT[one_cou]:
                item_sold['cluster_delivery'] = one_cou
                report_with_filter_city.append(item_sold)

    numb_shipment_countries = get_numb_shipment_in_countries(report_with_filter_city)
    sorted_report = get_sorted_report(report_with_filter_city, numb_shipment_countries)

    return sorted_report, numb_shipment_countries


def get_numb_shipment_in_countries(report):
    clusters_delivery = []
    for posit in report:
        clusters_delivery.append(posit['cluster_delivery'])
    numb_shipment_countries = Counter(clusters_delivery).most_common()
    return numb_shipment_countries


def get_sorted_report(report, numb_shipment_countries):
    sorted_report = []
    for one_country in numb_shipment_countries:
        for item in report:
            if one_country[0] in item['cluster_delivery']:
                sorted_report.append(item)
    return sorted_report
