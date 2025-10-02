The goal of the HBnB project is to recreate a simple AirBnB website.
You'll be able to create an account, search places, make bookings and publish reviews. More options could be added later like payment for instance.

Please find below the Package Diagram, the Class Diagram and 4 Sequence Diagrams for a better understanding of the architecture as well as the information flow.

1- High-Level Package Diagram

The architecture is divided in 3 layers: the Presentation Layer, the Business Logic Layer and the Persistence Layer. There is also a Facade between the first two layers to simplify the system use.

- Presentation Layer: All the actions that an user can make on the platform (Services and API).

- Facade: Entry point of the system. Any API call goes through the Facade. Its goal is also to centralise, for instance one call can use many classes.
You can find in the diagram a non-exhaustive list of available functions.

- Business Logic Layer: Layer including the base classes of the system: User, Place, review and Amenity. Thanks to these classes we can make a basic platform where an user can create an account, list a place, publish review, and add amenities for instance.
Please note that many classes could be added later like Photos, Payment,... but this is just the base idea.

- Persistence Layer: Can fetch and send data from or to the DataBase.

Please find below the Package Diagram of the 3 Layers system. The relationship between the layers is dependency because layer depends on the layer below it until the DataBase.

![Package Diagram](Hbnb_Package_Diagram.png)

