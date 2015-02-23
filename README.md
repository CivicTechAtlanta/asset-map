This is a map of South Downtown Atlanta, created for [CodeAcross](http://www.codeforamerica.org/events/codeacross-2015/). Soon, the map will have a home on [southdowntown.org](http://www.southdowntown.org/).

##Data and sources: 

* South Downtown polygon
* MARTA train stops, [Atlanta Regional Commission](http://documents.atlantaregional.com/GISdocs/rs_Marta_Rail_and_Stations_07.kmz)
* Historical markers, [The Historical Marker Database](http://www.hmdb.org/CountiesGPXList.asp)
* Landmarks, [City of Atlanta](http://gis.atlantaga.gov/apps/gislayers/download/)
* Aerial survey, 1949, [Georgia State University](http://digitalcollections.library.gsu.edu/cdm/ref/collection/atlaerial/id/134)
* Government buildings, [Foursquare](https://developer.foursquare.com/docs/explore#req=venues/categories)
* Entertainment, [Foursquare](https://developer.foursquare.com/docs/explore#req=venues/categories)
* Residential Building, [Foursquare](https://developer.foursquare.com/docs/explore#req=venues/categories)
* Food, [Foursquare](https://developer.foursquare.com/docs/explore#req=venues/categories)
* Art
* Community assets
* Vacant properties 
* Parcels, [Fulton County Board of Assessors](http://www.qpublic.net/ga/fulton/)
* Neighborhood Profile, [City of Atlanta](http://www.atlantaga.gov/modules/showdocument.aspx?documentid=7903)
* Population Density, [United States Census Bureau](http://factfinder.census.gov/)

##Possible Foursquare category additions:


* Neighborhood: 4f2a25ac4b909258e854f55f
* Southern / Soul Food Restaurant: 4bf58dd8d48988d14f941735
* Other Great Outdoors: 4bf58dd8d48988d162941735
* Salon / Barbershop: 4bf58dd8d48988d110951735
* Courthouse: 4bf58dd8d48988d12b941735
* Building: 4bf58dd8d48988d130941735
* Plaza: 4bf58dd8d48988d164941735
* Food Truck: 4bf58dd8d48988d1cb941735
* Cosmetics Shop: 4bf58dd8d48988d10c951735
* Indian Restaurant: 4bf58dd8d48988d10f941735
* Pizza Place: 4bf58dd8d48988d1ca941735
* Office: 4bf58dd8d48988d124941735
* Police Station: 4bf58dd8d48988d12e941735
* Gym: 4bf58dd8d48988d176941735
* Parking: 4c38df4de52ce0d596b336e1
* Internet Cafe: 4bf58dd8d48988d1f0941735
* Non-Profit: 50328a8e91d4c4b30a586d6c
* Convenience Store: 4d954b0ea243a5684a65b473

##Future Goals:

* Add more layers
* Make vacancy data more clear (it currently seems like whole buildings are vacant that aren't)
* Create separate maps for different audiences
* Add to South Downtown website

##Some possible ways to narrow the map for different audiences

* Real estate developers
* Advocacy (city planning, decision-makers, etc.)
* Visitors

##Potential Additions:

* Population density and demographics
* Zoning
* Parking (lots, decks, street)
* Use parcel layer to shade parcels based on data (use, ownership, etc.)
* Historical uses (esp. for vacancies)
* Tax (TAD?)
* More transit
	* Bus stops (MARTA and regional) and/or routes
	* Greyhound
	* Bike lanes & routes
	* Streetcar
	* Map usage
* Infrastructure (plumbing, electrical, fiber)
* Social services
* Economic indicators
* Organizations and other social events, etc.
* Government use
* Security (GSU police, Fulton county police & sheriff, APD, gov't building security)
* Proximity to stuff outside South Downtown
* Ambassadors
* Future plans (building permits; future land use map)
* Events
* Previous property sales/prices
* Visitors to the area
* More landmarks
* Filming locations
* Retail
* Integrating other CodeAcross groups' efforts: storytelling, branding, participatory


##Collaborators

* John Mancini
* Kyle Kessler
* Rudy Goodwine
* Katie OConnell
* Darin Givens
* Jimmy Lo
* Janae Futrell
* Luigi Montanez
* Mollie Taylor
* Ethan Henderson
* Scott Henderson
* Bryan Lackey
* Matthew Jones
* John Crocker


##Stack

* Research, Cleaning, and Geocoding
	* [QGIS](http://www2.qgis.org/en/site/)
	* Ruby (see [https://github.com/codeforatlanta/csv_geocoder](https://github.com/codeforatlanta/csv_geocoder))
* Implementation
	* HTML, CSS, Javascript
	* [Leaflet](http://leafletjs.com/)
	* [leaflet-omnivore](https://github.com/mapbox/leaflet-omnivore)
	* [leaflet.shapefile](https://github.com/calvinmetcalf/leaflet.shapefile) & [shapefile-js](https://github.com/calvinmetcalf/shapefile-js)
	* jQuery (for Foursquare API integration)
	* [Foursquare API](https://developer.foursquare.com/)
	* [Font Awesome](http://fortawesome.github.io/Font-Awesome/)
	* [Leaflet.awesome-markers](https://github.com/lvoogdt/Leaflet.awesome-markers)
