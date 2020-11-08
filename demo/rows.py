from seatable_api import SeaTableAPI

server_url = 'https://cloud.seatable.cn'
api_token = 'd00ad238bb6050b32aa8b2fa95e5f7b3ca79b1e6'


def filter_rows():
    seatable = SeaTableAPI(api_token, server_url)
    seatable.auth()

    table_name = '在职员工'

    filters = [
        {
            "column_name": "姓名",
            "filter_predicate": "contains",
            "filter_term": "王",
        },
        {
            "column_name": "姓名",
            "filter_predicate": "contains",
            "filter_term": "杨",
        }
    ]

    filtered_rows = seatable.filter_rows(table_name, filters=filters, filter_conjunction='Or')



def row_link():

    table_name = 'Table1'
    other_table_name = 'Table2'
    column_name = 'Foreign Key'

    seatable = SeaTableAPI(api_token, server_url)
    seatable.auth()

    # get column link id
    metadata = seatable.get_metadata()

    table = None
    for table_item in metadata['tables']:
        if table_item['name'] == table_name:
            table = table_item
            break

    column = None
    for column_item in table['columns']:
        if column_item['name'] == column_name:
            column = column_item
            break

    link_id = column['data']['link_id']

    # get row id
    rows = seatable.list_rows(table_name)
    other_rows = seatable.list_rows(other_table_name)
    row_id = rows[0]['_id']
    other_row_id = other_rows[0]['_id']

    # add link
    seatable.add_link(link_id, table_name, other_table_name,row_id, other_row_id)

    # remove link
    # seatable.remove_link(link_id, table_name, other_table_name, row_id, other_row_id)


if __name__ == '__main__':
    filter_rows()
    row_link()
