#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


from setuptools import find_packages, setup

setup(
    name="source_http_request",
    description="source_http_request.",
    author="Airbyte",
    author_email="contact@airbyte.io",
    packages=find_packages(),
    package_data={"": ["*.json", "*.yaml", "schemas/*.json"]},
    install_requires=["airbyte-cdk~=0.1", "pendulum>=2,<3", "genson==0.1.0"],
)
