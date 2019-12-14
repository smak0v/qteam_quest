# USERS API Endpoints

- ```/api/users/``` (GET)

    Returns info about all users.

- ```/api/users/login/``` (POST)

    ```
    phone (required)
    ```

    Register user if phone not registered in system and sends SMS to phone number with one time password for user.

    Or if phone is registered in system only sends SMS to phone number with one time password for user.

     ### Validators:

    - ```phone``` - must be in russian number format and must be registered in system.

- ```/api/users/login/confirm/``` (POST)

    ```
    phone (required)
    sms_code (required)
    ```

    Login user in system using ```sms_code``` like password and ```phone``` like username.

     ### Validators:

    - ```phone``` - must be equal to sent earlier by SMS;

    - ```sms_code``` - must be in russian number format and must be registered in system.

- ```/api/users/logout/``` (GET)

    Logout user from system.
    
- ```/api/users/my_profile/``` (POST)

    ```
    token (required)
    ```

    Get user`s profile.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```token``` - must be valid user authorization token and must be equal to ```HTTP_AUTHORIZATION``` token from 
    ```HEADERS```.

- ```/api/users/user_pk/``` (DELETE)

    Delete user account.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/users/user_pk/``` (GET)

    Retrieve info about user.

    If user is not authenticated (request without authentication token) - returns basic info about requested user.

    If user is authenticated (request with authentication token) and ```user_pk``` != authenticated user - returns basic 
    info about requested user and subscription status for this user (```subscribed``` or ```not_subscribed```).

    If user is authenticated (request with authentication token) and ```user_pk``` == authenticated user - returns basic 
    info about requested user.

- ```/api/users/user_pk/``` (PUT, PATCH)

    ```
    username
    first_name
    last_name
    email
    location
    gender (NOT_SET, MALE, FEMALE)
    nationality
    profile_image (base64)
    ```

    Update user profile.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```username``` - unique;

    - ```email``` - unique, must be in email format;

    - ```profile_image``` - filename must be less than 256 symbols, file should not be empty.

- ```/api/users/user_pk/change_password/``` (PUT, PATCH)

    ```
    old_password (required)
    new_password_1 (required)
    new_password_2 (required)
    ```

    Change user password.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - authenticated user must have ```old_pasword``` password;

    - ```new_password_1``` and ```new_password_2``` - equal to each other, must include numbers and should not be in 
    ordinary words.

- ```/api/users/user_pk/change_password/``` (POST)

    ```
    phone (required)
    ```

    Change user phone number.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```phone``` - must be in russian number format and starts from '+' symbol.

- ```/api/users/user_pk/change_password_confirm/``` (POST)

    ```
    sms_code (required)
    ```

    Confirm user phone number.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - ```sms_code``` - must be a code from SMS.

- ```/api/users/user_pk/change_phone/``` (POST)

    ```
    phone (required)
    ```

    Change user phone.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

     ### Validators
     - ```phone``` - must be in russian number format.

- ```/api/users/user_pk/change_phone_confirm/``` (POST)

    ```
    sms_code (required)
    ```

    Activate user phone.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

     ### Validators
     - ```sms_code``` - must be like in SMS sent to user.

- ```/api/users/user_pk/venue_subscriptions/``` (GET)

    Get all user`s venue subscriptions.

- ```/api/users/user_pk/user_subscriptions/``` (GET)

    Get all user`s user subscriptions.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/users/user_pk/user_subscribers/``` (GET)

    Get all user`s user subscribers.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/users/user_pk/subscribe/``` (POST)

    ```
    user (required)
    subscriber (required)
    ```

    Subscribe ```user``` to ```subscriber```.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators:

    - subscription must`t exist;

    - ```user``` must`t be equal to ```subscriber```;

- ```/api/users/user_pk/unsubscribe/``` (DELETE)

    ```
    user (required)
    subscriber (required)
    ```

    Unsubscribe ```user``` from ```subscriber```.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

    ### Validators

    - subscription must exist;

- ```/api/users/user_pk/games/``` (GET)

    Return info about all user`s games.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/users/user_pk/past_games/``` (GET)

    Return info about all user`s past games.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint.

- ```/api/users/user_pk/future_games/``` (GET)

    Return info about all user`s future games.

    Authorization required. Add an authorization header ```Authorization: Token <authorization token>```, and you can 
    access the endpoint. 
