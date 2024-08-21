import streamlit as st
from openai import OpenAI
from pydantic import BaseModel
from typing import List, Literal, Union

class Questions:
    def __init__(self):
        self.init_questions()
        self.init_options()

    def init_questions(self):
        self.question1 = "Are you here to buy insurance?"
        self.question2 = "Great - what type of insurance are you looking for?"
        self.question3 = "What date do you need insurance to be effective?"
        self.question4 = "What is the reason you are purchasing insurance?"
        self.question5 = "What is the name of your business?"
        self.question6 = "This is what we found about your business. Does this look correct?"
        self.question7 = "Great! Please provide an email address and password to create your account."
        self.question8 = "Excellent! A link will be emailed/texted to you so you can complete your application later."

    def init_options(self):
        self.options1 = ["Yes", "No"]
        self.options2 = ["General Liability", "Contents", "Contents and Building", "Building Only"]
        self.options3 = ["ASAP", "Specific Date"]
        self.options4 = ["Purchase building", "New purchase", "Expiration of policy", "Starting new business", "Other"]
