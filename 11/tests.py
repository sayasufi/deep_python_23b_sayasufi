import json
import unittest

import cjson
import ujson


class TestCJSON(unittest.TestCase):
    def test_loads(self):
        json_strs = (
            '{"":""}',
            '{"": ""}',
            '{"" : ""}',
            '{"hello": 10, "world": "value"}',
            '{"board": 123444, "width": 120}',
        )
        for json_str in json_strs:
            self.assertEqual(
                cjson.loads(json_str),
                ujson.loads(json_str),
                json.loads(json_str),
            )

    def test_error_loads(self):
        bad_json_strs = (
            '{"":""',
            '"": ""}',
            '{1234 : ""}',
            '{"hello": 10    "world": "value"}',
            '{"board": 123444, "width" 120}',
        )
        for json_str in bad_json_strs:
            with self.assertRaises(expected_exception=ValueError):
                cjson.loads(json_str)

        other_types = (12, [], {})

        for i in other_types:
            with self.assertRaises(expected_exception=TypeError):
                cjson.loads(i)

    def test_dumps(self):
        dicts = (
            {"": ""},
            {"hello": 10, "world": "value"},
            {"hello": "10", "world": "value"},
            {"board": 123444, "width": 120},
            {"board": 123444, "width": "120"},
        )

        for d in dicts:
            self.assertEqual(ujson.dumps(d), cjson.dumps(d))

    def test_bad_dicts(self):
        bad_dicts = (
            {"": []},
            {10: 10, "world": "value"},
            {(): "10", "world": "value"},
        )

        for d in bad_dicts:
            with self.assertRaises(expected_exception=TypeError):
                cjson.dumps(d)

    def test_dict_to_dict_via_str(self):
        dicts = (
            {"": ""},
            {"hello": 10, "world": "value"},
            {"hello": "10", "world": "value"},
            {"board": 123444, "width": 120},
            {"board": 123444, "width": "120"},
        )

        for d in dicts:
            self.assertEqual(cjson.loads(cjson.dumps(d)), d)

    def test_str_to_str_via_dict(self):
        json_strs = (
            '{"":""}',
            '{"hello":10,"world":"value"}',
            '{"board":123444,"width":120}',
        )
        for json_str in json_strs:
            self.assertEqual(cjson.dumps(cjson.loads(json_str)), json_str)


if __name__ == "__main__":
    unittest.main()
