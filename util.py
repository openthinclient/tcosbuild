import subprocess
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def shell(command, **kwargs):
    logger.debug(f'running command: {command}')
    res = subprocess.run(command,
                          shell=True,
                          capture_output=True,
                          text=True,
                          **kwargs)
    return res.stdout.strip()


