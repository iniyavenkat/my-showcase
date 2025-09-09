import functions_framework
import json
import requests


# takes in the inParams outcome from the previous function and passes it in
# this function tells the chatGPT api what to do with the input - make it into a complete sentence
def create_request(inParams):
    outReq = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                # telling the api how it should response, in this case being semi-formal
                "content": "Your name is Speech Assistant. When answering try to be semi-formal and very respectful."
            },
            {
                "role": "user",
                # telling the api what to do with the in Params - almost like passing this whole thing into chatGPT
                "content": "Create a complete sentence using the following words:" + inParams,
            }
        ]
    }

    json.dumps(outReq);
    return outReq


# defining the api key and making the call
def make_api_call2(in_params):
    # api call
    apiUrl = "https://api.openai.com/v1/chat/completions"

    # TODO : API key for chatGPT, hardcoding for now, will need to get this dynamically

    apiKey = “”


    # making a POST request to the api
    # authenticate the key
    # sending in the inParams in JSON format
    response = requests.post(apiUrl, auth=('Bearer Token', apiKey), headers={'Content-Type': 'application/json'},
                             json=in_params)

    return (response.content)


# creating the final response
def create_response(inRes):
    inRes = json.loads(inRes)
    # print(inRes)
    # print just the content and not all of the other parts
    outRes = inRes["choices"][0]["message"]["content"]
    return (outRes)


@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    # Extract API key from request headers or query parameters
    api_key = request.args.get('apiKey') or request.headers.get('x-api-key') or request.headers.get('X-goog-api-key')

    # TODO : Define your expected API key, hardcoding for now, will need to get this dynamically
    expected_api_key = “”

    # Check if API key is provided and matches the expected key
    if api_key and api_key == expected_api_key:
        # API key is valid, proceed with the function logic

        request_json = request.get_json(silent=True)
        request_args = request.args

        if request_json and 'question' in request_json:
            userQuestion = request_json['question']
        elif request_args and 'question' in request_args:
            userQuestion = request_args['question']
        else:
            return 'Sorry, please provide a valid input!'

        # "Please use these words to create a complete sentence: I work auto shop"

        print(userQuestion)
        requestForAPI = create_request(userQuestion)

        print(requestForAPI)

        # this method is using the open api using https post
        responseFromAPI = make_api_call2(requestForAPI)

        print(responseFromAPI)
        # this method is used to create the response back to the user
        userResponse = create_response(responseFromAPI)
        return f"Response from Assistant!: {userResponse}"

    else:
        # Unauthorized access
        return 'Unauthorized', 401



