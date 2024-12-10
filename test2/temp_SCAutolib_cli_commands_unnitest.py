import unittest
from os.path import join, dirname, abspath
from click.testing import CliRunner

try:
    import mock
except ImportError:
    import unittest.mock as mock

failed_import = False
try:
    from SCAutolib.cli_commands import cli
except ImportError:
    failed_import = True

@pytest.fixture(scope="module", autouse=True)
def runner():
    return CliRunner()

@unittest.skipIf(failed_import,
                 "Could not import SCAutolib. Skipping related tests.")
class TestCommandLine(unittest.TestCase):
    @mock.patch("SCAutolib.cli_commands.logger")
    @mock.patch("SCAutolib.controller.Controller.prepare")
    @mock.patch("SCAutolib.controller.Controller.__init__")
    def test_command_line_prepare(self, mock_init, mock_prepare, mock_logger):
        runner = CliRunner()
        mock_init.return_value = None
        mock_logger.setLevel.return_value = None

        conf_file = join(dirname(abspath(__file__)), "files",
                         "dummy_config_file.json")
        args = ['-c', conf_file, 'prepare']
        result = runner.invoke(cli, args)

        self.assertEqual(result.exit_code, 0)
        mock_init.assert_called_once_with(conf_file)
        mock_prepare.assert_called_once_with(False, False, False, False)
        mock_logger.setLevel.assert_called_once_with("DEBUG")

    @mock.patch("SCAutolib.cli_commands.logger")
    @mock.patch("SCAutolib.controller.Controller.prepare")
    @mock.patch("SCAutolib.controller.Controller.__init__")
    def test_command_line_prepare_force(self, mock_init, mock_prepare,
            mock_logger):
        runner = CliRunner()
        mock_init.return_value = None
        mock_logger.setLevel.return_value = None

        conf_file = join(dirname(abspath(__file__)), "files",
                         "dummy_config_file.json")
        args = ['-c', conf_file, '-f' 'prepare']
        result = runner.invoke(cli, args)

        self.assertEqual(result.exit_code, 0)
        mock_init.assert_called_once_with(conf_file)
        mock_prepare.assert_called_once_with(False, False, False, False)
        mock_logger.setLevel.assert_called_once_with("DEBUG")