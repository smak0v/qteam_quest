# QUESTS API Endpoints

- ```/api/quests/``` (GET)

    Returns info about all quests.

- ```/api/quests/``` (POST)

    ```
    name (required)
    phone (required)
    description (default '')
    location (required)
    x_coordinate (required)
    y_coordinate (required)
    coever_image (defaul None)
    photo (default None)
    ```

    Create a quest.

    Only for authorized staff users.

- ```/api/quests/quest_pk/``` (GET)

    Returns info about the quest by it primary key.

    If the request contains user authorization token - returns information about the user's subscription to 
    this quest.

- ```/api/quests/quest_pk/``` (DELETE)

    Delete quest by it primary key.

    Only for authorized staff users.

- ```/api/quests/quest_pk/``` (PUT, PATCH)

    ```
    name
    phone
    description
    location
    x_cordinate
    y_coordinate
    coever_image
    photo
    ```

    Update quest by it primary key.

    Only for authorized staff users.

- ```/api/quests/quest_pk/subscribers/``` (GET)

    Returns info about all quest`s subscribers.

- ```/api/quests/quest_pk/subscribe/``` (POST)

    ```
    user (required)
    quest (required)
    ```

    Subscribe ```user``` to ```quest``` if subscription does not exist.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    ```user``` - must be existing and authorized user;

    ```quest``` - must be existing quest.

- ```/api/quests/quest_pk/unsubscribe/``` (DELETE)

    ```
    user (required)
    quest (required)
    ```

    Unsubscribe ```user``` from ```quest```.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

     ### Validators

    ```user``` - must be existing and authorized user;

    ```quest``` - must be existing quest.

- ```/api/quests/quest_pk/games/``` (GET)

    Returns list of games and their count by quest.

- ```/api/quests/quest_pk/comments/``` (GET)

    Return all comments and their count from users for quest by it primary key.

- ```/api/quests/quest_pk/comments/``` (POST)

    ```
    quest (required)
    user (required)
    text (required)
    timestamp
    scores (required (1 or 2 or 3 or 4 or 5))
    ```

    Add comment for a quest. 

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```scores``` - must be from 1 to 5;

    - ```quest``` - must be existing quest;

    - ```user``` - must be existing and authorized user.
