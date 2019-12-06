# GAMES API Endpoints

- ```/api/games/``` (GET)

    Returns info about all active games.
    
- ```/api/game/?date=yyyy-mm-dd``` (GET)

    Returns all active games and info for them for date from URL argument.
    
- ```/api/games/``` (POST)

    ```
    title (required)
    description (default '')
    cover_image (default None)
    timespan (required)
    duration (required)
    venue (reuqired)
    payment_method (ONLINE, default ONLINE)
    price (required)
    currency (RUB, default RUB)
    refund_money_if_game_is_cancelled (default False)
    refundable_days (default 0)
    game_status (PUBLIC, PRIVATE, default PUBLIC)
    a_side_players_count (5, 6, 7, 8, 9, 10, 11, default 5)
    registration_available (default True)
    cancel (default False)
    ```
  
    Create a game.
    
    ### Validators
    
    - ```price``` - must be positive integer or decimal.
    - ```duration``` - must be positive integer.
    
- ```/api/games/game_pk/``` (GET)

    Returns info about a game by it primary key.
    
    If the request contains a user authorization token - also returns:
    - a flag of whether the game passed or not;
    - number of seats purchased for this game.
    
- ```/api/games/game_pk/``` (DELETE)

    Delete a game by it primary key.
    
- ```/api/games/game_pk/``` (PUT, PATCH)

    ```
    title
    description
    cover_image
    timespan
    duration
    venue
    payment_methodtitle
    price
    currency
    refund_money_if_game_is_cancelled
    refundable_days
    game_status
    a_side_players_count
    registration_available
    cancel
    ```
  
    Update a game by it primary key.
    
    ### Validators
    
    - ```price``` - must be positive integer or decimal.
    - ```duration``` - must be positive integer.
    
- ```/api/games/game_pk/comments/``` (GET)

    Returns all comments and their count for a game by game primary key;
    
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
    
- ```/api/games/game_pk/teams/``` (GET)
    
    Returns all info about teams for a game.
    
- ```/api/games/game_pk/players/``` (GET)

    Returns info about all users for a game.
    
- ```/api/games/game_pk/players/``` (POST)

    ```
    game (required)
    user (required)
    team (required)
    user_position (required: GOALIE or DEFENDER or MIDFIELDER or FORWARD)
    ```
  
    Register user for a game.
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
    ### Validators
    
    - ```user``` must not be registered for the game.
    
- ```/api/games/game_pk/players/?team=white``` (GET)

    Returns info about all users for a white team for a game.
    
- ```/api/games/game_pk/players/?team=black``` (GET)

    Returns info about all users for a black team for a game.
    
- ```/api/games/game_pk/players/player_pk/``` (GET)

    Returns info about registered user for a game.
    
- ```/api/games/game_pk/players/player_pk/``` (DELETE)

    Delete user and all it`s reserved places for a game.
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
- ```/api/games/game_pk/reserved_places/``` (GET)

    Returns info about all reserved places for a game.
    
- ```/api/games/game_pk/reserved_places/``` (POST)

    ```
    title (required)
    game (required)
    team (required)
    user (required)
    reserved_position (required: GOALIE or DEFENDER or MIDFIELDER or FORWARD)
    ```

    Reserve a place for a player`s friend.
    
    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
    ### Validation
    
    - ```user``` - must be the participant of the game;
    - ```reserved_position``` - must not be NOT_SET.
    
- ```/api/games/game_pk/reserved_places/?team=white``` (GET)

    Returns info about all reserved places for a white team for a game.
    
- ```/api/games/game_pk/reserved_places/?team=black``` (GET)

    Returns info about all reserved places for a black team for a game.
    
- ```api/games/game_pk/reservd_places/reserve_user_pk/``` (GET)

    Returns info about all reserved places for reserve user.   
    
- ```api/games/game_pk/reservd_places/reserve_user_pk/?count=all``` (DELETE)

    Delete reserved place for player`s friend. ```count``` parameter can be a number or ```all``` word.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.
    
- ```api/games/game_pk/places_status/``` (GET)

    Returns info about total places count and occupied places count for a game.
    
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