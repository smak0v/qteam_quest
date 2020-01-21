# PAYMENT API Endpoints

- ```/api/payment/success/``` (POST)

    ```
    game_id (required)
    ```

    Endpoint that returns status 200 OK if payment is successful. Finally register player`s places for the game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```game_id``` - must be id of existing game;

    - user must have reserved places for the game and must have time to pay them within 5 minutes.

    ### Response

    ```json
    {
      "success": "Payment success!"
    }
    ```
