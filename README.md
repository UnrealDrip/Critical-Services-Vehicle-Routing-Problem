Vehicle Routing Problem in Critical Services Application
This project aims to solve the Vehicle Routing Problem in Critical Services using Genetic Algorithms to obtain fast solutions.

Datasets
There are 3 main datasets: Fixed, Mobile, and Mixed.

Fixed Dataset
The Fixed Dataset contains the locations of vehicles starting and ending at hospitals.

Mobile Dataset
The Mobile Dataset is the opposite of the Fixed Dataset, where the vehicle locations are random.

Mixed Dataset
The Mixed Dataset takes the best from both worlds, where 70% of vehicles are at random locations and 30% are at hospitals as found in research done by Plos One.

Chromosomes
The Chromosome Locations are at random and maintain the pickup locations before the drop-off locations.

Chromosomes are broken down in different ways:

Randomly breaking while maintaining order
Hub-based where the first vehicles are assigned to the first requests and so on
Breaking chromosomes depending on the distance between two pickups, the distance sum, and drop-off distance in a chromosome pair
Objectives
There are 4 objectives:

Total Arrival Time
Maximum Arrival Time
Total Wait Time
Maximum Wait Time
Status
As of now, the crossover and mutations still need to be done.

Data Generation
The generated data has not been provided for this project on the Github repository, but the data generators have been included.
