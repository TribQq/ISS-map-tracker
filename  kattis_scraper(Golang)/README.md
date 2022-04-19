# Kattis scraper

🔎 Kattis web scraper.

(Currently) A CLI kattis Web Scraper that gives all solved problems of a user, along with their difficulty and their URL.

## Getting started

Make sure you have Go installed on your machine (1.14+), and that $PATH leads to your binary go files.

```
$ go get github.com/TribQq/mini_apps/tree/master/%20kattis_scraper(Golang)
$ go install github.com/TribQq/mini_apps/tree/master/%20kattis_scraper(Golang)
```

You should add a `.env` file with two parameters : 
```
EMAIL:email
PASSWORD:password
```
where _email_ is your Kattis email, and _password_ is your kattis password.

## How to use it

Simply run the following 
```
$ kattis-scrapper
```

Currently returns a difficulty-sorted list of your solved problems (alphabetically, increasing difficulty or decreasing difficulty ordering possible).

**⚠️ Note: Make sure to have the .env file in that location.**

### Example

```
$ kattis-scrapper
1: Hello World!, 1.2, https://open.kattis.com/problems/hello
2: Planina, 1.3, https://open.kattis.com/problems/planina
3: Cold-puter Science, 1.3, https://open.kattis.com/problems/cold
4: Pot, 1.3, https://open.kattis.com/problems/pot
5: Quality-Adjusted Life-Year, 1.3, https://open.kattis.com/problems/qaly
6: Piece of Cake!, 1.3, https://open.kattis.com/problems/pieceofcake2
7: Detailed Differences, 1.4, https://open.kattis.com/problems/detaileddifferences
8: Simon Says, 1.4, https://open.kattis.com/problems/simonsays
9: No Duplicates, 1.4, https://open.kattis.com/problems/nodup
10: Spavanac, 1.4, https://open.kattis.com/problems/spavanac
11: Solving for Carrots, 1.4, https://open.kattis.com/problems/carrots
12: Oddities, 1.4, https://open.kattis.com/problems/oddities
13: Soda Slurper, 1.5, https://open.kattis.com/problems/sodaslurper
```

## Behaviour for Unexpected Results

Here are some explanations for weird results of the program:

### Difficulty of 0 on a problem ?
Scraper could not parse the difficulty of the problem, it may be related to some weird notations like this one (TODO):

![Unprecise difficulty](https://github.com/TribQq/mini_apps/tree/master/%20kattis_scraper(Golang)/assets/pb_ex1.PNG)

### Not a valid link for a problem ?
Scraper could not parse the link associated with the problem.
