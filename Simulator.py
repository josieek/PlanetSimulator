import pygame
import math
pygame.init()

WIDTH, HEIGHT = 900, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DARK_GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    #astronomical unit (distance from earth to sun in meters)
    AU = 149.6e6 * 1000
    G = 6.67428e-11 #gravitational constant
    SCALE = 250 / AU # 1AU = 100 pixels. Make smaller for closer planets
    TIMESTEP = 3600 * 24 # 1 day


    def __init__(self, x, y, radius, color, mass):
        self.x = x # x and y are in meters, distance from origin (sun)
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.moons = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        updated_points = []
        if len(self.orbit) > 2:
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x, y))

        for moon in self.moons:
            moon.draw(win)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun :
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

        for moon in self.moons:
            moon.update_position()

class Moon(Planet):
    def __init__(self, x, y, radius, color, mass, parent_planet):
        super().__init__(x, y, radius, color, mass)
        self.parent_planet = parent_planet

    def update_position(self):
        total_fx, total_fy = self.attraction(self.parent_planet)
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.parent_planet.x_vel += total_fx / self.parent_planet.mass * self.TIMESTEP
        self.parent_planet.y_vel += total_fy / self.parent_planet.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP + self.parent_planet.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP + self.parent_planet.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 15, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 11, RED, 6.39 * 10**24)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 10, DARK_GREY, 0.330 * 10**24)
    mercury .y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    phobos = Moon(-1.424 * Planet.AU, 0, 7, GREY, 1.0659 * 10**15, mars)
    # Phobos initialization
    distance_phobos_mars = abs(phobos.x - mars.x)
    phobos.y_vel= math.sqrt(Planet.G * mars.mass / distance_phobos_mars)

    deimos = Moon(-1.7 * Planet.AU, 0, 7, GREY, 1.4762 * 10**15, mars)
    # Deimos initialization
    distance_deimos_mars = abs(deimos.x - mars.x)
    deimos.y_vel = math.sqrt(Planet.G * mars.mass / distance_deimos_mars)

    moon = Moon(-1.1 * Planet.AU, 0, 7, GREY, 7.342 * 10**22, earth)
    # Moon initialization
    distance_moon_earth = abs(moon.x - earth.x)
    moon.y_vel = math.sqrt(Planet.G * earth.mass / distance_moon_earth)

    mars.moons.append(phobos)
    mars.moons.append(deimos)

    earth.moons.append(moon)

    planets = [sun, earth, mars, mercury, venus]


    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()