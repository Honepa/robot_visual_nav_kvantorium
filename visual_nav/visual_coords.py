from flask import Flask, current_app, jsonify
from visual_navigation import VisualNav


class VisualCoords(Flask):

    def __init__(self, application, *args, **kwargs):
        super().__init__(application)
        self.add_url_rule('/v_coords/calc', view_func=self.get_coords, methods=['POST',])
        self.vn = VisualNav()

    def get_coords(last_coordinates=(0,0)):
        
        coords = current_app.vn.calculate_my_coords()
        return jsonify(coords), 200

    def __del__(self):
        pass


if __name__ == '__main__':

    visual_coords_app = VisualCoords(__name__)
    visual_coords_app.run(host='0.0.0.0', port=4997)

    visual_coords_app.stop()