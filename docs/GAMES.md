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

    Reserve one temporary place (will be saved only for 10 minutes) for a game.

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

- ```/api/games/game_pk/reserved_places_info/``` (GET)

    Get info about reserved places for user on the game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Response example

    ```json
    {
      "occupied_places_count": 3,
      "summa": 600,
      "discount": 0,
      "is_coupon": true
    }
    ```
  
- ```/api/games/game_pk/payment_token/``` (POST)

    ```
    code
    game_id (required)
    ```

    Create payment for user on the game and store it. Returns Yandex payment token for web-widget initialization.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```code``` - must be code from existing coupon;

    - ```game_id``` - must be an id of existing game and must be equal to ```game_pk``` from url;

    - the current date must be within the range of the coupon;

    - INDIVIDUAL coupon can be allayed for ```user``` if this coupon was created for this ```user```;

    - user must have reserved places for the game and must have time to pay them within 5 minutes.

    ### Response example

    ```json
    {
      "yandex_token": "ct-24301ae5-000f-5000-9000-13f5f1c2f8e0",
      "payment_id": "25baba3a-000f-5000-a000-1016f655b8da"
    }
    ```

- ```/api/games/game_pk/team/``` (GET)

    Returns info about team for a game (id and game info).

- ```/api/games/game_pk/players/``` (GET)

    Returns info about all users for a game.

    ### Validators

    - ```game_pk``` from the url must belong to an existing game.

- ```/api/games/game_pk/players/player_pk/``` (GET)

    Returns info about registered user for a game.

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
