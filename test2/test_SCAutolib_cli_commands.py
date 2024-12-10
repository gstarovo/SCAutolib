import pytest
from os.path import join, dirname, abspath
from click.testing import CliRunner

from SCAutolib.cli_commands import cli, ReturnCode, prepare

try:
    import mock
except ImportError:
    import unittest.mock as mock

@pytest.fixture(scope="module")
def runner():
    return CliRunner()

@pytest.mark.parametrize("force", [None, "force", "f"])
@pytest.mark.parametrize("verbose", [None, "INFO", "ERROR"])
@mock.patch("SCAutolib.cli_commands.logger")
@mock.patch("SCAutolib.controller.Controller.prepare")
@mock.patch("SCAutolib.controller.Controller.__init__")
def test_command_line_main(mock_init, mock_prepare, mock_logger, runner,
        force, verbose):
    mock_init.return_value = None
    mock_logger.setLevel.return_value = None

    conf_file = join(dirname(abspath(__file__)), "files",
                        "dummy_config_file.json")
    args = ["-c", conf_file]

    if force:
        prefix = "-" if len(force) == 1 else "--"
        args.append(prefix + force)
    if verbose:
        args.extend(["-v", verbose])
    else:
        verbose = "DEBUG"

    args.append("prepare")

    result = runner.invoke(cli, args)

    assert result.exit_code == ReturnCode.SUCCESS.value
    mock_init.assert_called_once_with(conf_file)
    mock_prepare.assert_called_once_with(force != None, False,
        False, False)
    mock_logger.setLevel.assert_called_once_with(verbose)

@pytest.mark.parametrize("gdm", [None, "gdm", "g"])
@pytest.mark.parametrize("install_missing", [None, "install-missing", "i"])
@pytest.mark.parametrize("graphical", [None, "graphical"])
@mock.patch("SCAutolib.cli_commands.logger")
@mock.patch("SCAutolib.controller.Controller.prepare")
@mock.patch("SCAutolib.controller.Controller.__init__")
def test_command_line_prepare(mock_init, mock_prepare, mock_logger, runner,
        gdm, install_missing, graphical):
    mock_init.return_value = None
    mock_logger.setLevel.return_value = None

    conf_file = join(dirname(abspath(__file__)), "files",
                        "dummy_config_file.json")
    args = ["-c", conf_file, "prepare"]

    if gdm:
        prefix = "-" if len(gdm) == 1 else "--"
        args.append(prefix + gdm)
    if install_missing:
        prefix = "-" if len(install_missing) == 1 else "--"
        args.append(prefix + install_missing)
    if graphical:
        args.append("--" + graphical)

    result = runner.invoke(cli, args)

    assert result.exit_code == ReturnCode.SUCCESS.value
    mock_init.assert_called_once_with(conf_file)
    mock_prepare.assert_called_once_with(False, gdm != None,
        install_missing != None, graphical != None)

@pytest.mark.parametrize("ca_type", ["local"])
@mock.patch("SCAutolib.cli_commands.logger")
@mock.patch("SCAutolib.controller.Controller.setup_local_ca")
@mock.patch("SCAutolib.controller.Controller.prepare")
@mock.patch("SCAutolib.controller.Controller.__init__")
def test_command_setap_ca(mock_init,
                            mock_prepare,
                            mock_setup_local_ca,
                            mock_logger,
                            runner,
                            ca_type):
    mock_init.return_value = None
    mock_logger.setLevel.return_value = None

    conf_file = join(dirname(abspath(__file__)), "files",
                        "dummy_config_file.json")
    args = ["-c", conf_file]
    args.append("-f")
    args.append("setup-ca")
    args.extend(["-t", ca_type])
    result = runner.invoke(cli, args)

    print(result.output)

    assert result.exit_code == ReturnCode.SUCCESS.value
    mock_init.assert_called_once_with(conf_file)
    mock_setup_local_ca.assert_called_once_with(force=ca_type== "local")