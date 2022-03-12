import json
import turtle
import urllib.request
import time
import geocoder


def create_pen(iss_name: str):
    iss = turtle.Turtle()
    iss.shape(f'assets/iss_s/{iss_name}')
    iss.setheading(45)
    iss.pensize(5)
    return iss


def get_command() -> list[str, ...]:
    url: str = "http://api.open-notify.org/astros.json"
    response: object = urllib.request.urlopen(url)
    result: dict = json.loads(response.read())
    humans_info: list = result['people']
    iss_command: list[str, ...] = [hi['name'] for hi in humans_info if hi['craft'] == 'ISS']
    return iss_command


def go_to_noprint(iss,  lat: float, lng: float) -> None:
    iss.penup()
    iss.goto(lat, lng)


def print_command(iss, chosen_map: str, iss_command: list[str, ...]) -> None:
    team: str = ", ".join(iss_command[0:5]) + ' and others ...' if len(iss_command) > 5 else ', '.join(iss_command)
    usr_location: list[float, float] = geocoder.ip('me').latlng
    if chosen_map == 'old':
        go_to_noprint(iss, -175, 82)
        iss.pendown()
        iss.pencolor('#eaebe4')
        iss.write(arg=f'Flying ship crew({len(iss_command)}): {team}', font=("Pacifico", 15, "italic"))
        go_to_noprint(iss, usr_location[0]-10, usr_location[1]-35) #-40 fix for map pic
        iss.pendown()
        iss.pencolor('black')
        iss.write(arg='〠', font=("Pacifico", 20, "bold"))
        iss.pencolor('#2d2485')
    else:
        go_to_noprint(iss, -175, 85)
        iss.pendown()
        iss.pencolor('#2d2485')
        iss.write(arg=f' ISS crew({len(iss_command)}): {team}', font=("Righteous", 13, "bold"))
        go_to_noprint(iss, usr_location[0], usr_location[1])
        iss.pendown()
        iss.write(arg='㋛', font=("Righteous", 20, "bold"))
    iss.penup()


def get_now_location() -> tuple[float, float]:
    url: str = "http://api.open-notify.org/iss-now.json"
    response: object = urllib.request.urlopen(url)
    result: dict = json.loads(response.read())
    location: dict = result["iss_position"]
    lat, lon = float(location['latitude']), float(location['longitude'])
    return lat, lon


def correct_coordinate_for_map(map_chosen, lat, lon) -> tuple[float, float]:
    if map_chosen == 'old':
        lat -= 10
        lon -= 10
    return lat, lon


def iss_move(iss, new_lat: float, old_lat: float, new_lon: float, old_lon: float) -> tuple[float, float]:
    steps: int = 20
    step_lat, step_lon = (new_lat - old_lat) / steps, (new_lon - old_lon) / steps
    for pos in range(steps+1):
        old_lat += step_lat
        old_lon += step_lon
        iss.goto(old_lon, old_lat)
        time.sleep(3)
    return new_lat, new_lon


def print_trace(iss, lat: float, lon: float, trace_mark: str = '*', font: tuple[str, int, str] = ("Righteous", 15, "bold")) -> None:
    iss.goto(lon, lat)
    iss.pendown()
    iss.write(arg=trace_mark, font=font)
    iss.penup()


def coordinate_log(waypoints: list[tuple[float, float], ...], iss, lat: float, lon: float) -> list[tuple[float, float], ...]:
    way_point: tuple[float, float] = waypoints.pop(0)
    point_lat, point_lon = way_point[0], way_point[1]
    print_trace(iss, point_lat, point_lon)
    print("\nLatitude: " + str(lat)) # ориг позиции неотредакт под карту
    print("Longitude: " + str(lon))
    return waypoints


def generate_route_prehistory(old_lat: float, old_lon: float, new_lat: float, new_lon: float) -> tuple[float, float]:
    old_lat: float = old_lat+10 if old_lat > new_lat else old_lat-10
    old_lon: float = old_lon+10 if old_lon > new_lon else old_lon-10
    return old_lat, old_lon


def iss_main(map_chosen: str, iss) -> None:
    old_lat, old_lon = get_now_location()
    waypoints: list = []
    if map_chosen == 'old':
        old_lat, old_lon = correct_coordinate_for_map(map_chosen, old_lat, old_lon)
        time.sleep(1)
        new_lat, new_lon = get_now_location()
        new_lat, new_lon = correct_coordinate_for_map(map_chosen, new_lat, new_lon)
        old_lat, old_lon = generate_route_prehistory(old_lat, old_lon, new_lat, new_lon)

        while True:
            new_lat, new_lon = get_now_location()
            new_lat, new_lon = correct_coordinate_for_map(map_chosen, new_lat, new_lon)
            old_lat, old_lon = iss_move(iss, new_lat, old_lat, new_lon, old_lon)
            waypoints.append((old_lat-10, old_lon))
            if len(waypoints) == 3:
                waypoints: list[tuple[float, float], ...] = coordinate_log(waypoints, iss, old_lat, old_lon)
    else:
        time.sleep(1)
        new_lat, new_lon = get_now_location()
        old_lat, old_lon = generate_route_prehistory(old_lat, old_lon, new_lat, new_lon)
        while True:
            new_lat, new_lon = get_now_location()
            old_lat, old_lon = iss_move(iss, new_lat, old_lat, new_lon, old_lon)
            waypoints.append((old_lat - 10, old_lon))
            if len(waypoints) == 3:
                waypoints: list[tuple[float, float], ...] = coordinate_log(waypoints, iss, old_lat, old_lon)


def map_config(map_chosen: str) -> tuple[str, str]:
    maps = {'old': 'old_map.gif', 'political': 'Political_map.png',
            'physical': 'Physical_map.png'}
    iss_s = {'old': 'old_fly_ship.gif', 'now': 'ISS_01b.gif'}
    map_name = maps[map_chosen]
    iss_name = iss_s['old'] if map_chosen == 'old' else iss_s['now']
    return map_name, iss_name


def map_main(map_chosen):
    screen = turtle.Screen()
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)
    map_name, iss_name = map_config(map_chosen)
    screen.bgpic(f'assets/maps/{map_name}')
    screen.register_shape(f'assets/iss_s/{iss_name}')
    iss = create_pen(iss_name)
    print_command(iss=iss, chosen_map=map_chosen, iss_command=get_command())
    iss_main(map_chosen, iss)


if __name__ == '__main__':
    map_main('old')