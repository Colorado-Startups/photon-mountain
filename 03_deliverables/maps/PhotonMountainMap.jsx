import { useEffect, useRef, useState } from "react";

// Photon Mountain corridor: interactive map.
// Boundary along seven roads: CO-93/Broadway (west), Pearl St (Boulder closure),
// 28th St / US-36 (northeast), I-25 (link), Park Ave West + Broadway (Denver wrap), 6th Ave / US-6 (south).
// Traced to OSM centerlines (OSRM); straight stitches under 150 m at the
// US-36/Broadway junction (north Boulder) and at 6th & Speer (Denver).

const BOUNDARY = [[39.75714,-105.23518],[39.76057,-105.23363],[39.76241,-105.23331],[39.76397,-105.23361],[39.76987,-105.23632],[39.77099,-105.23649],[39.77205,-105.23635],[39.77335,-105.23571],[39.77585,-105.2335],[39.77894,-105.23178],[39.78023,-105.23146],[39.7828,-105.23142],[39.79225,-105.23035],[39.79356,-105.22972],[39.7987,-105.22587],[39.80004,-105.22506],[39.80142,-105.22461],[39.80826,-105.2233],[39.81159,-105.22185],[39.81328,-105.22166],[39.8219,-105.22167],[39.8227,-105.22173],[39.82369,-105.22203],[39.82441,-105.22246],[39.82527,-105.2233],[39.82766,-105.22659],[39.82845,-105.22733],[39.82977,-105.22796],[39.83275,-105.22845],[39.83387,-105.22877],[39.83712,-105.23046],[39.83822,-105.23123],[39.84043,-105.23388],[39.84127,-105.23453],[39.84215,-105.23491],[39.84357,-105.23502],[39.85444,-105.23238],[39.85538,-105.23234],[39.85618,-105.2325],[39.85764,-105.23333],[39.8652,-105.23985],[39.8663,-105.24049],[39.8681,-105.24104],[39.90547,-105.2411],[39.9084,-105.24095],[39.90969,-105.24068],[39.91148,-105.24003],[39.92446,-105.2348],[39.9262,-105.2344],[39.92731,-105.23441],[39.9284,-105.23462],[39.93417,-105.23652],[39.93522,-105.23671],[39.93683,-105.23666],[39.94059,-105.23582],[39.94202,-105.23565],[39.94348,-105.23582],[39.94568,-105.23654],[39.94687,-105.23654],[39.94797,-105.23601],[39.95042,-105.23385],[39.95374,-105.23191],[39.95464,-105.23145],[39.95598,-105.23131],[39.95685,-105.23159],[39.95749,-105.23202],[39.96044,-105.23571],[39.96155,-105.23666],[39.96301,-105.23744],[39.96444,-105.23782],[39.96593,-105.23785],[39.97039,-105.23693],[39.97122,-105.23707],[39.97195,-105.23748],[39.97794,-105.24305],[39.98649,-105.25065],[39.98726,-105.25169],[39.989,-105.25525],[39.99004,-105.25647],[40.00229,-105.26512],[40.00288,-105.26599],[40.00341,-105.26753],[40.00389,-105.26851],[40.00747,-105.27476],[40.01051,-105.27686],[40.01358,-105.2785],[40.01594,-105.2793],[40.01876,-105.2796],[40.01925,-105.27332],[40.023745,-105.25123],[40.023675,-105.250583],[40.023013,-105.248555],[40.022882,-105.246414],[40.022708,-105.245737],[40.02115,-105.2447],[40.01929,-105.24392],[40.01573,-105.24149],[40.0147,-105.24092],[40.01287,-105.2405],[40.01021,-105.24049],[40.00884,-105.23997],[40.00077,-105.23342],[39.99717,-105.23172],[39.98871,-105.23178],[39.98519,-105.23238],[39.98456,-105.2322],[39.98405,-105.2317],[39.98365,-105.23075],[39.98347,-105.22836],[39.98296,-105.22702],[39.97425,-105.20816],[39.95829,-105.16715],[39.95631,-105.1624],[39.95438,-105.15929],[39.94858,-105.15165],[39.93951,-105.13766],[39.93852,-105.13578],[39.93196,-105.12134],[39.93064,-105.1192],[39.92528,-105.11231],[39.92361,-105.10988],[39.92234,-105.10739],[39.9173,-105.09641],[39.91566,-105.09331],[39.9147,-105.09193],[39.91349,-105.09051],[39.9111,-105.08842],[39.89997,-105.0806],[39.89464,-105.07748],[39.89286,-105.07626],[39.87193,-105.06083],[39.8704,-105.05994],[39.85896,-105.05462],[39.85625,-105.05311],[39.854,-105.05154],[39.85105,-105.04895],[39.84176,-105.03928],[39.84067,-105.03776],[39.83976,-105.03623],[39.83876,-105.03411],[39.83819,-105.03256],[39.82805,-104.99715],[39.82767,-104.99541],[39.82751,-104.99399],[39.82747,-104.98712],[39.82725,-104.98508],[39.82689,-104.98432],[39.82633,-104.9838],[39.82571,-104.98354],[39.82481,-104.98344],[39.82353,-104.98349],[39.82181,-104.98407],[39.82081,-104.98421],[39.81857,-104.98345],[39.81705,-104.98324],[39.80596,-104.98338],[39.80388,-104.98393],[39.80223,-104.98474],[39.80184,-104.98527],[39.80184,-104.98578],[39.79886,-104.98649],[39.79586,-104.98774],[39.78981,-104.98916],[39.78907,-104.98889],[39.77515,-104.98924],[39.7727,-104.98978],[39.77106,-104.99069],[39.76958,-104.99211],[39.76836,-104.99406],[39.76866,-104.99508],[39.76831,-104.99495],[39.76115,-104.99496],[39.76045,-104.99478],[39.75961,-104.99421],[39.7586,-104.99318],[39.75717,-104.99292],[39.75674,-104.99264],[39.75266,-104.98739],[39.72666,-104.98743],[39.72564,-104.98721],[39.72573,-105.00821],[39.72523,-105.01847],[39.72571,-105.02633],[39.72554,-105.03114],[39.72567,-105.03427],[39.72581,-105.05373],[39.72542,-105.1363],[39.72541,-105.1806],[39.72512,-105.19802],[39.72519,-105.19929],[39.72548,-105.2006],[39.72607,-105.20175],[39.72825,-105.20397],[39.7289,-105.20492],[39.72939,-105.20613],[39.73019,-105.2094],[39.73074,-105.21045],[39.73141,-105.21135],[39.74785,-105.22568],[39.74994,-105.22774],[39.75052,-105.22912],[39.75068,-105.2316],[39.75089,-105.23264],[39.75132,-105.23367],[39.75257,-105.23533],[39.75377,-105.23616],[39.75527,-105.23639],[39.75597,-105.23622],[39.75714,-105.23518]];

