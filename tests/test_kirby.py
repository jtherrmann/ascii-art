import os
import subprocess
import unittest


class KirbyTestCase(unittest.TestCase):

    _tests_dir = 'tests'

    # https://en.wikipedia.org/w/index.php?curid=32125089
    _image_path = os.path.join(_tests_dir, 'kirby.png')

    _output_path = os.path.join(_tests_dir, 'test-kirby.txt')

    def setUp(self):
        assert not os.path.exists(self._output_path)

    def tearDown(self):
        assert os.path.exists(self._output_path)
        os.remove(self._output_path)
        assert not os.path.exists(self._output_path)

    def test_kirby(self):
        saved_output_path = os.path.join(self._tests_dir, 'kirby.txt')
        assert os.path.isfile(saved_output_path)

        subprocess.check_call(
            ('python3', 'ascii_art.py',
             self._image_path,
             '100',
             '-o', self._output_path,
             '-s', ' .,:;/@')
        )

        with open(self._output_path, 'rb') as output_file:
            output = output_file.read()

        with open(saved_output_path, 'rb') as saved_output_file:
            saved_output = saved_output_file.read()

        self.assertEqual(output, saved_output)
