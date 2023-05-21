from flask import Flask, current_app, jsonify
from lidar_nav import LidarNav


class LidarCoords(Flask):

    def __init__(self, application, *args, **kwargs):
        super().__init__(application)
        self.add_url_rule('/l_coords/calc', view_func=self.get_coords, methods=['POST',])
        self.coords = (0,0)
        self.lc = LidarNav()

    def get_coords(self, last_coordinates=(0,0)):
        
        self.coords = self.lc.get_coords(last_coordinates)
        return jsonify(self.coords), 200

    def __del__(self):
        pass


if __name__ == '__main__':

    lidar_coords_app = LidarCoords(__name__)
    lidar_coords_app.run(host='0.0.0.0', port=4996)

    lidar_coords_app.stop()