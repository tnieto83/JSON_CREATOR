import seaborn as sb
planets = sb.load_dataset('planets')
print(type(planets))



in_2008 = planets['method'] == 'Radial Velocity'
in_2008.head()
planets_2008 = planets[in_2008]
print(planets_2008)