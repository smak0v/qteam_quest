# GAMES API Endpoints

- ```/api/games/``` (GET)

    Returns info about all active games.

- ```/api/game/?date=yyyy-mm-dd``` (GET)

    Returns all active games and info for them for date from URL argument.

- ```/api/games/``` (POST)

    ```
    title (required)
    description (default '')
    genre (required)
    cover_image (default None)
    photo (default None)
    timespan (required)
    duration (required)
    quest (reuqired)
    payment_method (ONLINE, default ONLINE)
    price (required)
    currency (RUB, default RUB)
    level (1, 2, 3, 4 or 5, default 1)
    refund_money_if_game_is_cancelled (default False)
    refundable_days (default 0)
    min_players_count (required)
    max_players_count (required)
    registration_available (default True)
    cancel (default False)
    ```

    Create a game.

    Only for authorized staff users.

    ### Validators

    - ```price``` - must be positive integer or decimal;

    - ```duration``` - must be positive integer;

    - ```quest``` - must be existing quest.

- ```/api/games/game_pk/``` (GET)

    Returns info about a game by it primary key.

    If the request contains a user authorization token - also returns:

    - a flag of whether the game passed or not;

    - number of seats purchased for this game;
    
    - reserved places count for user from request.

- ```/api/games/game_pk/``` (DELETE)

    Delete a game by it primary key.

- ```/api/games/game_pk/``` (PUT, PATCH)

    ```
    title
    description
    genre
    cover_image
    photo
    timespan
    duration
    quest
    payment_method
    price
    currency
    level
    refund_money_if_game_is_cancelled
    refundable_days
    min_players_count
    max_players_count
    registration_available
    cancel
    ```

    Update a game by it primary key.

    ### Validators

    - ```price``` - must be positive integer or decimal;

    - ```duration``` - must be positive integer;

    - ```quest``` - must be existing quest.

- ```/api/games/game_pk/comments/``` (GET)

    Returns all comments and their count for a game by game primary key.

- ```/api/games/game_pk/comments/``` (POST)

    ```
    user (required)
    game (required)
    timestamp
    text (required)
    ```

    Add comment for a game. 

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```user``` - must be existing and authorized user;

    - ```game``` - must be existing game.

- ```/api/games/game_pk/reserve_place/``` (POST)

    ```
    user (required)
    game (required)
    ```

    Reserve one temporary place (will be saved only for 5 minutes) for a game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```user``` - must be the real user and be equal to user from request;

    - ```game``` - must be the real game and must be equal for a game from request;

    - ```game``` - must be held in the future;

    - there should be enough free places in the game.

- ```/api/games/game_pk/unreserve_place/``` (DELETE)

    Unreserve one place for user from request on game from request url.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```game_pk``` - must be the real game primary key;

    - authorized user must have at least one reserved place for the game.

- ```/api/games/game_pk/book_places/``` (GET)

    Book places for the game (on ```Бронировать``` button click).

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/games/game_pk/team/``` (GET)

    Returns info about team for a game (id and game info).

- ```/api/games/game_pk/players/``` (GET)

    Returns info about all users for a game.

    ### Validators

    - ```game_pk``` from the url must belong to an existing game.

- ```/api/games/game_pk/players/``` (POST)

    ```
    user (required)
    title
    ```

    Register user for a game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```user``` - must be existing user;

    - ```game``` - must be existing game.

- ```/api/games/game_pk/players/player_pk/``` (GET)

    Returns info about registered user for a game.

- ```/api/games/game_pk/players/player_pk/``` (DELETE)

    Delete user and all it`s reserved places for a game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```api/games/game_pk/places_status/``` (GET)

    Returns free places count and occupied places count (by user from request) for a game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```api/games/game_pk/evaluate_player/``` (POST)

    ```
    game (required)
    appraiser (required)
    ranked_user (required)
    game_level (required, default 1)
    enjoyed_playing (required, default 1)
    ```

    Evaluate one player ```(ranked_user)``` by another user ```(appraiser)```.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```game_level``` - must be in the range 1 to 10;

    - ```enjoyed_playing``` - must be in the range 1 to 10;

    - ```game``` must exists;

    - ```appraiser``` should not be ```ranked_user```;

    - ```appraiser``` and ```ranked_user``` must participate in the ```game```.
