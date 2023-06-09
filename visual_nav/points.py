from svg_pnt_actions import points_to_svg


points = {
    0: {
        0: {
            'file':'samples/point_0_0_740_320.jpeg',
            'w':  740,
            'h':  320,
            'x': 6000,
            'y':11000,
        },
        2: {
            'file':'samples/point_2_0_1470_1470.jpeg',
            'w': 1740,
            'h': 1740,
            'x':    0,
            'y': 9000,
        },
    },
    1: {
        0: {
            'file':'samples/point_0_1_1300_540.jpeg',
            'w':  420,
            'h':  300,
            'x':11100,
            'y': 9900,
        },
        2: {
            'file':'samples/point_2_1_640_550.jpeg',
            'w':  420,
            'h':  300,
            'x': 9600,
            'y':10800,
        },
    },
    2: {
        0: {
            'file':'samples/point_0_2_920_1360.jpeg',
            'w':  920,
            'h': 1360,
            'x': 9600,
            'y': 3300,
        },
        2: {
            'file':'samples/point_2_2_1810_1730.jpeg',
            'w': 1810,
            'h': 1730,
            'x':11400,
            'y': 7200,
        },
    },
    3: {
        2: {
            'file':'samples/point_2_3_700_1100.jpeg',
            'w':  700,
            'h': 1100,
            'x': 6300,
            'y':    0,
        },
        4: {
            'file':'samples/point_4_3_1100_1700.jpeg',
            'w': 1100,
            'h': 1700,
            'x':10800,
            'y': 6000,
        },
    },

    5: {
        2: {
            'file':'samples/point_2_4_350_310.jpeg',
            'w':300,
            'h':310,
            'x':0,
            'y':4500,
        },
        4: {
            'file':'samples/point_4_4_1400_1000.jpeg',
            'w':1400,
            'h':1000,
            'x':2900,
            'y':0,
        },
    }
}

if __name__ == '__main__':
    print(points_to_svg(points))
    