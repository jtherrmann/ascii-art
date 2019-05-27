import os
import subprocess
import unittest


class KirbyTestCase(unittest.TestCase):

    _tests_dir = 'tests'

    # https://en.wikipedia.org/w/index.php?curid=32125089
    _image_path = os.path.join(_tests_dir, 'kirby.png')

    _output_path = os.path.join(_tests_dir, 'test-kirby.txt')
    _metadata_path = os.path.join(_tests_dir, 'test-kirby.metadata')

    def setUp(self):
        assert not os.path.exists(self._output_path)
        assert not os.path.exists(self._metadata_path)

    def tearDown(self):
        assert os.path.isfile(self._output_path)
        assert os.path.isfile(self._metadata_path)

        os.remove(self._output_path)
        assert not os.path.exists(self._output_path)

        os.remove(self._metadata_path)
        assert not os.path.exists(self._metadata_path)

    def test_kirby(self):
        saved_output_path = os.path.join(self._tests_dir, 'kirby.txt')
        assert os.path.isfile(saved_output_path)

        saved_metadata_path = os.path.join(self._tests_dir, 'kirby.metadata')
        assert os.path.isfile(saved_metadata_path)

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

        with open(self._metadata_path, 'rb') as metadata_file:
            metadata = metadata_file.read()

        with open(saved_metadata_path, 'rb') as saved_metadata_file:
            saved_metadata = saved_metadata_file.read()

        self.assertEqual(metadata, saved_metadata)

    def test_minimal_kirby(self):
        saved_output_path = os.path.join(self._tests_dir, 'minimal-kirby.txt')
        assert os.path.isfile(saved_output_path)

        saved_metadata_path = os.path.join(
            self._tests_dir, 'minimal-kirby.metadata'
        )
        assert os.path.isfile(saved_metadata_path)

        subprocess.check_call(
            ('python3', 'ascii_art.py',
             self._image_path,
             '50',
             '-o', self._output_path,
             '-s', ' .')
        )

        with open(self._output_path, 'rb') as output_file:
            output = output_file.read()

        with open(saved_output_path, 'rb') as saved_output_file:
            saved_output = saved_output_file.read()

        self.assertEqual(output, saved_output)

        with open(self._metadata_path, 'rb') as metadata_file:
            metadata = metadata_file.read()

        with open(saved_metadata_path, 'rb') as saved_metadata_file:
            saved_metadata = saved_metadata_file.read()

        self.assertEqual(metadata, saved_metadata)
