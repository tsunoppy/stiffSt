import linecache

line = linecache.getline('./H_Shape.csv', 2)
data = line.split(',')
print(data)
