#
# Copyright (c) 2021 Airbyte, Inc., all rights reserved.
#


from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import pendulum
import requests
from airbyte_cdk import AirbyteLogger
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from pendulum import DateTime
import genson

class HttpRequest(HttpStream):

    date_field_name = "date"

    # HttpStream related fields
    cursor_field = date_field_name
    primary_key = ""

    def __init__(self, baseUrl: str, conf: Mapping[str, Any]):
        super().__init__()
        self._url_base = baseUrl
        print(f"BASE URL : {baseUrl}")
        if "start_date" in conf:
            self._start_date = conf["start_date"]
        else:
            self._start_date = None
        if("access_key" in conf):
            self.access_key = conf["access_key"]
        else:
            self.access_key = None
        
    @property
    def url_base(self) -> str:
        print(f"returning base url {self._url_base}")
        return self._url_base

    def path(
        self, stream_state: Mapping[str, Any] = None, stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> str:
        return ""

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        return None

    def request_params(self, **kwargs) -> MutableMapping[str, Any]:
        params = {}
        print("Getting params")
        if self.access_key is not None:
            params["access_key"] = self.access_key

        return params

    def get_json_schema(self) -> Mapping[str, Any]:
        """
        :return: A dict of the JSON schema representing this stream.

        The default implementation of this method looks for a JSONSchema file with the same name as this stream's "name" property.
        Override as needed.
        """
        # TODO show an example of using pydantic to define the JSON schema, or reading an OpenAPI spec
        resp =  requests.get(self.url_base)
        jsonBody = resp.json()
        s = genson.Schema()
        s.add_object(jsonBody)
        return s.to_dict()

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        response_json = response.json()
        yield response_json

    #def stream_slices(self, stream_state: Mapping[str, Any] = None, **kwargs) -> Iterable[Optional[Mapping[str, Any]]]:
    #     stream_state = stream_state or {}
    #     start_date = pendulum.parse(stream_state.get(self.date_field_name, self._start_date))
    #     return chunk_date_range(start_date, self.ignore_weekends)

    # def get_updated_state(self, current_stream_state: MutableMapping[str, Any], latest_record: Mapping[str, Any]):
    #     current_stream_state = current_stream_state or {}
    #     current_stream_state[self.date_field_name] = max(
    #         latest_record[self.date_field_name], current_stream_state.get(self.date_field_name, self._start_date)
    #     )
    #     return current_stream_state


# def chunk_date_range(start_date: DateTime, ignore_weekends: bool) -> Iterable[Mapping[str, Any]]:
#     """
#     Returns a list of each day between the start date and now. Ignore weekends since exchanges don't run on weekends.
#     The return value is a list of dicts {'date': date_string}.
#     """
#     days = []
#     now = pendulum.now()
#     while start_date < now:
#         day_of_week = start_date.day_of_week
#         if day_of_week != pendulum.SATURDAY and day_of_week != pendulum.SUNDAY or not ignore_weekends:
#             days.append({"date": start_date.to_date_string()})
#         start_date = start_date.add(days=1)

#     return days


class SourceHttpRequest(AbstractSource):
    def check_connection(self, logger: AirbyteLogger, config: Mapping[str, Any]) -> Tuple[bool, Any]:
        try:
            params = {}

            #params["access_key"] = config["access_key"]

            resp = requests.get(f"{config['base_url']}", params=params)
            status = resp.status_code
            logger.info(f"Ping response code: {status}")
            if status == 200:
                return True, None
            # When API requests is sent but the requested data is not available or the API call fails
            # for some reason, a JSON error is returned.
            # https://exchangeratesapi.io/documentation/#errors
            error = resp.json().get("error")
            code = error.get("code")
            message = error.get("message") or error.get("info")
            # If code is base_currency_access_restricted, error is caused by switching base currency while using free
            # plan
            if code == "base_currency_access_restricted":
                message = f"{message} (this plan doesn't support selecting the base currency)"
            return False, message
        except Exception as e:
            return False, e

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        return [HttpRequest(config.get("base_url"), config)]