const CITYLABELS = [{"name": "BOULDER", "ll": [40.0005, -105.2605]}, {"name": "GOLDEN", "ll": [39.742, -105.212]}, {"name": "DENVER", "ll": [39.756, -105.025]}, {"name": "ARVADA", "ll": [39.815, -105.13]}];

const MARKERS = [{"name": "Colorado State Capitol", "ll": [39.73917, -104.98472], "cat": "state", "note": "Government Hall. 200 E Colfax Ave. Faces Civic Center Park; sits two blocks east of the Broadway line, counted as a corridor site.", "inside": true}, {"name": "Denver City & County Building", "ll": [39.7393, -104.9918], "cat": "muni", "note": "Government Hall. Denver's city hall, 1437 Bannock St, at the west end of Civic Center Park.", "inside": true}, {"name": "Boulder Municipal Building", "ll": [40.015523, -105.279164], "cat": "muni", "note": "Government Hall. Penfield Tate II Municipal Building, 1777 Broadway at Canyon. Sits directly on the Broadway boundary line; counted as a corridor site.", "inside": true}, {"name": "Golden City Hall", "ll": [39.7556, -105.2219], "cat": "muni", "note": "Government Hall. 911 10th St, downtown Golden. (Address-anchored.)", "inside": true}, {"name": "Arvada City Hall", "ll": [39.8028, -105.0875], "cat": "muni", "note": "Government Hall. 8101 Ralston Rd, near Olde Town Arvada.", "inside": true}, {"name": "Downtown Boulder Station", "ll": [40.01736, -105.27654], "cat": "transit", "note": "Transit Station. RTD bus hub, 1800 14th St at Walnut. (RTD stop location.)", "inside": true}, {"name": "Boulder Junction at Depot Square", "ll": [40.0243, -105.25146], "cat": "transit", "note": "Transit Station. Boulder's rail-ready hub, 3175 Pearl Pkwy at Depot Square; Flatiron Flyer BRT today, designated Boulder stop for the proposed Colorado Connector (CoCo) train. Immediately north of the Pearl Pkwy line; counted as a corridor station.", "inside": true}, {"name": "Denver Union Station", "ll": [39.75278, -105.00011], "cat": "transit", "note": "Transit Station. Denver's central rail hub, 1701 Wynkoop St; eastern end of the W Line and CoCo's Denver terminal.", "inside": true}, {"name": "Civic Center Station", "ll": [39.74107, -104.98702], "cat": "transit", "note": "Transit Station. RTD's downtown bus terminal, 1560 Broadway; south anchor of the 16th St corridor. In the Broadway-Lincoln block, steps east of the Broadway line; counted as a corridor station.", "inside": true}, {"name": "JeffCo Gov't Center-Golden Station", "ll": [39.72639, -105.20111], "cat": "transit", "note": "Transit Station. Western end of the W Line, 605 Johnson Rd; Golden FlexRide. About 60 m inside the US-6 line.", "inside": true}, {"name": "Olde Town Arvada Station", "ll": [39.79897, -105.07898], "cat": "transit", "note": "Transit Station. G Line commuter rail, 5595 Olde Wadsworth Blvd; Arvada's hub.", "inside": true}, {"name": "CU Boulder (Old Main)", "ll": [40.00915, -105.2721], "cat": "university", "note": "University Campus. University of Colorado Boulder, anchored at Old Main (1876), 1600 Pleasant St: the campus flagship and founding building, home of the CU Heritage Center. (Address-anchored.)", "inside": true}, {"name": "Venture Partners at CU Boulder", "ll": [40.0217, -105.24073], "cat": "statefac", "note": "Innovation Campus. The University of Colorado's commercialization arm, serving the Boulder, Colorado Springs, and Denver campuses (Anschutz biosciences work with CU Innovations). 4845 Pearl East Circle, Suite 300. About 400 m east of the Foothills Pkwy line, near COQI; counted as a corridor site. (Exact pin.)", "inside": true}, {"name": "CU Denver (CU Denver Building)", "ll": [39.7476, -105.0033], "cat": "university", "note": "University Campus. University of Colorado Denver; CU Denver Building, 1250 14th St at Lawrence. Also the innovation anchor: CityCenter, CU Denver's innovation and partnership portal, is at the 14th and Lawrence corner, and the building houses the Smart Futures Lab, CU Denver's smart-city startup incubator and accelerator (EDA grant funded). (Address-anchored.)", "inside": true}, {"name": "Colorado School of Mines (Guggenheim Hall)", "ll": [39.75085, -105.22255], "cat": "university", "note": "University Campus. Guggenheim Hall (1906), 1500 Illinois St, Golden. Also the tech transfer anchor: the Mines Research and Technology Transfer office is Guggenheim Suite 314. Quantum engineering program campus-wide.", "inside": true}, {"name": "MSU Denver (Jordan Student Success Building)", "ll": [39.74573, -105.00762], "cat": "university", "note": "University Campus. Metropolitan State University of Denver, anchored at the Jordan Student Success Building, 890 Auraria Pkwy: the university's flagship administration and student services building. (OSM building centroid.)", "inside": true}, {"name": "NIST Boulder", "ll": [39.99306, -105.26389], "cat": "natlab", "note": "National Lab. NIST Boulder campus, 325 Broadway: atomic clocks, optical frequency combs, quantum measurement. The Precision Measurement Laboratory (Building 81, the BMF cleanroom), Building 1 (the 1954 Radio Building), and the Communications Technology Laboratory (Building 3) carry their own dots; the 206-acre Department of Commerce campus also hosts NOAA and NTIA. Also on campus, per the National Academies 2023 assessment: semiconductor-reliability electron microscopy (Building 2) and spintronics research toward low-power memory (Building 24, slated for replacement). Immediately west of the Broadway line; counted as a corridor institution.", "inside": true}, {"name": "NIST Precision Measurement Laboratory (BMF)", "ll": [39.994244, -105.263614], "cat": "natlab", "note": "National Lab. Building 81 on the NIST Boulder campus, now the Katherine Gebbie Laboratory: a 283,000 sq ft precision measurement building housing the Boulder Microfabrication Facility, an operating 18,000 sq ft ISO 5 cleanroom with integrated-photonics tooling; cleanroom opened 2012. West of the Broadway line with the rest of the campus; counted as a corridor site. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NIST Building 1 (Radio Building)", "ll": [39.995038, -105.26283], "cat": "natlab", "note": "National Lab. The Central Radio Propagation Laboratory building, dedicated by President Eisenhower in 1954 and eligible for the National Register; historic home of the atomic clock work. Today it also houses NTIA's Institute for Telecommunication Sciences, the third federal lab on the Department of Commerce campus (radio spectrum and telecommunications research). Its labs include microwave photonics (quantum entanglement of microresonators, the Physics World 2021 Breakthrough of the Year), quantum sensor fabrication and packaging, and NIST's optical fiber power calibration service, used by industry and defense calibration labs worldwide (National Academies 2023 assessment). West of the Broadway line with the campus; counted as a corridor site. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NIST Communications Technology Laboratory (Building 3)", "ll": [39.991796, -105.264663], "cat": "natlab", "note": "National Lab. CTL, Building 3, renovated and reopened 2018: advanced communications metrology, home of the 5G Coexistence Testbed measuring millimeter-wave, Wi-Fi, and IoT spectrum sharing in specialized anechoic and reverberation chambers. West of the Broadway line with the campus; counted as a corridor site. (OSM building centroid; program per the National Academies 2023 facilities assessment.)", "inside": true, "bldg": true}, {"name": "NOAA Boulder (David Skaggs Research Center)", "ll": [39.99162, -105.26119], "cat": "natlab", "note": "National Lab. NOAA research laboratories, 325 Broadway; immediately west of the Broadway line, counted as a corridor institution.", "inside": true}, {"name": "NLR, South Table Mountain campus", "ll": [39.7406, -105.1697], "cat": "natlab", "note": "National Lab. National Laboratory of the Rockies (formerly NREL; renamed Dec 2025), 15013 Denver West Pkwy, Golden; 327 acres, 17 buildings, per NLR. Flagship lab buildings ESIF and SERF carry their own dots. Also on campus: the net-zero Research Support Facility offices and the Innovation and Entrepreneurship Center, which runs energy-startup programs including the Wells Fargo Innovation Incubator (IN2). The EMAPS building under construction on the east side of campus carries its own dot.", "inside": true}, {"name": "NLR Energy Systems Integration Facility (ESIF)", "ll": [39.74262, -105.17028], "cat": "natlab", "note": "National Lab. ESIF, on NLR's South Table Mountain campus: 185,000 sq ft for megawatt-scale grid integration testing, 15 partner-accessible laboratories, and the lab's high-performance computing data center, per NLR. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Solar Energy Research Facility (SERF)", "ll": [39.74176, -105.1731], "cat": "natlab", "note": "National Lab. SERF, on NLR's South Table Mountain campus: photovoltaics and basic energy sciences; semiconductor materials for high-efficiency solar cells, prototype cell fabrication, and cell and module performance characterization. The corridor's light-as-energy research anchor. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Research and Innovation Laboratory (RAIL)", "ll": [39.7403, -105.1737], "cat": "natlab", "note": "National Lab. RAIL, on NLR's South Table Mountain campus just west of the Café: 15,700 sq ft (per NLR) of flexible wet-lab space opened May 2023, the campus's first new lab building since 2013; plastics upcycling, next-generation batteries, and advanced energy materials. (Placed from the NLR campus map against OSM building anchors; approximate.)", "inside": true, "bldg": true}, {"name": "NLR Science and Technology Facility (S&TF)", "ll": [39.742211, -105.171638], "cat": "natlab", "note": "National Lab. S&TF, built 2006: photovoltaics and advanced materials science labs. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Solar Radiation Research Laboratory (SRRL)", "ll": [39.74241, -105.178475], "cat": "natlab", "note": "National Lab. SRRL, on the South Table Mountain mesa: continuous solar irradiance measurement and reference radiometer instrumentation; one of the longest-running solar resource records in the country. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR High-Flux Solar Furnace", "ll": [39.742785, -105.178329], "cat": "natlab", "note": "National Lab. Concentrating solar furnace focusing sunlight for high-temperature materials and thermochemical research. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Solar Industrial Mesa Test Area (SIMTA)", "ll": [39.743074, -105.178906], "cat": "natlab", "note": "National Lab. Outdoor solar test area on the mesa top. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Outdoor Test Facility (OTF)", "ll": [39.740541, -105.177836], "cat": "natlab", "note": "National Lab. Outdoor photovoltaic module testing and performance characterization. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR Thermal Test Facility (TTF)", "ll": [39.740664, -105.179012], "cat": "natlab", "note": "National Lab. TTF, on NLR's South Table Mountain campus: building energy efficiency, HVAC, and thermal systems research, the cooling side of the energy story that data centers depend on. (OSM building centroid.)", "inside": true, "bldg": true}, {"name": "NLR EMAPS (under construction)", "ll": [39.742, -105.1682], "cat": "natlab", "note": "National Lab. Energy Materials and Processing at Scale: 129,000 sq ft, $224M lab and high-bay pilot facility for scaling energy materials from lab to market; broke ground Sept 2024, topped out Aug 2025, completion expected 2027. A horizon item, not operating today. (Sq ft per the design-build team's topping-out release; NLR's groundbreaking release said 127,000. East side of campus per NLR release; approximate, pin welcome.)", "inside": true, "bldg": true}, {"name": "South Table Mountain Energy Park (STEP)", "ll": [39.7345, -105.1685], "cat": "statefac", "note": "Innovation Campus. NLR-managed commercialization park on the 26-building former Camp George West section just south of the main campus; DOE took possession Jan 2023, renovation underway. Planned home of NLR's Innovation and Entrepreneurship Center and the Net Zero World Action Center; startups are intended to graduate from STEP into the adjacent Glo Park. A horizon item, not fully operating today. (Approximate, campus extent; pin welcome.)", "inside": true}, {"name": "NLR Flatirons Campus", "ll": [39.9132, -105.2268], "cat": "natlab", "note": "National Lab. NLR Flatirons Campus, 19001 W 119th Ave: 305 acres per NLR, home of the ARIES integrated-energy-systems platform (grid, storage, hydrogen, solar). Wind turbine and water-power test facilities are on site (formerly the National Wind Technology Center); noted for completeness, not the corridor focus. The Control Center carries its own dot. Part of NLR (formerly NREL). (Campus dot at the main building cluster, OSM anchors.)", "inside": true}, {"name": "NLR Flatirons Control Center", "ll": [39.9133, -105.2245], "cat": "natlab", "note": "National Lab. The Flatirons Campus's control hub, delivered December 2024 per builder Mortenson: 8,000 sq ft with a real-time control room and data center for ARIES grid-scale experiments, interconnected with ESIF on the South Table Mountain campus; supports DOE's Integrated Electrical Systems at Scale initiative. (Sited just north of the main road, east of the 5 MW dynamometer, per Mortenson and 360 Engineering; approximate.)", "inside": true, "bldg": true}, {"name": "NCAR Mesa Laboratory", "ll": [39.97806, -105.27472], "cat": "natlab", "note": "National Lab. NSF FFRDC for atmospheric science, 1850 Table Mesa Dr. Operating but under NSF restructuring review (announced Dec 2025-Jan 2026). 2 km southwest of the Broadway line; counted as a corridor institution.", "inside": true}, {"name": "USGS Geologic Hazards / NEIC", "ll": [39.7493, -105.2212], "cat": "natlab", "note": "National Lab. Includes the National Earthquake Information Center, 1711 Illinois St, on the Mines campus.", "inside": true}, {"name": "JILA", "ll": [40.007265, -105.268599], "cat": "univlab", "note": "University Lab. Joint NIST + CU institute, 440 UCB; light science and precision measurement, home of Nobel-recognized work in laser physics and ultracold atoms. The JILA tower sits attached to Duane Physics' southwest side; Duane carries its own dot. (OSM building centroid; corrected from an address-anchored pin that landed on the CIRES building.)", "inside": true}, {"name": "Duane Physics and Astrophysics", "ll": [40.007967, -105.267543], "cat": "univlab", "note": "University Lab. CU Boulder's physics complex on main campus: quantum optics, atomic-molecular-optical physics, and condensed matter labs. Attached to JILA on its west side; separate building and address, so separate dots. (OSM building centroid.)", "inside": true}, {"name": "Discovery Learning Center (NCF)", "ll": [40.0075536, -105.2617944], "cat": "univlab", "note": "University Lab. Gallogly Discovery Learning Center, 1095 Regent Dr, part of CU's Engineering Center complex. Named lab: the Nanomaterials Characterization Facility (NCF), the college's shared nanoscale characterization suite, serving 100-plus researchers. ECEE's photonics and quantum engineering groups sit in the adjacent Engineering Center. (OSM building footprint.)", "inside": true}, {"name": "LASP Space Science Building", "ll": [40.00943, -105.24692], "cat": "univlab", "note": "University Lab. Laboratory for Atmospheric and Space Physics, 3665 Discovery Dr, CU East Campus; space instrumentation and optics. (Building-centered via georeferenced aerial.)", "inside": true}, {"name": "LASP Space Technology Research Center", "ll": [40.009054, -105.247428], "cat": "univlab", "note": "University Lab. LASP's instrument and spacecraft development building, 1234 Innovation Dr, CU East Campus: flight hardware built, integrated, and tested here. Sister building to the Space Science Building. (OSM building centroid.)", "inside": true}, {"name": "Colorado Quantum Incubator (COQI)", "ll": [40.02005, -105.22131], "cat": "statefac", "note": "Innovation Campus. CU Boulder / CSU / Mines / Elevate Quantum incubator, Flatiron Park, east Boulder; launched Jan 2025. About 1.9 km east of the Foothills line; counted as a corridor site. (Exact pin.)", "inside": true}, {"name": "IRISS / Smead Aerospace labs", "ll": [40.01018, -105.24377], "cat": "univlab", "note": "University Lab. Smead Aerospace building, 3775 Discovery Dr, CU East Campus. Named labs: IRISS (Integrated Remote and In-Situ Sensing; the photonic-sensing tie), BioServe Space Technologies, CCAR (astrodynamics), RECUV (unmanned vehicles), AMReC (aerospace mechanics). (Building-centered via georeferenced aerial.)", "inside": true}, {"name": "Mines Quantum Engineering labs (CoorsTek Center)", "ll": [39.7505, -105.2221], "cat": "univlab", "note": "University Lab. CoorsTek Center for Applied Science and Engineering, 1523 Illinois St, Golden: quantum engineering lab and Class 1000 cleanroom in the basement (CK040), dilution refrigerators for solid-state qubits and quantum sensors; Physics department home. (Address-anchored; pin welcome.)", "inside": true}, {"name": "Colorado Fuel Cell Center", "ll": [39.7522, -105.2246], "cat": "univlab", "note": "University Lab. Mines energy research center, 1310 Maple St, Golden: solid oxide fuel cell and hydrogen research; its test facility feeds power to the campus grid. Mines and NLR also run the joint NEXUS energy initiative. (Address-anchored; pin welcome.)", "inside": true}, {"name": "MSU Denver Advanced Manufacturing labs (AES Building)", "ll": [39.74507, -105.00871], "cat": "univlab", "note": "University Lab. Aerospace and Engineering Sciences Building, 1449 7th St, Auraria campus. Named labs: the Advanced Manufacturing Sciences Institute (3D printing, laser cutting, CNC). York Space Systems' satellite production floor is in the building but private, not separately marked. (OSM building footprint.)", "inside": true}, {"name": "Quantum Commons PIC Fab (Elevate Quantum)", "ll": [39.86143, -105.20616], "cat": "fab", "note": "Fabrication Facility. The corridor's photonic-integrated-circuit fab: a 10,000 sq ft fabrication and cleanroom building for prototyping and low-volume manufacturing, coming online 2026 per Elevate Quantum; in build-out, not operating at volume. State-backed (EDA Tech Hub + HB24-1325 funded), on the 70-acre Mines-owned Quantum Commons campus, 18300 CO-72, Arvada. (Campus pin; building location within the campus pending, pin welcome.)", "inside": true}, {"name": "Quantum Commons Labs (open-access)", "ll": [39.8617, -105.206], "cat": "statefac", "note": "Innovation Campus. The first major building on the Quantum Commons campus, grand-opened August 2025: a renovated building carrying the campus's offices, coworking, and administration, per the Governor's office. The 17,000 sq ft of open-access quantum labs (solid-state and AMO modalities, with a Class IV laser lab in the construction scope) are the next phase; August 2025 reporting put them a few months out, and no opening notice had been found as of July 2026. Run by Elevate Quantum with Mines, CU Boulder, and CSU. (Georeferenced from current satellite imagery; approximate.)", "inside": true}, {"name": "Glo Park (Global Energy Park)", "ll": [39.7395, -105.1716], "cat": "statefac", "note": "Innovation Campus. State-championed energy research and commercialization campus; NexCore ground lease on the open state parcel immediately south-southwest of NLR's South Table Mountain campus, across Denver West Pkwy. In development; no street address yet. Location per project owner. Sits between NLR's campus and STEP, the DOE's commercialization park; the stated pipeline is startups graduating from STEP into Glo Park.", "inside": true}, {"name": "Beck Venture Center (Mines)", "ll": [39.75089, -105.21758], "cat": "statefac", "note": "Innovation Campus. Colorado School of Mines' startup incubator and accelerator, 1700 Washington Ave at 17th St, Golden; opened April 2024. 31,000 sq ft of coworking, event, and mentor space for Mines-connected founders; 57 startups incubating at its one-year mark, per the Mines newsroom. (OSM building centroid.)", "inside": true}, {"name": "SEEC (Sustainability, Energy & Environment Community)", "ll": [40.00982, -105.2417], "cat": "univlab", "note": "University Lab. Main building of the SEEC complex, 4001 Discovery Dr, CU East Campus: RASEI, CIRES, INSTAAR, ATOC, environmental engineering. (Building-centered via georeferenced aerial.)", "inside": true}, {"name": "SEEL: COSINC Nanofab + NQN", "ll": [40.00874, -105.24134], "cat": "fab", "note": "Fabrication Facility. Laboratory building of the SEEC complex, 4001 Discovery Dr, at Colorado Ave and Foothills Pkwy. Houses COSINC, CU's operating ISO 5/6 shared nanofab cleanroom. The National Quantum Nanofab (NQN), a $20M NSF national facility, is under development as a 3,600 sq ft addition on this building's east side, expanding COSINC; completion expected 2028-29, a horizon item, not operating today. (Building-centered via georeferenced aerial.)", "inside": true}];
const MSTYLE = {"state":["#ffd43b","#103a63"],"muni":["#ffffff","#103a63"],"transit":["#e8590c","#ffffff"],"university":["#a5d8ff","#1971c2"],"natlab":["#ffd43b","#f59f00"],"univlab":["#b2f2bb","#2f9e44"],"fab":["#99e9f2","#0c8599"],"statefac":["#eebefa","#9c36b5"]};





