"""https://project-osrm.org/docs/v5.24.0/api/#"""
from models import Route, RouteType
from route_service import RouteServiceInterface, RouteServiceOSRM
import csv

SOURCE_FILENAME = f'part_1.csv'


async def test() -> int | None:
    route_service: RouteServiceInterface = RouteServiceOSRM(base_url='http://router.project-osrm.org/route/v1/')
    return route_service.get_route_time(route=Route(id=0,
                                                    a_x=59.8470433,
                                                    a_y=30.3296737,
                                                    b_x=59.927378,
                                                    b_y=30.360623),
                                        route_type=RouteType.CAR)


def write_to_csv_file(filename: str, data: list[dict]) -> None:
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['id', 'route_time'])
        writer.writeheader()
        writer.writerows(data)


def main():
    base_url = 'http://router.project-osrm.org/route/v1/'
    route_service: RouteServiceInterface = RouteServiceOSRM(base_url=base_url)

    routes: list[Route] = route_service.get_routes_from_file(filename=f"data/{SOURCE_FILENAME}")

    counted_data = route_service.count_routes_time(routes=routes, route_type=RouteType.CAR)

    write_to_csv_file(filename=f'collected_data/{SOURCE_FILENAME}', data=counted_data)


if __name__ == '__main__':
    main()
