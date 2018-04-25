#!/usr/bin/python3
''' Unit tests for DB storage '''
import os
import unittest
import models
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Only want to test Database storage")
class testDBStorage(unittest.TestCase):
    '''
    Testing the DB storage class
    '''
    def test_existence_user(self):
        '''
        Testing if User class is being created properly
        '''
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        if user.id in models.storage.all('User'):
            self.assertTrue(user.password, "johnpwd")

    def test_existence_amenity(self):
        '''
        Testing if Amenity class is being created properly
        '''
        amenity = Amenity(name="Wifi")
        amenity.save()
        if amenity.id in models.storage.all():
            self.assertTrue(amenity.name, "Wifi")

    def test_existence_state(self):
        '''
        Testing if State class is being created properly
        '''
        state = State(name="Alaska")
        state.save()
        if state.id in models.storage.all():
            self.assertTrue(state.name, "Alaska")

    def test_all_method(self):
        '''
        Testing if all() method returns all instances
        '''
        state = State(name="Cali")
        state.save()
        amenity = Amenity(name="Cable")
        amenity.save()
        user = User(email="john@snow.com", password="johnpwd")
        user.save()
        test_me = str(state.id) + str(amenity.id) + str(user.id)
        if test_me in models.storage.all():
            self.assertTrue(state.name, "Cali")

    def test_delete_method(self):
        '''
            Tests the delete method in db_storage
        '''
        state = State(name="Texas")
        state.save()
        all_stored = models.storage.all()
        models.storage.delete(state)
        self.assertTrue(all_stored["State." + state.id])

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "Only want to test Database storage")

class testDBStorageGetCount(unittest.TestCase):
    """Test of Get & Count methods"""
    
    @classmethod
    def setUp_Class(cls):
        storage.delete_all()
        cls.user1 = User(email="kevin@holberton.com", password="kevinpwd")
        cls.user2 = User(email="sue@holberton.com", password="suepwd")
        cls.state1 = State(name="California")
        cls.city1 = City(state_id=cls.state1.id, name="Sacramento")
        cls.city2 = City(state_id=cls.state1.id, name="San Francisco")
        cls.place1 = Place(user_id=cls.user1.id, city_id=cls.city1.id, name="Town House")
        cls.place2 = Place(user_id=cls.user2.id, city_id=cls.city2.id, name="Apartment")
        cls.amenity1 = Amenity("hot tub")
        cls.amenity2 = Amenity("roof deck")
        cls.amenity3 = Amenity("Garage")
        cls.amenity4 = Amenity("Wifi")
        
        objs = [cls.user1, cls.user2, cls.state1, cls.city1, cls.city2, cls.place1,
                   cls.place2, cls.amenity1, cls.amenity2, cls.amenity3, cls.amenity4]
        
        for obj in objs:
            obj.save()

    def setUp_Test(self):
        self.user1 = testDBStorageGetCount.user1
        self.user2 = testDBStorageGetCount.user2
        self.state1 = testDBStorageGetCount.state1
        self.city1 = testDBStorageGetCount.city1
        self.city2 = testDBStorageGetCount.city2
        self.place1 = testDBStorageGetCount.place1
        self.place2 = testDBStorageGetCount.place2
        self.amenity1 = testDBStorageGetCount.amenity1
        self.amenity2 = testDBStorageGetCount.amenity2
        self.amenity3 = testDBStorageGetCount.amenity3
        self.amenity4 = testDBStorageGetCount.amenity4

    def test_get_user1(self):
        test_user = storage.get('User', self.user1.id)
        check = self.user1.id
        self.assertEqual(check, test_user.id)

    def test_get_user2(self):
        test_user = storage.get('User', self.user2.id)
        check =self.user2.id
        self.assertEqual(check, test_user.id)

    def test_get_place1(self):
        test_place = storage.get('Place', self.place1.id)
        check = self.place1.id
        self.assertEqual(check, test_place.id)

    def test_count_users(self):
        test_users = storage.count('User')
        check = 2
        self.assertEqual(check, test_users)

    def test_count_places(self):
        test_places = storage.count('Place')
        check = 2
        self.assertEqual(check, test_places)

    def test_count_amenitys(self):
        test_amenities = storage.count('Amenity')
        check = 4
        self.assertEqual(check, test_amenities)
