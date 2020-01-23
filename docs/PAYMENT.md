# PAYMENT API Endpoints

- ```/api/payment/success/``` (POST)

    ```
    game_id (required)
    payment_id (required)
    ```

    Endpoint that returns status 200 OK if payment is successful. Finally register player`s places for the game.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```game_id``` - must be id of existing game;

    - ```payment_id``` - can`t be empty and must be an id of real payment;

    - user must have reserved places for the game and must have time to pay them within 5 minutes.

    ### Response

    ```json
    {
      "success": "Payment success!"
    }
    ```

- ```/api/payment/error/``` (POST)

    ```
    error (required)
    payment_id (required)
    ```

    Save error message for payment with ```payment_id```.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```payment_id``` - must be an id of real payment;

    - ```payment_id``` and ```error``` can`t be empty.

    ### Response

    ```json
    {
      "message": "Error saved successfully!"
    }
    ```
