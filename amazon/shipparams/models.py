from django.db import models
from math import radians, sin, cos, sqrt, asin

class Ship_params(models.Model):
    # zone = models.IntegerField(default=100)
    unit_dim_choices = [
        ("m","meters"),
        ("cm","centimeters"),
        ("in","inches"),
        ("ft","feet"),
    ]
    unit_wt_choices = [
        ("kg","kilograms"),
        ("g","grams"),
        ("lb","pounds"),
    ]
    length = models.FloatField(default=10)
    breadth = models.FloatField(default=10)
    height = models.FloatField(default=10)
    mode = models.IntegerField(default=2)
    actual_weight = models.IntegerField(default=1)
    slot = models.FloatField(default=1)
    days = models.FloatField(default=1)
    lat1 = models.FloatField(default=10.00)
    lon1 = models.FloatField(default=10.00)
    lat2 = models.FloatField(default=10.00)
    lon2 = models.FloatField(default=10.00)
    unit_dim = models.CharField(choices=unit_dim_choices, default="in")
    unit_wt = models.CharField(choices=unit_wt_choices, default="lb")

    def billable_weight(self):
        
        def convert_to_pounds(value, unit):
            if unit == "kg":
                return value * 2.20462  # 1 kilogram = 2.20462 pounds
            elif unit == "g":
                return value * 0.00220462  # 1 gram = 0.00220462 pounds
            else:
                return value
        def convert_to_inches(value):
            if self.unit == "m":
                return value * 39.37  # 1 meter = 39.37 inches
            elif self.unit == "cm":
                return value * 0.3937  # 1 centimeter = 0.3937 inches
            elif self.unit == "ft":
                return value * 12  # 1 foot = 12 inches
            else:
                return value
                
        weight = convert_to_pounds(self.actual_weight)
        length_inches = convert_to_inches(self.length)
        breadth_inches = convert_to_inches(self.breadth)
        height_inches = convert_to_inches(self.height)

        dim_weight = length_inches * breadth_inches * height_inches
        bill_weight = int(dim_weight / 139)

        if bill_weight > weight:
            return bill_weight
        else:
            return weight
        

    def haversine_distance(self):
            """
            Calculate the distance between two points on the Earth's surface using the haversine formula.

            Arguments:
            lat1 -- latitude of the first point (in degrees)
            lon1 -- longitude of the first point (in degrees)
            lat2 -- latitude of the second point (in degrees)
            lon2 -- longitude of the second point (in degrees)

            Returns:
            The distance between the two points (in miles).
            """
            # Convert latitude and longitude from degrees to radians
            lat1, lon1, lat2, lon2 = map(radians, [self.lat1, self.lon1, self.lat2, self.lon2])

            # Haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a))
            radius = 6371  # Radius of the Earth in kilometers
            distance = c * radius

            return distance*0.621371  # conversion into miles
    
    @staticmethod   
    def get_last_dig(miles):
        if miles >= 1 and miles <= 50:
            return "1"
        elif miles >= 51 and miles <= 150:
            return "2"
        elif miles >= 151 and miles <= 300:
            return "3"
        elif miles >= 301 and miles <= 600:
            return "4"
        elif miles >= 601 and miles <= 1000:
            return "5"
        elif miles >= 1001 and miles <= 1400:
            return "6"
        elif miles >= 1401 and miles <= 1800:
            return "7"
        elif miles >= 1801:
            return "8"

    def zone_calc(self):

        res = self.haversine_distance()

        mode=self.mode
        days=self.days
        slot=self.slot

        if mode==1:
            print(self.get_last_dig(res))

        else:
            if days==1 :
                if slot==1:
                    zone="10"+self.get_last_dig(res)
                elif slot==2:
                    zone="10"+self.get_last_dig(res)
                elif slot==3:
                    zone="13"+self.get_last_dig(res)
            elif days==2:
                if slot==1:
                    zone="24"+self.get_last_dig(res)
                elif slot==2:
                    zone="20"+self.get_last_dig(res)
            elif days==3:
                zone="30"+self.get_last_dig(res)

        return zone

    @property
    def cost(self):
        if self.billable_weight()>150:
            return -1

        t1_entry = T1.objects.get(zones=self.zone_calc(), weight=self.billable_weight(), time=self.slot)
        return t1_entry.price

class T1(models.Model):
    zones = models.IntegerField(db_column='Zones', blank=True, null=True)  # Field name made lowercase.
    weight = models.IntegerField(db_column='Weight', blank=True, null=True)  # Field name made lowercase.
    time = models.IntegerField(db_column='Time', blank=True, null=True)  # Field name made lowercase.
    price = models.FloatField(db_column='Price', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'air'


class T2(models.Model):
    dest_zip = models.IntegerField(db_column='Dest. ZIP', blank=True, null = True)
    ground = models.IntegerField(db_column='Ground', blank=True, null = True)
    three_day_select = models.IntegerField(db_column='3 Day Select', blank=True, null = True)
    two_day_air = models.IntegerField(db_column='2nd Day Air', blank=True, null = True)
    two_day_air_am = models.IntegerField(db_column='2nd Day Air A.M.', blank=True, null = True)
    next_day_air_saver = models.IntegerField(db_column='Next Day Air Saver', blank=True, null = True)
    two_day_air_am = models.IntegerField(db_column='Next Day Air', blank=True, null = True)

    class Meta:
        managed = False
        db_table = 'air'
