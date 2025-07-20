import pygame
import random
import math

# robot that moves across the grid
class Robot:
    def __init__(self, x, y, dest_x, dest_y, closest_obstacle, screen, allobstacles):
        self.screen = screen
        self.x = x
        self.y = y
        self.dest_x = dest_x
        self.dest_y = dest_y
        self.closest_obstacle = closest_obstacle
        self.width = 60
        self.height = 60
        self.vel = 60
        self.allobstacles = allobstacles
        self.numObstacles = random.randint(1, 3)

    def drawObstacles(self):

        # Generate random placement for 3 alarms
        obstacle_coordinates = []
        for (i) in range(self.numObstacles):
            x = random.randint(0, 9) * 60
            y = random.randint(0, 9) * 60
            obstacle_coordinates.append((x, y))

        # paint alarms to screen
        for coord in obstacle_coordinates:
            rect = pygame.Rect(coord[0], coord[1], self.width, self.height)
            pygame.draw.rect(self.screen, "black", rect)

        pygame.display.update()

    # move robot to closest obstacle
    def move(self, closest_ob):
        vel = 60

        self.dest_x = closest_ob[0]
        self.dest_y = closest_ob[1]

        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.display.update()

        # clear robot's old position
        old_x = self.x
        old_y = self.y
        pygame.draw.rect(self.screen, (255, 255, 255), (old_x, old_y, self.width, self.height))

        if self.y > self.dest_y:
            self.y -= vel  # go up
        elif self.y < self.dest_y:
            self.y += vel  # go down
        else:
            # Only update x coordinate if the robot is not moving vertically
            if self.y == self.dest_y:
                if self.x < self.dest_x:
                    self.x += vel
                elif self.x > self.dest_x:
                    self.x -= vel

        if (self.x, self.y) == closest_ob:
            pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, self.width, self.height))
            pygame.display.update()
            self.vel = 0  # stop moving
            return

        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.display.update()

    def reachDest(self):
        return self.x == self.dest_x and self.y == self.dest_y


class Game:

    def __init__(self, num_robots):

        self.unassigned = []
        self.num_robots = num_robots

        # playing area dimensions
        self.gridw = 600
        self.gridh = 600

        # robot height and width
        self.width = 60
        self.height = 60

        # obstacle locations
        self.ob_coordinates = []

        self.robots = []

        self.cur_pos = 0, 0

        self.genMap()  # generate random placement for alarms

        self.assigned = []  # all finished tasks
        self.bot_pos = []  # bot positions after they reach dest, for next set of tasks

        self.r_x = 0
        self.r_y = 0

        self.num_alarms = 3

        pygame.init() # initializes pygame window

        # create a screen:
        self.screen = pygame.display.set_mode((self.gridw, self.gridh))

        self.main()

    def main(self):
        self.screen.fill((255, 255, 255))
        self.ob_coordinates = self.drawAlarms()  # create array of tasks (coordinates)
        self.unassigned = self.ob_coordinates.copy()  # tasks to do
        # obstacle_coordinates = self.drawObstacles()

        # Create an instance of the Robot class
        Bot = Robot(0, 0, 0, 0, None, self.screen, None)
        Bot.drawObstacles()

        # create certain number of robots
        for (i) in range(self.num_robots):

            # generate random starting positions for robots
            self.r_x = random.randint(0, 9) * 60
            self.r_y = random.randint(0, 9) * 60

            closest_obstacle = self.detectObstacles(self.unassigned)  # get the closest obstacle for each robot

            # make sure robots don't go to same alarm
            if closest_obstacle in self.unassigned:
                dest_x, dest_y = closest_obstacle

                self.unassigned.remove(closest_obstacle)
                self.assigned.append(closest_obstacle)

                # make a new robot at a random starting position
                self.robots.append(Robot(self.r_x, self.r_y, dest_x, dest_y, closest_obstacle, self.screen, self.unassigned))

        pygame.time.set_timer(pygame.USEREVENT, 500)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.USEREVENT:

                    # if self.num_robots > self.num_alarms:
                    for robot in self.robots:  # for each robot made

                        robot.move(robot.closest_obstacle)  # move all the robots to their closest task
                        reachDest = [robot.reachDest() for robot in self.robots]

                        if all(reachDest):  # if reach dest is true for this robot
                            self.cur_pos = robot.x, robot.y
                            self.bot_pos.append(self.cur_pos)
                            pygame.time.set_timer(pygame.USEREVENT, 0)

                    # if self.unassigned:  # if there is leftover tasks
                    #
                    #     # get the current positions of the robots and recalculate the robot closest to an obstacle
                    #     closest_obstacle = self.unassigned[0]  # get the closest obstacle for each robot
                    #
                    #     # get the closest bot to the remaining obstacle
                    #     closest_bot = self.calcNearestBot()
                    #     move_x, move_y = closest_bot
                    #
                    #     self.unassigned.remove(closest_obstacle)  # remove from to do list
                    #     self.assigned.append(closest_obstacle)  # add to finished task list
                    #
                    #     # get closest_bot
                    #     for bot in self.robots:
                    #         if bot.x == move_x and bot.y == move_y:
                    #             bot.closest_obstacle = closest_obstacle
                    #         bot.move(bot.closest_obstacle)  # move all the robots to their closest task
                    #
                    # elif not self.unassigned:
                    #     # when unassigned is empty then add more tasks
                    #     self.ob_coordinates = self.drawAlarms()  # create array of tasks (coordinates)
                    #     self.unassigned = self.ob_coordinates.copy()  # tasks to do

            self.drawGrid()


