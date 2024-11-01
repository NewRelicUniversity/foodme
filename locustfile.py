#!/usr/bin/python

import json
import random
from locust import FastHttpUser, TaskSet, between
from faker import Faker
fake = Faker()

class Order:
    class Customer:
        name = ""
        address = ""
        def toJson(self):
            return dict(name = self.name, address = self.address)
    
    class Restaurant:
        name = ""
        def toJson(self):
            return dict(name = self.name)

    class Payment:
        cvc = "456"
        expire = "08/2027"
        number = "1234123412341234"
        type = "visa"
        def toJson(self):
            return dict(cvc = self.cvc, expire = self.expire, number = self.number, type = self.type)
    
    def __init__(self):
        self.deliverTo = self.Customer()
        self.restaurant = self.Restaurant()
        self.payment = self.Payment()
        self.items = []

    def toJson(self):
        return dict(deliverTo = self.deliverTo.toJson(), restaurant = self.restaurant.toJson(), payment = self.payment.toJson(), items = self.items)

customers = [
  'Emilia Brooks',
  'Hugo Awesomesauce',
  'Justin Ferguson',
  'Penelope Andrews',
  'Rebecca Elliott',
  'Rocco Marinara',
  'Yasmin Reid'
]

orders = []

order = Order()
order.restaurant.name = "Beijing Express"
order.items = [{"name":"Egg rolls (4)","price":3.95,"qty":1},{"name":"General Tao's chicken","price":5.95,"qty":1},{"name": "Potstickers (6)","price":6.95,"qty":1}]
orders.append(order)

order = Order()
order.restaurant.name = "Naan Sequitur"
order.items = [{"name":"Butter Chicken","price":5.95,"qty":1},{"name":"Basmati rice","price":6.95,"qty":1},{"name":"Plain naan","price":5.95,"qty":1},{"name":"Gulab Jamun","price":8.95,"qty":1}]
orders.append(order)

order = Order()
order.restaurant.name = "Czech Point"
order.items = [{"name":"Chicken breast fillet schnitzel ","price":10.45,"qty":1},{"name":"Dumplings","price":5.95,"qty":1}]
orders.append(order)

def restaurants(l):
    l.client.get("/api/restaurant")

def order(l):
    order = random.choice(orders)
    order.deliverTo.name = random.choice(customers)
    order.deliverTo.address = fake.street_address() + " " + fake.city() + ", " + fake.state_abbr() + " " + fake.zipcode()
    l.client.post("/api/order", json = order.toJson())

class UserBehavior(TaskSet):
    def on_start(self):
        restaurants(self)

    tasks = [restaurants, order]

class WebsiteUser(FastHttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
  
