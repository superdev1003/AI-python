""""""
from os import getenv
from typing import Dict, List
import unittest

import datetime as dt

import shimoku_api_python as shimoku
from shimoku_api_python.exceptions import ApiClientError


api_key: str = getenv('API_TOKEN')
universe_id: str = getenv('UNIVERSE_ID')
business_id: str = getenv('BUSINESS_ID')
app_id: str = getenv('APP_ID')
report_id: str = getenv('REPORT_ID')
report_element: Dict[str, str] = dict(
    business_id=business_id,
    app_id=app_id,
    report_id=report_id
)


config = {
    'access_token': api_key,
}

s = shimoku.Client(
    config=config,
    universe_id=universe_id,
)


def test_get_report():
    report: Dict = s.report.get_report(**report_element)
    assert report


def test_update_report():
    """Set the updatedAt field of an report to '2000-01-01'
    Then revert the updatedAt to its original value
    """
    report: Dict = s.report.get_report(**report_element)
    old_val: str = report['reportType']

    val: str = 'BARCHART'
    assert old_val != val

    report_data: Dict = {'reportType': val}
    s.report.update_report(
        report_metadata=report_data,
        **report_element,
    )

    report_updated: Dict = s.report.get_report(**report_element)

    assert report_updated['reportType'] == val

    #########
    # Revert the change
    #########

    report_data: Dict = {'reportType': old_val}
    s.report.update_report(
        report_metadata=report_data,
        **report_element,
    )

    report_updated: Dict = s.report.get_report(**report_element)

    assert report_updated['reportType'] == old_val


def test_create_and_delete_report():
    report_metadata = {
        'title': 'test',
        'order': 0,
        'grid': '1, 1',
        'path': 'test',
        'reportType': 'LINECHART',
    }
    new_report: Dict = (
        s.report.create_report(
            business_id=business_id,
            app_id=app_id,
            report_metadata=report_metadata,
        )
    )
    new_report_id: str = new_report['id']

    report: Dict = s.report.get_report(
        business_id=business_id,
        app_id=app_id,
        report_id=new_report_id,
    )

    assert report == new_report

    s.report.delete_report(
        business_id=business_id,
        app_id=app_id,
        report_id=new_report_id,
    )

    # Check it does not exists anymore
    class MyTestCase(unittest.TestCase):
        def check_report_not_exists(self):
            with self.assertRaises(ApiClientError):
                s.report.get_report(
                    business_id=business_id,
                    app_id=app_id,
                    report_id=new_report_id,
                )

    t = MyTestCase()
    t.check_report_not_exists()


def test_get_report_data():
    data: List[Dict] = s.report.get_report_data(**report_element)
    assert data
    assert len(data[0]) > 0


def test_get_reports_in_same_app():
    reports: List[str] = s.report.get_reports_in_same_app(**report_element)
    assert reports
    assert len(reports) > 1


def test_get_reports_in_same_path():
    reports: List[str] = s.report.get_reports_in_same_path(**report_element)
    assert reports
    assert len(reports) > 1


def test_get_report_last_update():
    last_update: dt.datetime = s.report.get_report_last_update(**report_element)


def test_get_report_by_title():
    title: str = ''
    report: Dict = (
        s.report.get_report_by_title(
            business_id=business_id,
            app_id=app_id,
            title=title,
        )
    )
    assert report
    assert report['title'] == title


def test_get_report_by_path():
    path: str = ''  # TODO
    report: Dict = (
        s.report.get_report_by_path(
            business_id=business_id,
            app_id=app_id,
            path=path,
        )
    )
    assert report
    assert report['path'] == path


def test_get_report_by_external_id():
    external_id: str = ''  # TODO
    report: Dict = (
        s.report.get_report_by_external_id(
            business_id=business_id,
            app_id=app_id,
            external_id=external_id,
        )
    )
    assert report
    assert report['codeETLId'] == external_id


def test_get_report_by_chart_type():
    report_type: str = 'LINECHART'
    report: Dict = (
        s.report.get_report_by_chart_type(
            business_id=business_id,
            app_id=app_id,
            chart_type=chart_type,
        )
    )
    assert report
    assert report['reportType'] == report_type


def test_get_report_by_grid_position():
    row: int = 1
    column: int = 1
    report: Dict = (
        s.report.get_report_by_grid_position(
            business_id=business_id,
            app_id=app_id,
            row=row, column=column,
        )
    )
    assert report
    assert report['grid'] == f'{row}, {column}'


# TODO
def test_change_report_grid_position():
    s.report.change_report_grid_position()


def test_get_filter_report():
    # s.report.get_filter_report()
    raise NotImplementedError


def test_get_filter_reports():
    # s.report.get_filter_reports()
    raise NotImplementedError


def test_fetch_filter_report():
    # s.report.fetch_filter_report()
    raise NotImplementedError


def test_add_report_to_filter():
    # s.report.add_report_to_filter()
    raise NotImplementedError


def test_set_filter_to_reports():
    # s.report.set_filter_to_reports()
    raise NotImplementedError


def test_remove_filter_for_report():
    # s.report.remove_filter_for_report()
    raise NotImplementedError


test_get_report()
# test_update_report()
# test_create_and_delete_report()
# TODO pending have data:
#  test_get_report_data()
# TODO pending have path (fix by Guillermo)
#  test_get_reports_in_same_path()

test_get_report_by_title()
# TODO pending have path (fix by Guillermo)
#  test_get_report_by_path()
# test_get_report_by_external_id()
test_get_report_by_chart_type()
# TODO pending have grid (fix by Guillermo)
test_get_report_by_grid_position()
# TODO pending have grid (fix by Guillermo)
test_change_report_grid_position()

"""
test_get_filter_report()
test_get_filter_reports()
test_add_report_to_filter()
test_remove_filter_for_report()
test_set_filter_to_reports()
test_fetch_filter_report()
"""