const OUTSIDE = [];

const CORNERS = [];

function loadLeaflet() {
  return new Promise((resolve, reject) => {
    if (window.L) return resolve(window.L);
    if (!document.querySelector('link[data-leaflet]')) {
      const css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css";
      css.setAttribute("data-leaflet", "1");
      document.head.appendChild(css);
    }
    const existing = document.querySelector('script[data-leaflet]');
    if (existing) {
      existing.addEventListener("load", () => resolve(window.L));
      existing.addEventListener("error", reject);
      return;
    }
    const s = document.createElement("script");
    s.src = "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js";
    s.setAttribute("data-leaflet", "1");
    s.onload = () => resolve(window.L);
    s.onerror = reject;
    document.body.appendChild(s);
  });
}

export default function PhotonMountainMap() {
  const elRef = useRef(null);
  const mapRef = useRef(null);
  const polyRef = useRef(null);
  const [showFill, setShowFill] = useState(true);
  const [status, setStatus] = useState("loading"); // loading | ready | error

  useEffect(() => {
    let cancelled = false;
    const timer = setTimeout(() => {
      if (!window.L && !cancelled) setStatus("error");
    }, 8000);

    loadLeaflet()
      .then((L) => {
        if (cancelled || !elRef.current || mapRef.current) return;
        clearTimeout(timer);

        // permanent label styling
        if (!document.querySelector("style[data-pm]")) {
          const st = document.createElement("style");
          st.setAttribute("data-pm", "1");
          st.textContent =
            ".pm-lbl{background:transparent;border:none;box-shadow:none;color:#0b3d63;font-weight:800;font-size:13px;text-shadow:0 0 3px #fff,0 0 3px #fff,0 0 3px #fff;} .pm-city{background:transparent;border:none;box-shadow:none;color:#0b3d63;font-weight:800;font-size:15px;letter-spacing:2.5px;text-shadow:0 0 4px #fff,0 0 4px #fff;}";
          document.head.appendChild(st);
        }

        const map = L.map(elRef.current, { zoomControl: true, scrollWheelZoom: true });
        mapRef.current = map;

        const sat = L.tileLayer(
          "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
          { maxZoom: 19, attribution: "Imagery &copy; Esri, Maxar, Earthstar Geographics" }
        ).addTo(map);
        const voyager = L.tileLayer(
          "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
          { subdomains: "abcd", maxZoom: 20, attribution: "&copy; OpenStreetMap &copy; CARTO" }
        );
        const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution: "&copy; OpenStreetMap contributors",
        });
        L.control
          .layers(
            { Satellite: sat, "Streets (clean)": voyager, OpenStreetMap: osm },
            null,
            { position: "topright" }
          )
          .addTo(map);

        const poly = L.polygon(BOUNDARY, {
          color: "#ff7a18",
          weight: 4,
          opacity: 1,
          fillColor: "#ffb24d",
          fillOpacity: 0.16,
          lineJoin: "round",
        }).addTo(map);
        polyRef.current = poly;
        map.fitBounds(poly.getBounds(), { padding: [30, 30] });

        CITYLABELS.forEach((a) => {
          L.tooltip({ permanent: true, direction: "center", className: "pm-city" })
            .setLatLng(a.ll)
            .setContent(a.name)
            .addTo(map);
        });

        const bldgLayer = L.layerGroup();
        MARKERS.forEach((p) => {
          const st = p.inside ? MSTYLE[p.cat] : ["#adb5bd", "#495057"];
          const mk = L.circleMarker(p.ll, {
            radius: 6,
            color: st[0],
            weight: p.cat === "transit" && p.inside ? 3 : 2,
            fillColor: st[1],
            fillOpacity: 1,
          }).bindPopup("<b>" + p.name + "</b><br>" + p.note);
          if (p.bldg) { mk.addTo(bldgLayer); } else { mk.addTo(map); }
        });
        const pmBldgVis = () => {
          if (map.getZoom() >= 14) {
            if (!map.hasLayer(bldgLayer)) bldgLayer.addTo(map);
          } else if (map.hasLayer(bldgLayer)) {
            map.removeLayer(bldgLayer);
          }
        };
        map.on("zoomend", pmBldgVis);
        pmBldgVis();

        OUTSIDE.forEach((o) => {
          L.circleMarker(o.ll, {
            radius: 6,
            color: "#8a8a8a",
            weight: 2,
            fillColor: "#ffffff",
            fillOpacity: 1,
            dashArray: "3",
          })
            .addTo(map)
            .bindPopup("<b>" + o.name + "</b><br>" + o.note);
        });

        CORNERS.forEach((c) => {
          L.circleMarker(c.ll, {
            radius: 4,
            color: "#e8590c",
            weight: 2,
            fillColor: "#ffffff",
            fillOpacity: 1,
          })
            .addTo(map)
            .bindPopup(c.t);
        });

        setStatus("ready");
        setTimeout(() => map.invalidateSize(), 250);
        const onResize = () => map.invalidateSize();
        window.addEventListener("resize", onResize);
        map._pmOnResize = onResize;
      })
      .catch(() => {
        if (!cancelled) setStatus("error");
      });

    return () => {
      cancelled = true;
      clearTimeout(timer);
      if (mapRef.current) {
        if (mapRef.current._pmOnResize) window.removeEventListener("resize", mapRef.current._pmOnResize);
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    if (polyRef.current) polyRef.current.setStyle({ fillOpacity: showFill ? 0.16 : 0 });
  }, [showFill, status]);

  const resetView = () => {
    if (mapRef.current && polyRef.current)
      mapRef.current.fitBounds(polyRef.current.getBounds(), { padding: [30, 30] });
  };

  const ui = {
    card: {
      background: "rgba(255,255,255,0.95)",
      borderRadius: 12,
      boxShadow: "0 2px 12px rgba(0,0,0,0.18)",
      fontFamily: "-apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif",
    },
  };

  return (
    <div style={{ position: "relative", width: "100%", height: "100vh", minHeight: 560, background: "#eef1f3" }}>
      <div ref={elRef} style={{ position: "absolute", inset: 0 }} />

      {/* title */}
      <div style={{ ...ui.card, position: "absolute", top: 14, left: 14, zIndex: 1000, padding: "12px 16px", maxWidth: 320 }}>
        <div style={{ fontSize: 16, fontWeight: 800, letterSpacing: 0.4, color: "#1a1a1a" }}>PHOTON MOUNTAIN</div>
        <div style={{ fontSize: 12, lineHeight: 1.45, color: "#444", marginTop: 4 }}>
          Corridor boundary along seven roads: CO‑93/Broadway → Pearl St / Pearl Pkwy → Foothills Pkwy → US‑36 → I‑25 → Park Ave / Park Ave West → Broadway → 6th Ave / US‑6, back to Golden.
        </div>
        <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
          <button
            onClick={() => setShowFill((v) => !v)}
            style={{ fontSize: 12, fontWeight: 600, padding: "6px 10px", borderRadius: 8, border: "1px solid #e0823f", background: showFill ? "#e8590c" : "#fff", color: showFill ? "#fff" : "#c2410c", cursor: "pointer" }}
          >
            {showFill ? "Shade: on" : "Shade: off"}
          </button>
          <button
            onClick={resetView}
            style={{ fontSize: 12, fontWeight: 600, padding: "6px 10px", borderRadius: 8, border: "1px solid #ccc", background: "#fff", color: "#333", cursor: "pointer" }}
          >
            Reset view
          </button>
        </div>
      </div>

      {/* legend */}
      <div style={{ ...ui.card, position: "absolute", bottom: 26, left: 14, zIndex: 1000, padding: "10px 14px", fontSize: 12, color: "#333" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 22, height: 0, borderTop: "4px solid #e8590c", display: "inline-block" }} /> Corridor boundary (roads)
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#103a63", border: "2px solid #fff", display: "inline-block" }} /> Government Hall
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#fff", border: "3px solid #e8590c", display: "inline-block" }} /> Transit Station
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#1971c2", border: "2px solid #a5d8ff", display: "inline-block" }} /> University Campus
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#f59f00", border: "2px solid #ffd43b", display: "inline-block" }} /> National Lab
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#2f9e44", border: "2px solid #b2f2bb", display: "inline-block" }} /> University Lab
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#0c8599", border: "2px solid #99e9f2", display: "inline-block" }} /> Fabrication Facility
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, margin: "3px 0" }}>
          <span style={{ width: 12, height: 12, borderRadius: "50%", background: "#9c36b5", border: "2px solid #eebefa", display: "inline-block" }} /> Innovation Campus
        </div>
        <div style={{ marginTop: 6, fontSize: 11, color: "#777", fontStyle: "italic" }}>Roads traced to OSM centerlines. Sites just off the line are counted as corridor sites by decision; each popup says so. The State Capitol wears a gold ring.</div>
      </div>

      {status === "loading" && (
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", zIndex: 900, color: "#555", fontFamily: "-apple-system, sans-serif" }}>
          Loading map…
        </div>
      )}

      {status === "error" && (
        <div style={{ position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", zIndex: 900, padding: 24, textAlign: "center", color: "#555", fontFamily: "-apple-system, sans-serif" }}>
          <div>
            <div style={{ fontWeight: 700, marginBottom: 6 }}>Map tiles couldn’t load in this preview.</div>
            <div style={{ fontSize: 13 }}>Open this artifact in a full browser tab and the live street basemap will render. The boundary and markers are all defined in this file.</div>
          </div>
        </div>
      )}
    </div>
  );
}
