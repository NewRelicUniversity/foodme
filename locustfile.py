#!/usr/bin/python

import random
from locust import FastHttpUser, TaskSet, between
from faker import Faker
fake = Faker()

customers = [
  'Emilia Brooks',
  'Hugo Awesomesauce',
  'Justin Ferguson',
  'Penelope Andrews',
  'Rebecca Elliott',
  'Rocco Marinara',
  'Yasmin Reid'
]

orders = [
    {
        "deliverTo.name": "",
        "deliverTo.address": "",
        "restaurant.name": "Beijing Express",
        "items": [{"name":"Egg rolls (4)","price":3.95,"qty":1},{"name":"General Tao's chicken","price":5.95,"qty":1},{"name": "Potstickers (6)","price":6.95,"qty":1}],
        "payment.cvc": "789",
        "payment.expire": "08/2027",
        "payment.number": "1234123412341234",
        "payment.type": "visa"
    },
    {
        "deliverTo.name": "",
        "deliverTo.address": "",
        "restaurant.name": "Naan Sequitur",
        "items": [{"name":"Butter Chicken","price":5.95,"qty":1},{"name":"Basmati rice","price":6.95,"qty":1},{"name":"Plain naan","price":5.95,"qty":1},{"name":"Gulab Jamun","price":8.95,"qty":1}],
        "payment.cvc": "789",
        "payment.expire": "08/2027",
        "payment.number": "1234123412341234",
        "payment.type": "visa"
    },
    {
        "deliverTo.name": "",
        "deliverTo.address": "",
        "restaurant.name": "Czech Point",
        "items": [{"name":"Chicken breast fillet schnitzel ","price":10.45,"qty":1},{"name":"Dumplings","price":5.95,"qty":1}],
        "payment.cvc": "789",
        "payment.expire": "08/2027",
        "payment.number": "1234123412341234",
        "payment.type": "visa"
    }
]

def restaurants(l):
    l.client.get("/api/restaurant")

def order(l):
    order = random.choice(orders)
    order["deliverTo.name"] = random.choice(customers)
    order["deliverTo.address"] = fake.street_address() + " " + fake.city() + ", " + fake.state_abbr() + " " + fake.zipcode()
    l.client.post("/api/order", json = order)
    
class UserBehavior(TaskSet):
    def on_start(self):
        restaurants(self)

    tasks = [restaurants, order]

class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
