# 30DayMapChallenge 2026

This is my contribution to the #30DayMapChallenge for November 2026.\
About the #30DayMapChallenge , check out <https://30daymapchallenge.com/> !

## Introduction

### About me

I am currently a Principal Geomatics Engineer at the Singapore Land Authority and hold an MSc in Urban Spatial Science from the Centre for Advanced Spatial Analysis (CASA), University College London (UCL). \
I specialise in Geographic Information Systems (GIS), Remote Sensing, Data Science, and Agent-Based Modelling. \
For opportunities or collaboration, I can be contacted via [LinkedIn](https://www.linkedin.com/in/james-tan-song-en-76b73418a/)

### Day 20: Hexagons
 
I have done bivariate and 3D bivariate hexagons for this theme in previous years, so this time each hexagon is a mini scorecard, with each wedge showing how accessible a different everyday need is.
 
I first thought about a country-wide map (e.g. elevation, rainfall, temperature, population, vegetation), but at that scale each hexagon either has to be tiny which is too small to read the wedges, or so big that it averages away the detail. So I settled on one city and one idea: the “X-minute city”, where daily essentials are within walking distance.
 
In 2017, Melbourne launched Plan Melbourne, which defines a 20-minute neighbourhood as one where people can meet most daily needs within a 20-minute return walk from home.
 
This map shows that only 10% of walkable Melbourne has all six within reach. There are a few caveats. Scale matters so changing the hexagon size changes the result (i.e. how you define a “neighbourhood” shapes the answer). The analysis also assumes an average walking speed, so for people with different mobility needs, the map could look quite different.

![Day 20](Day%2020/Day%2020.png)

### Day 19: Senses: Smell

While searching for inspiration, I came across Kate McLean’s smellmaps (part of her Sensory Maps project). She records smells while walking around a city, then turns them into contour maps of the city's scents.

I loved the style, but I didn't have the luxury of time to walk around and collect scents myself. The proxy I thought of was trees and flowers which have some of the strongest smells in a city. Many cities also publish open street-tree registers with species and trunk size. I experimented with a few cities' registers (New York, Melbourne, Paris) and decided to focus on Vienna.

How the map is designed is that each fragrant tree gives off a "scent cloud" (modelled, not measured), and the bigger the trunk diameter, the bigger the cloud. Where trees cluster, the clouds stack up into stronger rings.

Next time, I would love to try other scent sources such as food (e.g. bakeries or coffee roasters) or get a group of people to walk around an area, record what they smell, and see what the crowdsourced map looks like.

![Day 19](Day%2019/Day%2019.png)

Data Source: [Tree register or tree locations in Vienna](https://www.data.gv.at/datasets/c91a4635-8b7d-43fe-9b27-d95dec8392a7?locale=de) 

### Day 18: null

I was originally thinking of mapping Point Nemo or Null Island, but decided to map absence instead. In OpenStreetMap, buildings can be tagged as abandoned, ruined or disused, so I went looking for a place where null takes up a whole district.  The place I landed on was Varosha, the beachfront district of Famagusta, Cyprus. In the early 1970s it was one of the Mediterranean's best-known tourist destinations, but it was fenced off in 1974 during the conflict that divided the island. Since 2020, parts of it have slowly been opening up to the public.

![Day 18](Day%2018/Day%2018.png)

### Day 17: Light & Shadow

Rjukan (Norway) sits in a valley where the mountains block the sun from late September to mid-March. The town’s founder first proposed a sun mirror in 1913 which was finally built in 2013. Today, three sun-tracking mirrors on the slope reflect light onto the town square.

The map compares direct sun hours on the winter solstice, when the town square gets 0 minutes of sun, with the spring equinox, when it gets 18 minutes. The map was made with [cityshade](https://janosovm.gumroad.com/l/cityshade), a Python library by Milan Janosov. It was easy to use and there are plenty of tutorials.

![Day 17](Day%2017/Day%2017.png)

### Day 16: Collaborative Map

A few years ago I collected Pokémon GO gift data from a number of contacts and this map uses one of them. In Pokémon GO, every gift a friend sends shows the PokéStop where they picked it up. Using this one subject's gifts, I tried to work out where they lived and worked in Maine. A cluster of many different stops close together suggested home or the surrounding neighbourhood, while the same stop repeating over and over pointed to a workplace, somewhere the person spent all day. The names of the stops also gave extra context: a library, post office and ice cream shop hint at everyday errands, while two marine research labs look a lot like a job. 

Disclaimer: the subject stays anonymous and is no longer based in the area. All data was shared with consent.

![Day 16](Day%2016/Day%2016.png)

### Day 15: Inside Out

We are at the halfway mark of the challenge. For this prompt, I swapped the places of oceans and continents, so up becomes down and vice versa.
 
Terra Inversa takes Earth’s elevation and depth (from GEBCO) and multiplies it by −1. The ocean floor rises into land, and the continents sink into the sea.
 
A few things to note in this inverted world: the Mariana Trench becomes the highest mountain on the planet, while the Himalaya becomes the deepest trench. There are also no oceans on Terra Inversa as every old continent becomes a landlocked sea, cut off from the others.

![Day 15](Day%2015/Day%2015_edited_compressed.png)

Data Source: [GEBCO_2026 Grid (ice surface elevation)](https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2026-grid) 

### Day 14: Borgesian map

I kinda wanted to do everything, everywhere all at once, so I tried to force a few datasets into a blueprint-style layout. This included OSM buildings and streets, plus the City of Melbourne’s open inventories of street lighting, trees and street furniture (consisting of 15 categories such as bollards, bins, bicycle parking and BBQ pits).
 
That adds up to 82,064 trees, 106,037 street-lighting points and 26,250 pieces of street furniture all in one municipality. Zoomed out, it looks almost artistic, but zoom into any area and you see how much detail has been captured.
 
The theme comes from Borges’ “On Exactitude in Science”, where an empire’s cartographers make a map so detailed it is the same size as the empire and hence is useless.

![Day 14](Day%2014/Day%2014.png)

Data Source: [Trees, with species and dimensions (Urban Forest)](https://discover.data.vic.gov.au/dataset/trees-with-species-and-dimensions-urban-forest) ; [Street furniture including bollards, bicycle rails, bins, drinking fountains, horse troughs, planter boxes, seats, barbecues](https://discover.data.vic.gov.au/dataset/street-furniture-including-bollards-bicycle-rails-bins-drinking-fountains-horse-troughs-planter
) ; [Street lights with emitted lux level (council-owned lights only)](https://discover.data.vic.gov.au/dataset/street-lights-with-emitted-lux-level-council-owned-lights-only)

### Day 13: Interactions

Slightly late today, but agent-based modelling (ABM) takes a bit of time to build. ABM is one of my favourite techniques crafting the rules for each agent and building the world they live in. Unity is also my go-to for it nowadays, with 3D, physics and visuals all in one place. Cesium was a huge help as well, streaming Google’s photorealistic 3D tiles straight into Unity so the world looks like the real city.

For this one I made a Shibuya Crossing simulator. Pedestrians wait at the corners, then everyone crosses at once. There are two variables to play with:
• Crowd size: how many people are waiting at the lights
• Aggressiveness: the share of pedestrians who walk faster, give way less and cut straight through the crowd
Both polite and aggressive crowds bunch up in the middle of the crossing, but the aggressive pedestrians push through and get across faster, at the cost of a lot more bumping into each other.

The web version is on [Shibuya Crossing Simulator](https://jamestansongen.itch.io/shibuya-crossing-simulator) and the 3D tiles will stay live till 14 December.

![Day 13](Day%2013/Day%2013.gif)


### Day 12: Power

I decided to explore nuclear power trends as Singapore is studying whether nuclear could be an option, including through the IAEA’s Integrated Nuclear Infrastructure Review.

Since 2011, countries have taken very different paths. China has expanded nuclear power the most, while Germany and Taiwan have left it entirely. Japan has mothballed much of its fleet rather than retiring it, and the UAE and Belarus have switched on their first reactors, with Egypt and Bangladesh building theirs now. Every country has its own reasons, whether safety, politics, energy security or growing demand. It is a reminder that whether to go nuclear is less a global trend than a national choice, shaped by each country’s own circumstances.

![Day 12](Day%2012/Day%2012.png)

Data Source: [Global Nuclear Power Tracker dataset](https://globalenergymonitor.org/projects/global-nuclear-power-tracker#download) ; [Yearly Electricity Data](https://ember-energy.org/data/yearly-electricity-data/)

### Day 11: Senses: Sound

🔊 Sound on for some 80s synthwave

For this one, I wanted the design itself to feel like music, so each city is an LED level meter, the kind you see bouncing on a stereo, showing how many live performances were logged there each year from 2010 to 2020. Across 50 cities, logged performances climbed steadily through the decade, from around 71,000 in 2010 to over 126,000 in 2019, before dropping 69% in 2020 during Covid. 
 
The data comes from setlist.fm, where fans log the sets they see live. It is quite comprehensive and has an open API, which made it easy to pull counts for every city and year. One caveat though is part of the rise in performances reflects more people using the site, not just more gigs.

![Day 11](Day%2011/Day%2011.gif)

Data Source: [setlist.fm](https://www.setlist.fm/)
Music: [On The Road To The Eighties” by Grand_Project / Roman Dudchyk, via Pixabay](https://pixabay.com/music/synthwave-on-the-road-to-the-eighties-loop1-177567/)

### Day 10: Prompting Only

For this one I handed the wheel to Claude Opus 5.5 and asked it to make a map of New York City in the style of Stardew Valley. The pixel aesthetic was something I wanted to try for a while but could never quite get right myself.

The rules I set included 1) no AI image generated map, 2) every pixel had to come from real geographic data and code and 3) it had to find the data and show me the code it used. It handled the whole workflow from start to finish from downloading the open data (streets, subway lines, surrounding counties) to processing and projecting everything in Python and creating the pixel textures (grass tufts, water sparkle, little trees in the parks) in code.

My job was mostly reviewing checking colour contrast, making sure the labels were legible and verifying accuracy. I checked the landmarks and didn’t spot any major issues. It was genuinely impressive to read back through the whole pipeline. It’s not perfect and still needed a human eye, but it’s a big leap from the AI-only map I made two years ago.

![Day 10](Day%2010/Day%2010.png)

### Day 9: Urban-Rural

Where exactly does urban end and rural begin? The shift from city to countryside is often more of a gradient than a sharp line, so how urban a place looks depends on where you draw the boundary.

This map looks at Paris through four official definitions, each one wider than the last:
1. Ville de Paris: the official city (104 km²)
2. Métropole du Grand Paris: the administrative metropolis (809 km²)
3. Unité urbaine: the continuous built-up area (2,819 km²)
4. Aire d’attraction: the commuter region (18,896 km²)

Measuring the land cover inside each one shows how quickly Paris turns rural: built-up land drops from 73% of the official city to just 8% of the commuter region while farmland rises from almost 0% to 50%.

![Day 9](Day%209/Day%209.png)

Data Source: [ESA WorldCover 10m 2021 v200](https://esa-worldcover.org/) ; [INSEE Base des unités urbaines 2020](https://www.insee.fr/fr/information/4802589) ; [INSEE Base des aires d'attraction des villes 2020](https://www.insee.fr/fr/information/4803954) ; [INSEE Base des EPCI à fiscalité propre au 1er janvier 2026](https://www.insee.fr/fr/information/2510634)

### Day 8: Utopia

“There will be no more death or mourning or crying or pain, for the old order of things has passed away.” (Revelation 21:4)

This one was tough. Every utopia I thought of, like fixing coastal flooding or making the built environment more liveable, comes with trade-offs and messy realities. So I went with the one place described as having none: the New Jerusalem.

The map draws mainly from Revelation 21–22 for the dimensions, gates, foundations, throne, tree and river, with gate placement taken from Ezekiel 48. I added the relevant verse next to each feature so you can see where it comes from.

Some verses need interpretation and are probably debated by Bible scholars, but this is my reading of the text.
![Day 8](Day%208/Day%208.png)

### Day 7: 10 minute map

This one came in under 10 minutes because most of the work was already done. This is my third aurora map using VIIRS night-time lights. Reusing the same code meant I only had to change the region of interest, the date range and the projection (orthographic so both hemispheres fit nicely).

Taking the maximum VIIRS pixel value (VNP46A2) for 1–15 October 2024, you can pick out where strong aurora appeared. That period includes the severe geomagnetic storm of 10–11 October. The northern lights glow green across Canada, and the southern lights reach the tip of South America near Tierra del Fuego.

![Day 7](Day%207/Day%207_edited.png)

Data Source: [VNP46A2: VIIRS Lunar Gap-Filled BRDF Nighttime Lights Daily L3 Global 500m](https://developers.google.com/earth-engine/datasets/catalog/NASA_VIIRS_002_VNP46A2)

### Day 6: Vintage

Two things immediately came to mind when I saw today's theme: Edinburgh's Old Town and the Marauder's Map from Harry Potter. This map brings those two ideas together, showing part of the walking route I took during my visit to Edinburgh in August 2024.

During my stay, I was based at 475 Lawnmarket. From there, I visited Edinburgh Castle, stopped for a cup of tea at The Elephant House (famous for its association with J.K. Rowling), and wandered through Greyfriars Kirkyard.

To achieve the Marauder's Map-inspired feel, I reduced the size of the buildings to create more space for the footprints to stand out. I then digitised my walking route and generated footprints along it to recreate the effect of wandering through the city. It took a bit of tinkering to get the look right, but I'm really pleased with how it turned out!

![Day 6](Day%206/Day%206.gif)

Data Source: [OpenStreetMaps](https://www.openstreetmap.org/#map=12/1.3649/103.8229)

### Day 5: Senses: Sight

The first of five senses in this year’s challenge and the obvious place to start felt like a visibility analysis.

From 1,085 metres, Yr Wyddfa can see far, but not everywhere. Ridges, cwms and its own shoulders hide whole valleys from view. The glowing areas are what the summit can see within 5 km. Everything in shadow is out of sight.

This viewshed was built on a 1 m digital surface model from DataMapWales, so buildings count as terrain, including the summit station and café, which end up blocking part of the view.

![Day 5](Day%205/Day%205_edited.png)

Data Source: [DSM from DataMapWales](https://datamap.gov.wales/maps/lidar-data-download/)

### Day 4: Clusters

I visited Dartmoor National Park in 2024 and was fascinated by the tors, the granite outcrops that crown the hilltops across the moor. For this map, I took 636 tors that the public can visit and used a clustering algorithm (HDBSCAN) to find where they naturally bunch together. It found 7 groups, each named after the tor closest to its middle, while 189 tors stand on their own.

And yes, there really is a place called Yes Tor.

![Day 4](Day%204/Day%204.png)

Data Source: [TORS OF DARTMOOR: a database of both lesser- & well-known rocks and outcrops](https://www.torsofdartmoor.co.uk/map.php)

### Day 3: Polygons

When we think of contours, we usually think of elevation. Two years ago I used contour polygons to map the Isle of Skye, and last year I applied them to the elevation and bathymetry of Crater Lake. But contours can be drawn for any continuous surface, so this year I mapped population density across Spain instead.

![Day 3](Day%203/Day%203_v2.png)

Data Source: [Unconstrainted individual countries 2020 UN adjusted (1km resolution)](https://hub.worldpop.org/geodata/listing?id=77), [Precipitation and Elevation](https://www.worldclim.org/data/worldclim21.html)

### Day 2: Lines

Two years ago for the same challenge, I imagined a train network connecting the US National Parks. This year, I headed south: what if South America had a railway linking all 27 of its natural and mixed UNESCO World Heritage Sites?

As with the previous map, I used a minimum spanning tree as the skeleton network, then added links to form loops for redundancy. I rerouted segments that would have run through the ocean and created ferry routes to the Galápagos Islands, Malpelo and Fernando de Noronha. Iguazú Falls also gets two stations, one on each side of the Argentina–Brazil border, connected by a border transfer. Each line name draws on South American culture and nature:<br>
🔴 Qhapaq Ñan Line: the Inca road network along the Andes<br>
🟢 Amazonas Line: across the rainforest to the Atlantic<br>
🟡 Jaguar Line: named after the big cat found across the Amazon, Pantanal and Cerrado<br>
🔵 Bossa Nova Line: named after Brazil’s music genre, serving Brazilian stops<br>
🟣 Gaucho Line: named after the South American cowboys of the pampas and Patagonia<br>
⛴️ Darwin Ferries: following the HMS Beagle’s stops at Fernando de Noronha and the Galápagos<br>

![Day 2](Day%202/Day%202.png)

Data Source: [UNESCO World Heritage List](https://whc.unesco.org/en/interactive-map/)
Picture Source: [Samuel Quek/Unsplash](https://unsplash.com/photos/ancient-inca-citadel-of-machu-picchu-in-peru-iMWos9jS3oE)


### Day 1: Points

For Day 1's theme on Points, I plotted all 6,079 surviving Ordnance Survey trig pillars in Great Britain (as of 2018), coloured from dim amber to bright white based on their elevation.

Trig pillars are the concrete columns found on hilltops across Britain. They were built between 1936 and 1962 for the Retriangulation of Great Britain, the survey that established the framework behind the National Grid still used on Ordnance Survey maps today.

![Day 1](Day%201/Day%201_edited.png)

Data Source: [OS Triangulation Stations](https://github.com/philmikejones/trigpoints), [Land Boundaries](https://www.naturalearthdata.com/downloads/10m-physical-vectors/)
