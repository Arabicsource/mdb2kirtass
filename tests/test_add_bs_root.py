import unittest
from lxml import etree
from io import StringIO

from mdb2kirtass.add_root import add_root

class AddRootBsTestCase(unittest.TestCase):

    def original_group_string (self):
        return """
        <setting>
            <root Name='abc' id='1'>
                <Item Name='def' id='1'>
                    <bk />
                </Item>
            </root>
        </setting>
        """.strip()



    def test_add_root(self):
        changed = add_root(StringIO(self.original_group_string()), 'new')
        self.assertIn(b'new', etree.tostring(changed))
        self.assertIn(b'0', etree.tostring(changed))

    def test_add_root_twice(self):
        changed = add_root(StringIO(self.original_group_string()), 'abc')

        self.assertIn(b'abc', etree.tostring(changed))
        self.assertIn(b'2', etree.tostring(changed))

    def test_add_root_with_prefix_id(self):
        changed = add_root(StringIO(self.original_group_string()),
                  'abc', 'bs')
        self.assertIn(b'abc', etree.tostring(changed))
        self.assertIn(b'bs2', etree.tostring(changed))





if __name__ == '__main__':
    unittest.main()