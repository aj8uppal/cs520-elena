import unittest
import sys
import osmnx as ox
sys.path.append('../../')

from model.model import EleNa


class TestModel(unittest.TestCase):

    def test_origin_node(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302

        E = EleNa((start_lat, start_long), (end_lat, end_long))

        self.assertNotEqual(type(E.origin_node), None, "Should find a nearest node on the map.")

    def test_destination_node(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302

        E = EleNa((start_lat, start_long), (end_lat, end_long))

        self.assertNotEqual(type(E.destination_node), None, "Should find a nearest node on the map.")

    def test_default_path(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3916
        end_long = -72.5194

        E = EleNa((start_lat, start_long), (end_lat, end_long))

        self.assertEqual(E.shortest_path_custom(), [], "Should be an empty path for same start and end node.")

    def test_neighbour_travel(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302
        E = EleNa((start_lat, start_long), (end_lat, end_long))

        point = ox.get_nearest_node(E.get_graph(), (float(start_lat), float(start_long))) 
        neighbours = []
        for _,neighbor in E.get_graph().edges(point):
            neighbours.append(neighbor)

        path = E.shortest_path_custom()
        check = ox.get_nearest_node(E.get_graph(), (float(path[1][1]), float(path[1][0])))
        self.assertTrue(check in neighbours)

    def test_min_elev_dist(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302
        E = EleNa((start_lat, start_long), (end_lat, end_long), alg="min_elev_dist")
        E.shortest_path_custom()

        correct_path = [66691532, 66729584, 4277553939, 66764082, 66623950, 
        66688563, 66679422, 66692427, 66747253, 66610767, 66701452, 66672627]
        self.assertEqual(E.best_path, correct_path)

    def test_max_elev_dist(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302
        E = EleNa((start_lat, start_long), (end_lat, end_long), alg="max_elev_dist")
        E.shortest_path_custom()

        correct_path = [66691532, 66729584, 4277553939, 66764082, 66623950, 
        66688563, 66679422, 66692427, 66747253, 66610767, 66701452, 66672627]
        self.assertEqual(E.best_path, correct_path)

    def test_max_elev(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302
        E = EleNa((start_lat, start_long), (end_lat, end_long), alg="max_elev")
        E.shortest_path_custom()

        correct_path = [66691532, 6371920027, 66661136, 66764005, 66739703, 
        66702095, 66642506, 66661699, 66723121, 66719746, 66597142, 66680313, 
        66712389, 2111347918, 66611431, 66693426, 66601699, 66618290, 66736718, 
        66766174, 66707947, 66624533, 66752875, 66709470, 66606254, 66696752, 
        66701145, 66740793, 66590882, 66680199, 66705557, 66653057, 66695069, 
        66600236, 66755518, 66750618, 66696997, 66766106, 66704169, 66745361, 
        66704925, 66721706, 6775672007, 66591361, 66757569, 66713922, 2524415331, 
        66625145, 66754134, 66603981, 66609779, 66603685, 66720212, 66774321, 
        66738098, 66683824, 66634064, 66726263, 66746449, 66688542, 66649487, 
        8512412983, 8512412985, 66715579, 8512412988, 66693064, 66615522, 66690252, 
        66701422, 66672627]

        self.assertEqual(E.best_path, correct_path)

    def test_min_elev(self):
        start_lat = 42.3916
        start_long= -72.5194
        end_lat= 42.3843
        end_long = -72.5302
        E = EleNa((start_lat, start_long), (end_lat, end_long), alg="min_elev")
        E.shortest_path_custom()

        correct_path = [66691532, 6371920027, 66764082, 66623950, 66688563, 
        66679422, 66692427, 66747253, 66610767, 66701452, 66672627]
        self.assertEqual(E.best_path, correct_path)








if __name__ == '__main__':
    unittest.main()