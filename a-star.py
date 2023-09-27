import math
#this import is so that we can take in command line arguments
import sys

# For Testing if txt files were read correctly
def display(coords, maps):
  # Display Coord Dicts
  for key, value in coords.items():
      print(key, ':', value)
  
  print("\n")
  
  # Display Map Distances
  for key, value in maps.items():
    print(key, ':', value)

def convertradian(degrees):
  rad = math.radians(degrees)
  return rad

# Haversine Formula
def haversine(a, b): # pass in 2 coords
  r = 3958.8 #radius of the earth

  x1 = convertradian(a[0])  # latitude
  y1 = convertradian(a[1]) # longitude

  x2 =convertradian(b[0]) 
  y2 = convertradian(b[1])

  # MATH 
  z = math.sqrt((math.sin((x2-x1)/2) ** 2)
            + math.cos(x1) 
            * math.cos(x2) 
            * (math.sin((y2-y1)/2) ** 2)
           )

  d = 2 * r * (math.asin(z))
  d = math.floor(d * 100)/100.0
  return d
    
# # A* Algorithm function
# # f(n) = g(n) + h(n)
# # g(n) given in map.txt
# # a = from // b = to

def astar(coords, maps, a, b):
  open = []
  closed = []
  start = a # starting node  (sanfran)
  goal = b # final destination / goal node  (longbeach)
  parent = {} # dictionary of each node's with their parent 
  totalDist = 0.0 # total heuristic distance to the goal node

  open.append(start)
  parent[a] = a
  # bestcity = ''
  totalg = 0 # the total g distance of the route
  currentCity = a
  fl = "" # city with the lowest value f(n) (aka current node)
  
  while len(open) != 0:
    # grab node with the lowest total out of the entire list

    # Update a for when we go from one city to the other 
    # a should always be the last city we went to on best route
    if len(closed) != 0:
      currentCity = fl
    
    x = 10000 # smallest value of f(n)
    y = 0
    # fl = "" # city with the lowest value f(n) (aka current node)

    costs = maps[currentCity]
    costsKeys = maps[currentCity].keys() # cities connected to the current
    # search through open list to find the node with lowest f
    for i in open: # { Arad }
      h = haversine(coords[i], coords[goal])
      if i == start:
        g = 0
        f = totalg + g + h # f is the total distance
      else: # if i not the same as a
        # Checks to see if the city (i) is connected to the current city 
        if i in costsKeys:
          g = costs[i]
          f = totalg + g + h # f is the total distance
        elif i not in costsKeys: # if city i ISNT connected to the current city
          tempcity = i
          g = 0 
          while parent[tempcity] != tempcity:
            pastfl = tempcity
            tempcity = parent[tempcity]
            g += maps[pastfl][tempcity]
          f = g + h

          
      # lowest f node
      # save smallest f value node
      if f < x:
        x = f
        y = g
        fl = i

    if fl not in costsKeys:
      totalg = y
    else:
      # totalg += y
      totalg = 0
      city = fl
      while city != start:
        pastfl = city
        city = parent[city]
        totalg += maps[pastfl][city]

    if fl in open:
      open.remove(fl) # remove from open list
    closed.append(fl) # add to closed list

    # if the location is the same as the desired destination, return it
    if fl == goal:
      # test statement for printing parent list for debug
      print('\n')
      for i,v in parent.items():
        print(i + " : " + v)
      print("\n")
      
      print(closed)
      
      route = []
      totalDist = 0
      while parent[fl] != fl:
        route.append(fl)
        pastfl = fl
        fl = parent[fl]
        totalDist += maps[pastfl][fl]
      route.append(fl)
      route.reverse()
      return route, totalDist # return best route here and total distance
    else:
      cities = maps[fl].keys() # generate each successor route 

    # { sanjose, napa, eureka, sac }
    for i in cities:
      h = haversine(coords[i], coords[goal])
      costs = maps[fl]
      g = costs[i]
      tempG = totalg + g 
  
      if i in open:
        if totalg <= tempG: # if the total cost is less than or equal to the cost going to this city
          if parent[i] != fl:
            g1 = 0
            g2 = 0
            currentp = parent[i]
            city = i
            while city != start:
              pastfl = city
              city = parent[city]
              g1 += maps[pastfl][city]
            
            city = i
            parent[i] = fl
            while city != start:
              pastfl = city
              city = parent[city]
              g2 += maps[pastfl][city]

            if g1 < g2:
              parent[i] = currentp
            
          continue
      elif i in closed:
        if totalg <= tempG:
          continue
        # move successor from closed list to the open list
        closed.remove(i)
        open.append(i)
      else:
        open.append(i)
        parent[i] = fl 


  if fl != goal:  
    print("Error: The open list is empty, there is no optimal route")
  

def main(argv): # take in console  
# def main():
  # Reading Coordinates 
  coordsfile = open("coordinates.txt", "r")
  coordsdata = coordsfile.read().splitlines()
  
  count = 0
  coords = {}

  for line in coordsdata:
      count += 1
      items = line.split(':')
  
      #this gets rid of the parentheses from the line and splits tuple into 2 numbers
      item2 = items[1].replace("(", "").replace(")","")
      latLong = item2.split(',')
  
      #use map to convert the latitude and longitude to floats instead of string
      result = map(float, latLong)
  
      # creating entries for the dictionary
      # key's are the city and the value is the latitude and longitude
      key, values = items[0], tuple(result)
      coords[str(key)] = values

  # Reading Map
  mapfile = open("map.txt", "r")
  mapdata = mapfile.read().splitlines()
  
  count2 = 0
  maps = {}

  for line2 in mapdata:
    count2 += 1
    # get rid of dash 
    map1 = line2.split('-')
    loc1 = map1[0] # stores san jose
    
    # split by commas
    # SanFrancisco(48.4),Monterey(71.7),Fresno(149),SantaCruz(32.7)
    map2 = map1[1].split(',')
  
    #SanFrancisco(48.4 Monterey(71.7 Fresno(149 SantaCruz(32.7
    # each are elements within the map2 - have to split by () now 
    tempMap = {} # nested map
    count = 0
    for i in map2:
      cityDist = i.split('(')
      city = cityDist[0]
      tempDist = cityDist[1].replace(")","")
      distance = float(tempDist)
      tempMap[str(city)] = distance
  
    keys2, values2 = loc1, tempMap
    maps[str(keys2)] = values2

  # test display for what the code read from the txt files
  # display(coords, maps) 

  # uncomment this when you want to use command line arguments
  location1 = argv[1]
  location2 = argv[2]
  # location1 = str(input())
  # location2 = str(input())

  bestroute, totalDist = astar(coords, maps, location1, location2)

  # Display output format
  print("From city: {}".format(location1))
  print("To city: {}".format(location2))

  print("Best Route: ", end='')
  count = 0
  for i in bestroute:
    if count < len(bestroute) - 1:
      print(i, end=' - ')
      count += 1
    else:
      print(i)
  
  print("Total distance: %.2f" % totalDist, end=" mi")
  print("\n")
  
# uncomment this when you want to use command line arguments  
main(sys.argv)
# main()