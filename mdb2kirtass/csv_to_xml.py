from lxml import etree
import csv

class CsvtoXml(object):
    """Class untuk mengubah file csv ke file xml
    berdasarkan nama kolom....


    csv_file : file csv, atau yang semisal dengan file (dengan StringIO)?
    """

    def __init__(self, csv_file):
        self.csv_file = csv_file


    def _dict_csv(self):
        """Fungsi untuk mengubah file csv ke objek DictCsvReader"""
        return csv.DictReader(self.csv_file)

    def _make_xml(self, root='item', parent=None, col_name=None, include=None,
                            as_attrib=False, tag=None):
        item = etree.Element(root)
        for row in self._dict_csv():
            if include:
                row = self._process_include(row, include)
            if tag is None:
                if parent is None:
                    if col_name is None:
                        self._make_tag_with_parent_from_row(row, item)
                    else:
                        self._make_tag_and_rename_it_inside_parent_from_row(row,
                                                                     item, col_name)
                else:
                    p = etree.SubElement(item, parent)
                    if col_name is None:
                        self._make_tag_with_parent_from_row(row, p)
                    else:
                        self._make_tag_and_rename_it_inside_parent_from_row(row,
                                                        p, col_name)
            else:
                if col_name is None:
                    attrib = {k:row[k] for k in row}
                    etree.SubElement(item, tag, attrib)
                else:
                    self._change_col_name(row, col_name)
                    attrib = {k:row[k] for k in row}
                    etree.SubElement(item, tag, attrib)

        return item

    def _make_tag_with_parent_from_row(self, row, parent, as_attrib=False):
        """Membuat tag, didalam parent yang ditentukan oleh *parent*
        dari *row* csv, DictReader objek"""
        for col in row:
            t = etree.SubElement(parent, col)
            t.text = row[col]

    def _make_tag_and_rename_it_inside_parent_from_row(self, row,
                                                       parent, col_name):
        """membuat tag, dengan nama yang diubah, didalam row objek DictReader,
        col_name adalah list/tuple di dalam list/atau tuple, index 0 adalah
        asli, index 1 adalah setelah diubah"""
        self._change_col_name(row, col_name)

        for col in row:
            t = etree.SubElement(parent, col)
            t.text = row[col]

    def _change_col_name(self, row, col_name):
        """http://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary"""

        for c in col_name:
            row[c[1]] = row.pop(c[0])

    def _process_include(self, row, include):
        return {key:row[key] for key in row if key in include}
