import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder


def create_pen():
    iss = turtle.Turtle()
    iss.shape(f'assets/iss_s/{iss_name}')
    iss.setheading(45)
    iss.pensize(5)
    return iss


def get_command():
    url = "http://api.open-notify.org/astros.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    humans_info: list = result['people']
    # all_peoples = []
    iss_command = []
    for hi in humans_info:
        # all_peoples.append(hi['name'])
        if hi['craft'] == 'ISS':
            iss_command.append(hi['name'])
    return iss_command


def go_to_noprint(iss,  lat, lng):
    iss.penup()
    iss.goto(lat, lng)


def print_command(iss, map, iss_command):
    team = ", ".join(iss_command[0:5]) + ' and others ...' if len(iss_command) > 5 else ', '.join(iss_command)
    usr_location = geocoder.ip('me').latlng
    if map == 'old':
        go_to_noprint(iss, -175, 82)
        iss.pendown()
        iss.pencolor('#eaebe4')
        iss.write(arg=f'Flying ship crew: {team}', font=("Pacifico", 15, "italic"))
        go_to_noprint(iss, usr_location[0]-10, usr_location[1]-35) #-40 fix for map pic
        iss.pendown()
        iss.pencolor('black')
        iss.write(arg='〠', font=("Pacifico", 20, "bold"))
        iss.pencolor('#eaebe4')
    else:
        go_to_noprint(iss, -175, 85)
        iss.pendown()
        iss.pencolor('#2d2485')
        iss.write(arg=f' ISS crew: {team}', font=("Righteous", 13, "bold"))
        go_to_noprint(iss, usr_location[0], usr_location[1])
        iss.pendown()
        iss.write(arg='㋛', font=("Righteous", 20, "bold"))
    iss.penup()


def now_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result["iss_position"]
    lat, lon = float(location['latitude']), float(location['longitude'])
    return lat, lon


def correct_coordinate_for_map(map_chosen,lat,lon):
    if map_chosen == 'old':
        lat -=10
        lon -=10
    return lat, lon


def iss_move(iss, new_lat, old_lat, new_lon, old_lon):
    steps = 20
    step_lat, step_lon = (old_lat-new_lat)/steps, (old_lon-new_lon)/steps
    for pos in range(steps+1):
        old_lat += step_lat
        old_lon += step_lon
        iss.goto(old_lon, old_lat)
        time.sleep(3)
    return new_lat, new_lon


def print_trace(iss, lat, lon, trace_mark='*', font=("Righteous", 15, "bold")):
    iss.goto(lon, lat)
    iss.pendown()
    iss.write(arg=trace_mark, font=font)
    iss.penup()


def coordinate_log(lat, lon):
    print("\nLatitude: " + str(lat))
    print("Longitude: " + str(lon))


def iss_main(map_chosen, iss):
    old_lat, old_lon = now_location()
    if map_chosen == 'old':
        old_lat, old_lon = correct_coordinate_for_map(map_chosen, old_lat, old_lon)
        while True:
            new_lat, new_lon = now_location()
            new_lat, new_lon = correct_coordinate_for_map(map_chosen, new_lat, new_lon)
            old_lat, old_lon = iss_move(iss, new_lat, old_lat, new_lon, old_lon)
            print_trace(iss, old_lat-10, old_lon)
            coordinate_log(old_lat, old_lon)
    else:
        while True:
            new_lat, new_lon = now_location()
            old_lat, old_lon = iss_move(iss, new_lat, old_lat, new_lon, old_lon)
            print_trace(iss, old_lat, old_lon)
            coordinate_log(old_lat, old_lon)


if __name__ == '__main__':
    screen = turtle.Screen()
    screen.setup(1280, 720)
    screen.setworldcoordinates(-180, -90, 180, 90)
    maps = {'old': 'old_map.gif', 'political': 'Political_map.png',
            'physical': 'Physical_map.png'}
    iss_s = {'old': 'old_fly_ship.gif', 'now': 'ISS_01b.gif'}
    # map_chosen = input('\nmaps?(old,political,physical)')
    map_chosen = 'old'
    map_name = maps[map_chosen]
    screen.bgpic(f'assets/maps/{map_name}')
    iss_name = iss_s['old'] if map_chosen == 'old' else iss_s['now']
    screen.register_shape(f'assets/iss_s/{iss_name}')
    iss = create_pen()
    iss_command = get_command()
    print_command(iss=iss, map=map_chosen, iss_command=iss_command)
    iss_main(map_chosen, iss)