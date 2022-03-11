import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder


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
screen.register_shape(f'assets/iss_s/{iss_name}'
#if f
                      )


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


def go_to_noprint(iss,map,  lat, lng):
    iss.penup()

    iss.goto(lat, lng)


def print_command(iss, map, iss_command):
    team = ", ".join(iss_command[0:5]) + ' and others ...' if len(iss_command) > 5 else ', '.join(iss_command)
    usr_loaction = geocoder.ip('me').latlng
    if map == 'old':
        go_to_noprint(iss, map, -175, 82)
        iss.pendown()
        iss.pencolor('#eaebe4')
        iss.write(arg=f'Flying ship crew: {team}', font=("Pacifico", 15, "italic"))
        go_to_noprint(iss, map, usr_loaction[0]-10, usr_loaction[1]-35) #-40 fix for map pic
        iss.pendown()
        iss.pencolor('black')
        iss.write(arg='〠', font=("Pacifico", 20, "bold"))
        iss.pencolor('#eaebe4')
    else:
        go_to_noprint(iss, map, -175, 85)
        iss.pendown()
        iss.pencolor('#2d2485')
        iss.write(arg=f' ISS crew: {team}', font=("Righteous", 13, "bold"))
        go_to_noprint(iss,map, usr_loaction[0], usr_loaction[1])
        iss.pendown()
        iss.write(arg='㋛', font=("Righteous", 20, "bold"))
    iss.penup()

iss = create_pen()
iss_command = get_command()
print_command(iss=iss, map=map_chosen, iss_command=iss_command)


def now_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result["iss_position"]
    new_lat, new_lon = float(location['latitude']), float(location['longitude'])
    print("\nLatitude: " + str(new_lat))
    print("Longitude: " + str(new_lon))
    if map_name == 'old_map.gif':
        new_lat -= 35
        new_lon -= 10

    return new_lat, new_lon

old_lat, old_lon = now_location()



#TODO optimize for map, flight trail
while True:
    new_lat, new_lon = now_location()
    # (0, 0) if (old_lat, old_lon) == (0, 0) else
    step_lat, step_lon = (old_lat-new_lat)/10, (old_lon-new_lon)/10

    for pos in range(11):
        old_lat += step_lat
        old_lon += step_lon
        iss.goto(old_lon, old_lat)
        time.sleep(3)
    old_lat, old_lon = new_lat, new_lon
    print("\nLatitude: " + str(old_lat))
    print("Longitude: " + str(old_lon))
    iss.pendown()
    iss.write('o') # every 10(move to every 3)
    iss.penup()
    # time.sleep(30) # to do list 30sec