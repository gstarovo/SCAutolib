import logging
from fixtures import *  # noqa: F401

LOGGER = logging.getLogger("pytest-custom")

def pytest_addoption(parser):
    """
    Define CLI parameters. Parameters for IPA would be serialised to ipa_config
    fixture.
    """
    # parser.addoption(
    #     "--ipa-ip", action="store", help="IP address of IPA server",
    #     default=environ["IPA_IP"]
    # )
    pass


def pytest_generate_tests(metafunc):
    """
    Inject variables to test. Variables should be specified in test arguments
    """
    # ipa_ip = metafunc.config.option.ipa_ip
    # if 'ipa_ip' in metafunc.fixturenames and ipa_ip is not None:
    #     metafunc.parametrize("ipa_ip", [ipa_ip], scope="session")
    pass


def pytest_sessionstart(session):
    pass


def pytest_sessionfinish(session, exitstatus):
    """
    Change behaviour: if no tests found (exit status == 5), for us, it is not a
    fail.
    """
    pass
