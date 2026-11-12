# 30DayMapChallenge 2026

This is my contribution to the #30DayMapChallenge for November 2026.\
About the #30DayMapChallenge , check out <https://30daymapchallenge.com/> !

## Introduction

### About me

I am currently a Principal Geomatics Engineer at the Singapore Land Authority and hold an MSc in Urban Spatial Science from the Centre for Advanced Spatial Analysis (CASA), University College London (UCL). \
I specialise in Geographic Information Systems (GIS), Remote Sensing, Data Science, and Agent-Based Modelling. \
For opportunities or collaboration, I can be contacted via [LinkedIn](https://www.linkedin.com/in/james-tan-song-en-76b73418a/)

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
