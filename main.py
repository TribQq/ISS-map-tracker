import json
import turtle
import urllib.request
import time
import webbrowser
import geocoder

url = "http://api.open-notify.org/astros.json"
response = urllib.request.urlopen(url)
result = json.loads(response.read())


file = open("iss.txt", "w")
file.write("There are currently " +
           str(result["number"]) + " astronauts on the ISS: \n\n")
people = result["people"]
for p in people:
    file.write(p['name'] + " - on board" + "\n")
# print long and lat
g = geocoder.ip('me')
file.write("\nYour current lat / long is: " + str(g.latlng))
file.close()
webbrowser.open("iss.txt")



screen = turtle.Screen()
screen.setup(1280, 720)

screen.setworldcoordinates(-180, -90, 180, 90)

# screen.bgpic('assets/maps/Physical_adapt_1.png')
map_name = 'old_map.gif'
screen.bgpic(f'assets/maps/{map_name}')

# screen.register_shape("assets/isss/ISS_01b.gif") #
screen.register_shape(f"assets/isss/old_fly_ship.gif")

iss = turtle.Turtle()

# iss.shape('assets/isss/ISS_01b.gif')
iss.shape('assets/isss/old_fly_ship.gif')
iss.setheading(45)
iss.pensize(5)
iss.pencolor('white')
iss.penup()
iss.goto(10, 10)
iss.pendown()
iss.write('Board command: ')
iss.penup()


def now_location():
    url = "http://api.open-notify.org/iss-now.json"
    response = urllib.request.urlopen(url)
    result = json.loads(response.read())
    location = result["iss_position"]
    new_lat, new_lon = float(location['latitude']), float(location['longitude'])
    print("\nLatitude: " + str(new_lat))
    print("Longitude: " + str(new_lon))
    if map_name == 'old_map.gif':
        new_lat -= 10
        new_lon -= 20

    return new_lat, new_lon


old_lat, old_lon = now_location()
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