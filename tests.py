from drivers import *
from truck_types import *
import datetime
import json
import requests
import unittest

class Tests(unittest.TestCase):
    ids = []
    url = 'http://0.0.0.0:5000/api'
    headers = {'Content-type':'application/json', 'Accept':'application/json'}

    now = datetime.datetime.now()
    oneWeekAgo = now - datetime.timedelta(days=7)
    oneMonthAgo = now - datetime.timedelta(days=30)

    drivers = [{
        'name': 'teste 1',
        'age': 33,
        'gender': 'M',
        'license_type': 'D',
        'has_truck': True,
        'truck_type': 1,
        'loaded': True,
        'origin': 'São Paulo, SP',
        'destination': 'Santos, SP',
        'stop_date': now.strftime('%d/%m/%Y %H:%M:%S')
    },
    {
        'name': 'teste 2',
        'age': 34,
        'gender': 'F',
        'license_type': 'C',
        'has_truck': False,
        'truck_type': 2,
        'loaded': False,
        'origin': 'Santos, SP',
        'destination': 'São Paulo, SP',
        'stop_date': now.strftime('%d/%m/%Y %H:%M:%S')
    },
    {
        'name': 'teste 3',
        'age': 35,
        'gender': 'F',
        'license_type': 'A',
        'has_truck': True,
        'truck_type': 1,
        'loaded': True,
        'origin': 'Santos, SP',
        'destination': 'São Paulo, SP',
        'stop_date': oneWeekAgo.strftime('%d/%m/%Y %H:%M:%S')
    },
    {
        'name': 'teste 4',
        'age': 36,
        'gender': 'M',
        'license_type': 'B',
        'has_truck': False,
        'truck_type': 1,
        'loaded': True,
        'origin': 'São Paulo, SP',
        'destination': 'Santos, SP',
        'stop_date': oneMonthAgo.strftime('%d/%m/%Y %H:%M:%S')
    }]

    combinations = [{
        'truck_type': 'Caminhão 3/4',
        'origin': 'São Paulo, SP',
        'destination': 'Santos, SP'
    },
    {
        'truck_type': 'Caminhão 3/4',
        'origin': 'Santos, SP',
        'destination': 'São Paulo, SP'
    },
    {
        'truck_type': 'Caminhão Toco',
        'origin': 'Santos, SP',
        'destination': 'São Paulo, SP'
    }]

    def getNotLoadedDrivers(self):
        response = requests.get(self.url + '/drivers/not-loaded', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def getCountDriversWithTruck(self):
        response = requests.get(self.url + '/drivers/with-truck', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def getCountLoadedByPeriod(self):
        response = requests.get(self.url + '/drivers/loaded-by-period', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def getOriginDestinationByTruckType(self):
        response = requests.get(self.url + '/drivers/origin-destination-by-truck-type', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def getDriverGeolocation(self, id):
        response = requests.get(self.url + '/drivers/geolocate/' + str(id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def postAddDriver(self, data):
        response = requests.post(self.url + '/drivers', json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def putEditDriver(self, id, data):
        response = requests.put(self.url + '/drivers/' + str(id), json.dumps(data), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        return response.json()

    def deleteDriver(self, id):
        response = requests.delete(self.url + '/drivers/' + str(id), headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def parseDate(self, dateString):
        return datetime.datetime.strptime(dateString, '%d/%m/%Y %H:%M:%S')

    def parseDateResponse(self, dateString):
        return datetime.datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%SZ')

    def assertDriverDataCorrect(self, data, driver):
        self.assertTrue(data['id'] > 0)
        self.assertEqual(data['name'], driver['name'])
        self.assertEqual(data['age'], driver['age'])
        self.assertEqual(data['gender'], driver['gender'])
        self.assertEqual(data['license_type'], driver['license_type'])
        self.assertEqual(data['has_truck'], driver['has_truck'])
        self.assertEqual(data['truck_type']['id'], driver['truck_type'])
        self.assertEqual(data['loaded'], driver['loaded'])
        self.assertEqual(data['origin'], driver['origin'])
        self.assertEqual(data['destination'], driver['destination'])
        self.assertEqual(self.parseDateResponse(data['stop_date']), self.parseDate(driver['stop_date']))

    def test_post_add_driver(self):
        driver = self.drivers[0]
        data = self.postAddDriver(driver)
        self.ids = [data['id']]
        self.assertDriverDataCorrect(data, driver)

    def test_put_edit_driver(self):
        new = self.postAddDriver(self.drivers[0])
        self.ids = [new['id']]
        data = self.putEditDriver( new['id'], self.drivers[1])
        self.assertDriverDataCorrect(data, self.drivers[1])

    def test_get_count_drivers_with_truck(self):
        self.ids = []
        data1 = self.getCountDriversWithTruck()
        for driver in self.drivers:
            data = self.postAddDriver(driver)
            self.ids += [data['id']]
        data2 = self.getCountDriversWithTruck()
        self.assertEqual(data2['count'], data1['count'] + 2)

    def test_get_not_loaded_drivers(self):
        self.ids = []
        for driver in self.drivers:
            data = self.postAddDriver(driver)
            self.ids += [data['id']]
        notLoadedDrivers = self.getNotLoadedDrivers()
        self.assertDriverDataCorrect(notLoadedDrivers[-1], self.drivers[1])

    def test_get_count_loaded_by_period(self):
        self.ids = []
        data1 = self.getCountLoadedByPeriod()
        for driver in self.drivers:
            data = self.postAddDriver(driver)
            self.ids += [data['id']]
        data2 = self.getCountLoadedByPeriod()
        self.assertEqual(data2['day'], data1['day'] + 1)
        self.assertEqual(data2['week'], data1['week'] + 2)
        self.assertEqual(data2['month'], data1['month'] + 3)

    def test_get_origin_destination_by_truck_type(self):
        data1 = self.getOriginDestinationByTruckType()
        count1 = {}
        for k, c in enumerate(self.combinations):
            for d in data1:
                if all(c[key] == d[key] for key in c):
                    count1[k] = d['count']
            if k not in count1:
                count1[k] = 0
        for driver in self.drivers:
            data = self.postAddDriver(driver)
            self.ids += [data['id']]
        data2 = self.getOriginDestinationByTruckType()
        count2 = {}
        for k, c in enumerate(self.combinations):
            for d in data2:
                if all(c[key] == d[key] for key in c):
                    count2[k] = d['count']
            if k not in count2:
                count2[k] = 0
        self.assertEqual(count2[0], count1[0] + 2)
        self.assertEqual(count2[1], count1[1] + 1)
        self.assertEqual(count2[2], count1[2] + 1)

    def test_get_driver_geolocation(self):
        driver = self.postAddDriver(self.drivers[0])
        self.ids = [driver['id']]
        data = self.getDriverGeolocation(driver['id'])
        self.assertEqual(data['origin_latitude'], -23.5506507)
        self.assertEqual(data['origin_longitude'], -46.6333824)
        self.assertEqual(data['destination_latitude'], -23.960833)
        self.assertEqual(data['destination_longitude'], -46.333889)

    def tearDown(self):
        for id in self.ids:
            self.deleteDriver(id)

if __name__ == '__main__':
    unittest.main()
