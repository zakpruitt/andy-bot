import gspread
import gspread_dataframe as gs_df


class GoogleSheetsUtility:

    def __init__(self, spreadsheet_name: str):
        self.gc = gspread.service_account(filename='resources/creds.json')
        self.spreadsheet = self.gc.open(spreadsheet_name)
        for worksheet in self.spreadsheet.worksheets():
            setattr(self, worksheet.title, worksheet)

    def get_worksheet(self, name):
        return self.spreadsheet.worksheet(name)

    def write_data_to_worksheet(self, worksheet_name, data, row=1, col=1, include_index=False,
                                include_column_header=False, resize=True):
        try:
            gs_df.set_with_dataframe(worksheet=self.get_worksheet(worksheet_name),
                                     dataframe=data,
                                     row=row,
                                     col=col,
                                     include_index=include_index,
                                     include_column_header=include_column_header,
                                     resize=resize)
        except Exception as e:
            print(e)

    @staticmethod
    def get_as_df(worksheet):
        return gs_df.get_as_dataframe(worksheet=worksheet)
