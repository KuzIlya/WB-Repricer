from typing import Any, Generator

from openpyxl import load_workbook


def get_articles_and_prices(excel_path: str) -> Generator[tuple[int, int], Any, Any]:

    wb = load_workbook(excel_path)
    if not (sheet := wb.active):
        return
    
    for row in sheet.iter_rows(min_row=1, values_only=True):
        if not row[0] or not row[1]:
            continue
        yield int(row[0]), int(row[1])


def get_skus(excel_path: str) -> Generator[str, None, None]:

    wb = load_workbook(excel_path)
    if not (sheet := wb.active):
        return
    
    for row in sheet.iter_rows(min_row=1, values_only=True):
        if row[0]:
            yield str(row[0])

