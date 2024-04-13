import abc
import csv
import json
import time
from typing import Any

import requests

from models import Route, RouteType

from loguru import logger


def cast_to_str(object: Any) -> str | None:
    if object is None:
        return 'N/A'
    try:
        return str(object)
    except:
        return 'N/A'


class RouteServiceInterface(abc.ABC):
    def get_route_time(self, route: Route, route_type: RouteType) -> int | None:
        ...

    @staticmethod
    def _parse_route(route: str) -> Route:
        route = list(map(float, route.split(",")))
        return Route(id=int(route[0]),
                     a_x=route[1],
                     a_y=route[2],
                     b_x=route[3],
                     b_y=route[4])

    def get_routes_from_file(self, filename: str) -> list[Route]:
        data = []
        with open(filename, encoding="utf8") as file:
            csvfile = csv.reader(file, delimiter=";", quotechar='"')
            for idx, lines in enumerate(csvfile):
                if idx == 0:
                    continue
                data.append(self._parse_route(lines[0]))
        return data

    def count_routes_time(self, routes: list[Route], route_type: RouteType) -> list[dict]:
        import concurrent.futures

        """Returns dict format list[{id: time}]"""
        routes_time = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Создаем список задач для выполнения в отдельных потоках
            futures = [executor.submit(self.get_route_time, route, route_type) for route in routes]
            # Дожидаемся завершения всех задач
            for future, route in zip(futures, routes):
                try:
                    route_time = future.result()
                    routes_time.append({'id': cast_to_str(route.id), 'route_time': cast_to_str(route_time)})
                except Exception as e:
                    logger.error(f"Error calculating route time")
            return routes_time


class RouteServiceOSRM(RouteServiceInterface):
    def __init__(self, base_url: str):
        self.base_url = base_url

    # base_url = 'http://router.project-osrm.org'
    # resp = requests.get(f'{base_url}/route/v1/car/59.946252,30.35764;60.2719474,30.4652774')
    # pprint.pprint(resp.json()['routes'][0]['duration'])
    def get_route_time(self, route: Route, route_type: RouteType) -> int | None:
        """Returns route time in seconds"""
        resp = requests.get(f'{self.base_url}{route_type.value}/{route.a_x},{route.a_y};{route.b_x},{route.b_y}')
        time.sleep(1)
        try:
            if resp.status_code == 200:
                logger.info(f"{route.id}:{resp.json()['routes'][0]['duration']}")
                return resp.json()['routes'][0]['duration']
            else:
                logger.error(f"Status code:{resp.status_code}")
        except Exception as e:
            logger.error(e)
            raise PermissionError(e)


# class RouteService2Gis(RouteServiceInterface):
#     def __init__(self, base_url: str, api_key: str, headers: dict):
#         self.base_url = base_url
#         self.api_key = api_key
#         self.headers = headers
#
#     def get_route_time(self, route: Route, route_type: RouteType) -> int | None:
#         """Returns route time in seconds"""
#         data = {
#             "points": [
#                 {"lat": route.a_x, "lon": route.a_y},
#                 {"lat": route.b_x, "lon": route.b_y}
#             ],
#             "sources": [0],
#             "targets": [1],
#             "mode": route_type.value,
#             "type": "statistics"
#         }
#         resp = requests.post(url=f"{self.base_url}get_dist_matrix?key={self.api_key}&version=2.0",
#                              data=json.dumps(data),
#                              headers=self.headers)
#         try:
#             if resp.status_code == 200:
#                 logger.info(resp.json()['routes'][0]['duration'])
#                 return resp.json()['routes'][0]['duration']
#             else:
#                 logger.error(f"Status code:{resp.status_code}, info: {resp.text}")
#         except Exception as e:
#             logger.error(e)
#             raise PermissionError(e)
