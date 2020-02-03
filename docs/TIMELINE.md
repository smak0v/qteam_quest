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
      "timeline": {
        "game_messages": [],
        "messages": []
      }
    }
    ```
