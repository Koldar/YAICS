from setuptools import setup, find_packages

setup(
    name="YAICS",
    version="0.1",
    packages=find_packages(),
    scripts = [
        'yaics/yaics_client.py',
        'yaics/yaics_server.py',
    ]
)
