from setuptools import setup, find_packages

import versioneer

setup(
    name="q2-pepsirf",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    package_data={},
    author="Annabelle Brown",
    author_email="annabelle811@live.com",
    description="Qiime2 Wrapper for pepsirf",
    license="Apache-2.0",
    url="https://github.com/LadnerLab/q2-pepsirf",
    entry_points={
        "qiime2.plugins": ["q2-pepsirf=q2_pepsirf.plugin_setup:plugin"]
    },
    zip_safe=False,
)
