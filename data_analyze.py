import geopandas as gpd
import shapely
import datetime
import scipy.stats as stats
import matplotlib.pyplot as plt

severity_mapping = {
    "Accident with fatalities": 1,
    "Accident with severe injuries": 2,
    "Accident with light injuries": 3,
    "Accident with property damage": 4
}

type_mapping = {
    "Accident with skidding or self-accident": 0,
    "Accident when overtaking or changing lanes": 1,
    "Accident with rear-end collision": 2,
    "Accident when turning left or right": 3,
    "Accident when turning-into main road": 4,
    "Accident when crossing the lane(s)": 5,
    "Accident with head-on collision": 6,
    "Accident when parking": 7,
    "Accident involving pedestrian(s)": 8,
    "Accident involving animal(s)": 9,
    "Other": 10
}

class Categorize:
    def __init__(self, beforeimply, afterimply):
        self.beforeimply = beforeimply
        self.afterimply = afterimply

        self.severity_before = self.beforeimply["AccidentSeverityCategory_en"]
        self.severity_after = self.afterimply["AccidentSeverityCategory_en"]
        self.severity_before_numeric = [severity_mapping[x] for x in self.severity_before]
        self.severity_after_numeric = [severity_mapping[x] for x in self.severity_after]

        self.type_before = self.beforeimply["AccidentType_en"]
        self.type_after = self.afterimply["AccidentType_en"]
        self.type_before_numeric = [type_mapping[x] for x in self.type_before]
        self.type_after_numeric = [type_mapping[x] for x in self.type_after]

class T_Test:
    def __init__(self, cat_before, cat_after):
        self.before = cat_before
        self.after = cat_after

    def t_test(self):
        t_statistic, p_value = stats.ttest_ind(self.before, self.after)
        print("T-Statistic_s:", t_statistic)
        print("P-Value_s:", p_value)

class Involvement:
    def __init__(self, beforeimply, afterimply):
        self.bike_before = beforeimply[beforeimply["AccidentInvolvingBicycle"] == "true"]
        self.bike_after = afterimply[afterimply["AccidentInvolvingBicycle"] == "true"]

        self.pedestrian_before = beforeimply[beforeimply["AccidentInvolvingPedestrian"] == "true"]
        self.pedestrian_after = afterimply[afterimply["AccidentInvolvingPedestrian"] == "true"]