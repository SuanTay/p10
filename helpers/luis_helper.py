# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "Book"
    CANCEL = "Cancel"
    GET_WEATHER = "GetWeather"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(
        luis_recognizer: LuisRecognizer, turn_context: TurnContext
    ) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        print("LUIS Helper")
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()
                print("LUIS Helper01")
                # dst_city
                to_entities = recognizer_result.entities.get("$instance", {}).get("dst_city", [])
            
                if len(to_entities) > 0:
                    result.destination = to_entities[0]["text"].capitalize()
                # ----
                # nombre d'adults
                adults_entities = recognizer_result.entities.get("$instance", {}).get("n_adult", [] )
                if len(adults_entities) > 0:
                    result.adults = adults_entities[0]["text"]
                elif len(adults_entities)==0:
                    result.adults = 1
                # ----
                # or city
                from_entities = recognizer_result.entities.get("$instance", {}).get("or_city", [])
                if len(from_entities) > 0:
                    result.origin = from_entities[0]["text"].capitalize()
                    
                # ----
                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.
                # ----
                date_entities = recognizer_result.entities.get("str_date", [])
                if date_entities:
                    timex = date_entities[0]["timex"]

                    if timex:
                        datetime = timex[0].split("T")[0]

                        result.travel_date = datetime

                else:
                    result.travel_date = None

        except Exception as exception:
            print('execute_luis_query',exception)

        return intent, result