# create the grid environment
    def drawGrid(self):
        for x in range(0, 600, 60):
            pygame.draw.line(self.screen, 0, (1, x), (600, x), 2)
            pygame.draw.line(self.screen, 0, (x, 1), (x, 600), 2)
        pygame.display.update()


    def genMap(self):
        rows = 10
        cols = 10

        # Generate the matrix with all 0's
        self.matrix = [[0 for j in range(cols)] for i in range(rows)]

        # control number of total generated alarms
        for (i) in range(3):
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            self.matrix[row][col] = 1

    def drawAlarms(self):
        # Clear the screen
        self.screen.fill((255, 255, 255))

        # Generate random placement for 3 alarms
        self.ob_coordinates = []
        for (i) in range(self.num_alarms):
            x = random.randint(0, 9) * 60
            y = random.randint(0, 9) * 60
            self.ob_coordinates.append((x, y))

        # paint alarms to screen
        for coord in self.ob_coordinates:
            rect = pygame.Rect(coord[0], coord[1], self.width, self.height)
            pygame.draw.rect(self.screen, "blue", rect)

        pygame.display.update()
        return self.ob_coordinates

    # find closest robot to the remaining obstacle
    # returns the coordinates of the closest robot to the rem obstacle
    def calcNearestBot(self):

        closest_dist = float('inf')
        closest_bot = None

        for robot in self.robots:

            dist = ((robot.x - self.unassigned[0][0]) ** 2 + (robot.y - self.unassigned[0][1]) ** 2) ** 0.5
            print("dist", dist)
            if dist < closest_dist:
                closest_dist = dist
                closest_bot = robot

        return closest_bot


    # given the set of obstacles find the closest obstacle to the robot
    def detectObstacles(self, ob_coordinates):

        player_pos = (self.r_x, self.r_y)

        print(ob_coordinates)

        # initialize the closest distance and obstacle to the first obstacle in the set
        closest_dist = ((ob_coordinates[0][0] - player_pos[0]) ** 2 +
                        (ob_coordinates[0][1] - player_pos[1]) ** 2) ** 0.5
        self.closest_obstacle = ob_coordinates[0]

        # iterate over all obstacles and update closest distance and obstacle if a closer one is found
        for coord in ob_coordinates:
            dist = ((coord[0] - player_pos[0]) ** 2 + (coord[1] - player_pos[1]) ** 2) ** 0.5
            if dist < closest_dist:
                closest_dist = dist
                self.closest_obstacle = coord

        return self.closest_obstacle


if __name__ == "__main__":
    game = Game(num_robots=1)
