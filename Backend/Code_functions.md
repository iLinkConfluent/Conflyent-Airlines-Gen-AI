# Brief Code Document

## Overall Scenario Flow

### Variables and Functions

- `msg` = user's message from frontend requesting meal change.
- `chat_history` - chat history up until current user message.
- `response = chat_completion_request(chat_history, tool_list)` - the LLM's response for the user's query, given the chat history and available tools. `chat_completion_request()` calls the OpenAI API to obtain the LLM's response for the user's question.

### List of Tools

- `get_customer_bookings(customer_id)` :Given a customer's ID, return their flight booking information.
- `change_meal_plan(customer_id, flight_number, new_meal_plan)`: For the given customer, change the meal plan to `new_meal_plan` for the given flight.
- `get_airline_policy(query)`: Retrieve policy information relevant to the provided query text.
- `get_flight_gate(customer_id, source, destination)`: For the given customer id, source and destination airports, retrieve the departure gate number for the flight. *Additionally, simulates gate change by firing a timer that notifies of a changed gate after 15s*.
- `get_weather_information_for_flight(customer_id, flight_number)`: Retrieves the flight status and informs the customer if their flight may be impacted by weather etc. *Additionally simulates a flight cancellation due to inclement weather by firing a timer for 15s that notifies of cancelled flight.*

### Scenario 1 - Meal Change Flow

1. obtain user `msg` requesting meal change and `chat_history`.
2. Obtain LLM's response by leveraging `chat_completion_request()`. This response lists the user's flights and asks for updated meal plan.
3. Obtain updated meal plan from user and pass it to LLM as in steps 1-2
4. LLM requests calling of `change_meal_plan()` to update the meal plan. Result of execution of `change_meal_plan` passed back to LLM.
5. LLM generates response confirming meal plan update

### Scenario 2 - Policy Information

1. obtain user `msg` containing query regarding airline policy and `chat_history`.
2. Obtain LLM's response by leveraging `chat_completion_request()`. 
3. LLM requests calling of `get_airline_policy()` to retrieve relevant policy information. Result of execution of `get_airline_policy` passed back to LLM.
4. LLM generates response answering user query based on the relevant policy information.

### Scenario 3 - Gate Information

1. obtain user `msg` requesting gate information and `chat_history`.
2. Obtain LLM's response by leveraging `chat_completion_request()`. This response lists the user's flights and asks for which flight gate info is required.
3. Obtain flight number from user and pass it to LLM as in steps 1-2
4. LLM requests calling of `get_flight_gate()` to Retrieve gate information. Result of execution of `get_flight_gate` passed back to LLM.
5. LLM generates response detailing gate information. Furthermore a 15s timer begins to simulate arbitrary gate change. After 15s, the user is notified of the new gate.

### Scenario 4 - Weather Information

1. obtain user `msg` requesting flight status and `chat_history`.
2. Obtain LLM's response by leveraging `chat_completion_request()`. This response lists the user's flights and asks for which flight status info is required.
3. Obtain flight number from user and pass it to LLM as in steps 1-2
4. LLM requests calling of `get_weather_information_for_flight()` to retrieve flight status due to weather. Result of execution of `get_weather_information_for_flight` passed back to LLM.
5. LLM generates response detailing flight status information. Furthermore a 15s timer begins to simulate flight cancellation due to inclement weather. After 15s, the user is notified of the cancellation.
