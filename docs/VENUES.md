# VENUES API Endpoints

- ```/api/venues/``` (GET)

    Returns info about all venues.
    
- ```/api/venues/``` (POST)

    ```
    name (required)
    location (required)
    x_coordinate (required)
    y_coordinate (required)
    coever_image (defaul None)
    rating (default 0.00)
    ```
  
    Create a venue.
    
- ```/api/venues/venue_pk/``` (GET)

    Returns info about the venue by it primary key.
    
    If the request contains a user authorization token - returns information about the user's subscription to 
    this venue.
    
- ```/api/venues/venue_pk/subscribers/``` (GET)

    Returns info about all venue`s subscribers.
    
- ```/api/venues/venue_pk/subscribe/``` (POST)

    ```
    user (required)
    venue (required)
    ```

    Subscribe ```user``` to ```venue``` if subscription does not exist.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    ```user``` - must be existing and authorized user;

    ```venue``` - must be existing venue.

- ```/api/venues/venue_pk/unsubscribe/``` (DELETE)

    ```
    user (required)
    venue (required)
    ```

    Unsubscribe ```user``` from ```venue```.
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
- ```/api/venues/venue_pk/games/``` (GET)

    Returns list of games and their count by venue.

- ```/api/venue/venue_pk/``` (DELETE)

    Delete venue by it primary key.
    
- ```/api/venue/venue_pk/``` (PUT, PATCH)

    ```
    name
    location
    c_cordinate
    y_coordinate
    coever_image
    rating
    ```
  
    Update venue by it primary key.
    
- ```/api/venues/venue_pk/comments/``` (GET)

    Return all comments and their count from users for venue by it primary key.
    
- ```/api/venues/venue_pk/comments/``` (POST)

    ```
    venue (required)
    user (required)
    text (required)
    timestamp
    scores (required (1 or 2 or 3 or 4 or 5))
    ```
  
    Add comment for a venue. 
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
    ### Validators
    
    - ```scores``` - must be from 1 to 5;
    
    - ```venue``` - must be existing venue;
    
    - ```user``` - must be existing and authorized user.