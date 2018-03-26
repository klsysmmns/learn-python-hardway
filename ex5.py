name = 'Zed A. Shaw'
age = 35 # not a lie
height = 74 #inches
weight = 180 # lbs
eyes = 'Blue'
teeth = 'White'
hair = 'Brown'
cmheight = height * 2.54
kgweight = weight * 0.453592

print 'Let\'s talk about {0}.'.format(name)
print 'He\'s {0} inches tall.'.format(cmheight)
print 'He\'s {0} pounds heavy.'.format(kgweight)
print 'Actually that\'s not too heavy.'
print 'He\'s got {0} eyes and {1} hair.'.format(eyes, hair)
print 'His teeh are usually {0} depending on the coffee.'.format(teeth)

#this line is tricky try to get it exactly right
print 'If I add {0}, {1}, and {2} I get {3}.'.format(age, height, weight, age + height + weight)
