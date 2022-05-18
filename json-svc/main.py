#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_http_request import SourceHttpRequest

if __name__ == "__main__":
    source = SourceHttpRequest()
    launch(source, sys.argv[1:])
