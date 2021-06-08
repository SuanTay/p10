  
import sys
import pathlib
import pytest
import aiounittest
import asyncio
import unittest

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.schema import InputHints
from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from botbuilder.schema import Activity, ActivityTypes, Attachment
from botbuilder.core.adapters import TestAdapter
from dialogs.booking_dialog import BookingDialog
from bots.dialog_bot import DialogBot
from botbuilder.core import (
    TurnContext,
    ConversationState,
    UserState,
    BotTelemetryClient,
)
from botbuilder.schema import Activity, Attachment, ChannelAccount

#class TestUnitaire(aiounittest.AsyncTestCase):
class TestPyEval(unittest.TestCase):

    def test_positive_operand_expression(self):
        '''
        Tests a single positive operand expression
        '''
        expr = "53"
        self.assertEqual("53 ", expr, "Equal")
