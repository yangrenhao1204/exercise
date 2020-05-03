import xlrd


class XLS():
    @classmethod
    def add_record(cls, file):
        f = file.read()  # 文件内容
        data = xlrd.open_workbook(file_contents=f)
        table = data.sheets()[0]
        # names = data.sheet_names()  # 返回book中所有工作表的名字
        # status = data.sheet_loaded(names[0])  # 检查sheet1是否导入完毕
        rows = table.nrows  # 获取该sheet中的有效行数
        cols = table.ncols  # 获取该sheet中的有效列数
        result = []
        for i in range(rows):
            row_list = []
            for j in range(cols):
                row_list.append(table.cell_value(i, j))
            result.append(row_list)
        del result[0]  # 删掉第一行，第一行获取的是文件的头，一般不用插到数据库里面
        return result
