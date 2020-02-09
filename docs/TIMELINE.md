# TIMELINE API Endpoints

- ```/api/timeline/user_pk/``` (GET)

    Returns a personalized for user from request timeline object.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```user_pk``` must be a pk of existing user and must the same as pk of user from request.

    ### Response example

    ```json
    {
      "timeline": [
          {
            "id": 1,
            "type": "GAME_MESSAGE",
            "timespan": "2020-02-05T01:32:37.881161+03:00",
            "message": "Message",
            "image": "image_url",
            "creator": "ADMIN",
            "user": 17,
            "game": 12
          },
          {}
        ]
    }
    ```

    Possible types:

    - ```GAME_MESSAGE```;

    - ```SIMPLE_MESSAGE```.

    Possible creators:

    - ```ADMIN``` - created by administrator;

    - ```APP``` - created programmatically.

    Game and image can be ```null```.
