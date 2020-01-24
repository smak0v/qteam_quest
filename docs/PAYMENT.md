# PAYMENT API Endpoints

- ```/api/payment/save/``` (POST)

    ```
    game_id (required)
    payment_id (required)
    ```

    Endpoint for saving Yandex payment. Finally register player`s places for the game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```game_id``` - must be id of existing game;

    - ```payment_id``` - can`t be empty and must be an id of real payment;

    - user must have reserved places for the game and must have time to pay them within 5 minutes.

    ### Success response

    ```json
    {
      "message": "Places were registered successfully!"
    }
    ```

    ### Error response

    ```json
    {
      "message": "Payment was canceled!",
      "party": "Party",
      "reason": "Reason"
    }
    ```
