class Hallway:
    door1 = (-1, -1)
    door2 = (-1, -1)
    waypoints = []

    def __init__(self, door1, door2, waypoints):
        """The Hallway class which represent a hallway by storing its two connected door positions and a list of
        waypoint position.

        Arguments:
            door1(Point): the from door connected with the hallway.
            door2(Point): the to door connected with the hallway.
            waypoints([Point,...]): the list of waypoints.
        """
        self.door1 = door1
        self.door2 = door2
        self.waypoints = waypoints
