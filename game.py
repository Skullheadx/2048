import pygame

from setup import *


two = 2  # The value of two. Do. Not. Change. It. Disastrous consequences. You have been warned.


class Tile:
    width = 100
    height = 100
    speed = 90 / 16  # since delta is 16 when fps is 60
    colours = [(238, 230, 219),
               (236, 224, 200),
               (239, 178, 124),
               (241, 152, 102),
               (243, 125, 99),
               (244, 96, 66),
               (236, 205, 122),
               (237, 203, 103),
               (236, 200, 90),
               (231, 194, 88),
               (232, 189, 78),
               ]

    def __init__(self, pos):
        self.position = pygame.Vector2(pos)
        self.target = self.position
        self.velocity = pygame.Vector2(0, 0)
        self.number = two ** random.randint(1, 2)  # the tile can start with 2 or 4 according to wikipedia
        self.can_merge = True
        self.colour = self.colours[math.floor(math.log(self.number, two)) - 1]
        self.label = Label(self.get_rect().center, [[[f"{self.number=}", self]]], 20, Colour.BLACK)

    @staticmethod
    def get_direction(start, end):
        out = end - start
        if out == pygame.Vector2(0, 0):
            return out
        return out.normalize()

    def update(self, delta, pos):
        self.target = pos
        self.velocity = self.get_direction(self.position, pos) * min((self.target - self.position).length(),
                                                                     self.speed * delta)  # so that we don't overshoot
        self.position += self.velocity  # We know that there will be no obstacles in the way
        self.label.update(delta, x=self.get_rect().centerx, y=self.get_rect().centery)
        self.colour = self.colours[math.floor(math.log(self.number, two)) - 1]

    def is_good(self):
        if self.position == self.target:
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.position + pygame.Vector2(5, 5),
                           (self.width - 10, self.height - 10))  # to account for the grid outlines

    def draw(self, surf):
        pygame.draw.rect(surf, self.colour, self.get_rect())
        self.label.draw(surf)


class Grid:
    rows = 4
    cols = 4
    cell_width = 100
    cell_height = 100
    width = cell_width * cols
    height = cell_height * rows
    offset = pygame.Vector2(SCREEN_WIDTH - width, SCREEN_HEIGHT - height) / 2

    def __init__(self):
        self.grid = self.new_grid()
        self.direction = None
        self.prev_direction = None
        self.just_pressed = False
        self.can_move = True
        for i in range(2):
            self.add_tile()

    def new_grid(self):
        return [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def no_legal_move(self):
        def in_bounds(r, c, grid, row):
            if (0 <= r <= len(grid) - 1 and
                    0 <= c <= len(row) - 1):
                return True
            return False

        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val is None:
                    return False
                elif isinstance(val, Tile):
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if (i == 0 or j == 0) and not (
                                    i == 0 and j == 0):  # so that we get the up, down, left, right no diagonal or center
                                if (in_bounds(r - i, c - j, self.grid, row) and
                                        isinstance(self.grid[r - i][c - j], Tile) and
                                        self.grid[r - i][c - j].number == self.grid[r][c].number):
                                    return False
        return True

    def get_empty(self):
        out = []
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if val is None:
                    out.append((r, c))
        return out

    def get_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            return "UP"
        elif pressed[pygame.K_DOWN]:
            return "DOWN"
        elif pressed[pygame.K_LEFT]:
            return "LEFT"
        elif pressed[pygame.K_RIGHT]:
            return "RIGHT"
        return None

    def update(self, delta, has_won):
        self.prev_direction = self.direction
        self.direction = self.get_input()
        if self.prev_direction != self.direction and self.direction is not None:
            self.just_pressed = True
        else:
            self.just_pressed = False

        score_this_turn = 0
        if self.can_move and self.just_pressed and has_won:
            for i in range(max(self.rows, self.cols)):
                if self.direction == "UP":
                    for r, row in enumerate(self.grid):
                        for c, val in enumerate(row):
                            if not c - 1 < 0:
                                if isinstance(val, Tile):
                                    target = self.grid[r][c - 1]
                                    if target is None:
                                        self.grid[r][c - 1] = self.grid[r][c]
                                        self.grid[r][c] = None
                                    elif isinstance(target,
                                                    Tile) and target.number == val.number and target.can_merge and val.can_merge:
                                        target.number *= two
                                        score_this_turn += target.number
                                        target.can_merge = False
                                        self.grid[r][c] = None

                elif self.direction == "DOWN":
                    for r, row in enumerate(self.grid):
                        for c, val in enumerate(row[::-1]):
                            if not c - 1 < 0:
                                if isinstance(val, Tile):
                                    target = self.grid[r][len(self.grid[r]) - c]
                                    if target is None:
                                        self.grid[r][len(self.grid[r]) - c] = self.grid[r][len(self.grid[r]) - c - 1]
                                        self.grid[r][len(self.grid[r]) - c - 1] = None
                                    elif isinstance(target,
                                                    Tile) and target.number == val.number and target.can_merge and val.can_merge:
                                        target.number *= two
                                        score_this_turn += target.number
                                        target.can_merge = False
                                        self.grid[r][len(self.grid[r]) - c - 1] = None
                elif self.direction == "LEFT":
                    for r, row in enumerate(self.grid):
                        for c, val in enumerate(row):
                            if not r - 1 < 0:
                                if isinstance(val, Tile):
                                    target = self.grid[r - 1][c]
                                    if target is None:
                                        self.grid[r - 1][c] = self.grid[r][c]
                                        self.grid[r][c] = None
                                    elif isinstance(target,
                                                    Tile) and target.number == val.number and target.can_merge and val.can_merge:
                                        target.number *= two
                                        score_this_turn += target.number
                                        target.can_merge = False
                                        self.grid[r][c] = None
                elif self.direction == "RIGHT":
                    for r, row in enumerate(self.grid[::-1]):
                        for c, val in enumerate(row):
                            if not r - 1 < 0:
                                if isinstance(val, Tile):
                                    target = self.grid[len(self.grid) - r][c]
                                    if target is None:
                                        self.grid[len(self.grid) - r][c] = self.grid[len(self.grid) - r - 1][c]
                                        self.grid[len(self.grid) - r - 1][c] = None
                                    elif isinstance(target,
                                                    Tile) and target.number == val.number and target.can_merge and val.can_merge:
                                        target.number *= two
                                        score_this_turn += target.number
                                        target.can_merge = False
                                        self.grid[len(self.grid) - r - 1][c] = None

        if self.just_pressed and has_won:
            self.add_tile()

        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if isinstance(val, Tile):
                    val.can_merge = True

        self.can_move = self.find_can_move(delta)
        return score_this_turn

    def win_condition(self):
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if isinstance(val, Tile):
                    if val.number == two ** 11:  # 2 ^ 11 = 2048
                        return True
        return False

    def add_tile(self):
        if len(self.get_empty()) > 0:
            r, c = random.choice(self.get_empty())
            self.grid[r][c] = Tile(self.offset + pygame.Vector2(r * self.cell_width, c * self.cell_height))

    def find_can_move(self, delta):
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                if isinstance(val, Tile):
                    val.update(delta, self.offset + pygame.Vector2(r * self.cell_width, c * self.cell_height))
                    if not val.is_good():
                        return False
        return True

    def get_rect(self, x=0, y=0, w=1, h=1):
        return pygame.Rect(self.offset + pygame.Vector2(x, y), (w, h))

    def get_cell_rect(self, x, y, w=1, h=1):
        return pygame.Rect(self.offset + pygame.Vector2(x, y), (self.cell_width * w, self.cell_height * h))

    def draw(self, surf):
        for r, row in enumerate(self.grid):
            for c, val in enumerate(row):
                pygame.draw.rect(surf, Colour.SQUARE_BG, self.get_cell_rect(r * self.cell_width, c * self.cell_height))
                pygame.draw.rect(surf, Colour.SQUARE_OUTLINE,
                                 self.get_cell_rect(r * self.cell_width, c * self.cell_height), 10)
                if isinstance(val, Tile):
                    val.draw(surf)
        pygame.draw.rect(surf, Colour.SQUARE_OUTLINE, self.get_rect(-5, -5, self.width + 10, self.height + 10), 10, 5)

class Effect:
    speed = 0.15

    def __init__(self, pos, txt):
        self.label = Label(pos, txt, 15, Colour.BLACK)
        self.vel_y = 0

    def update(self, delta):
        self.label.update(delta, y=self.label.position.y + self.vel_y)
        self.vel_y -= self.speed

    def is_out_of_bounds(self):
        if self.label.position.y + self.label.height < 0:
            return True
        return False


    def draw(self, surf):
        self.label.draw(surf)

class Game:
    # Background colour
    background_colour = (250, 248, 239)
    high_score = 0
    has_won = False

    def __init__(self):
        self.win = False
        self.game_over = False
        self.grid = Grid()
        self.win_effect = pygame.Surface((self.grid.width + 10, self.grid.height + 10))
        self.win_effect_time = 0
        self.game_title = two ** 11
        self.title = Label((0, 0), [[[f"{self.game_title=}", self]]], 50, Colour.BLACK, centered_x=False,
                           centered_y=False)
        self.score = 0
        self.score_label = Label((0, 0), [["Score:"], [[f"{self.score=}", self]]], 15, Colour.WHITE, filled=True,
                                 fill_colour=Colour.SQUARE_OUTLINE)
        self.high_score_label = Label((0, 0), [["Best:"], [[f"{self.high_score=}", self]]], 15, Colour.WHITE,
                                      filled=True, fill_colour=Colour.SQUARE_OUTLINE)
        self.new_game_button = Button((SCREEN_WIDTH / 2, SCREEN_HEIGHT * 8 / 9), [["New Game"]], 20, self.__init__,
                                      Colour.BLACK, filled=True, fill_colour=Colour.SQUARE_OUTLINE, outlined=True,
                                      outline_colour=Colour.GRAY, outline_radius=5)
        self.how_to_play = Label((0, 0),
                                 [["Join the numbers and get to the ", [f"{self.game_title=}", self], " tile!"]], 15,
                                 Colour.BLACK, centered_x=False)
        self.continue_button = Button((SCREEN_WIDTH / 3, SCREEN_HEIGHT * 3 / 5), [["Keep going"]], 20, self.keep_going,
                                      Colour.BLACK, filled=True, fill_colour=Colour.SQUARE_OUTLINE, outlined=True,
                                      outline_colour=Colour.GRAY, outline_radius=5)
        self.replay_button = Button((SCREEN_WIDTH/2, SCREEN_HEIGHT * 3 / 5), [["Try again"]], 20, self.__init__,
                                    Colour.BLACK, filled=True, fill_colour=Colour.SQUARE_OUTLINE, outlined=True,
                                    outline_colour=Colour.GRAY, outline_radius=5)
        self.win_label = Label((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - self.grid.cell_height / 4), [["You win!"]], 60,
                               Colour.WHITE)
        self.lose_label = Label((SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - self.grid.cell_height/4), [["You lose!"]], 60, Colour.WHITE)
        self.effects = []
        self.temp = 0
        self.update(0)

    def keep_going(self):
        self.has_won = True
        self.win = False

    def update(self, delta):
        if self.game_over:
            self.lose_label.update(delta)
            self.win_effect.fill(Colour.BLACK)
            self.win_effect.set_alpha(min(75, (math.floor(255 * self.win_effect_time / 1000))))
            self.win_effect_time += delta
            self.replay_button.update(delta, x=SCREEN_WIDTH / 2)

        self.temp = self.grid.update(delta, not self.win)
        self.score += self.temp
        if self.temp > 0:
            self.effects.append(Effect(self.score_label.position, [[f"+{self.temp}"]]))
        if self.win:
            self.win_label.update(delta)
            self.continue_button.update(delta)
            self.replay_button.update(delta, x=SCREEN_WIDTH * 2 / 3)
            self.win_effect.fill(Colour.GOLD)
            self.win_effect.set_alpha(min(75, (math.floor(255 * self.win_effect_time / 10000))))
            self.win_effect_time += delta
        self.high_score = max(self.score, self.high_score)
        if not self.has_won and self.grid.win_condition():
            self.win = True
            self.has_won = True
        if self.grid.no_legal_move():
            self.game_over = True
        self.title.update(delta, x=self.grid.offset.x, y=self.grid.offset.y - self.title.height * 1.5)
        self.high_score_label.update(delta, x=self.grid.offset.x + self.grid.width - self.high_score_label.width / 2,
                                     y=self.grid.offset.y - self.high_score_label.height * 1.5)
        self.score_label.update(delta,
                                x=self.high_score_label.position.x - self.high_score_label.width / 2 - self.score_label.width - Label.horizontal_padding,
                                y=self.grid.offset.y - self.high_score_label.height * 1.5)
        self.how_to_play.update(delta, x=self.grid.offset.x, y=self.grid.offset.y - self.how_to_play.height)
        self.new_game_button.update(delta)
        for effect in self.effects:
            effect.update(delta)
            if effect.is_out_of_bounds():
                del self.effects[self.effects.index(effect)]

    def draw(self, surf):
        surf.fill(self.background_colour)
        self.grid.draw(surf)
        self.title.draw(surf)
        self.score_label.draw(surf)
        self.high_score_label.draw(surf)
        self.new_game_button.draw(surf)
        self.how_to_play.draw(surf)
        for effect in self.effects:
            effect.draw(surf)
        if self.win:
            surf.blit(self.win_effect, self.grid.offset - pygame.Vector2(5, 5))
            self.win_label.draw(surf)
            self.continue_button.draw(surf)
            self.replay_button.draw(surf)
        elif self.game_over:
            surf.blit(self.win_effect, self.grid.offset - pygame.Vector2(5,5))
            self.lose_label.draw(surf)
            self.replay_button.draw(surf)


"""
class Tile:
    width = SCREEN_WIDTH / 2 / 4
    height = SCREEN_WIDTH / 2 / 4
    gravity_force = 0.1

    def __init__(self, pos, collide_list, number=2 ** random.randint(1,2)):
        self.position = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(0, 0)
        self.up_direction = pygame.Vector2(0, 0)
        self.collide_list = collide_list
        self.collide_list.append(self)
        self.can_move = True
        self.number = 2
        self.center = self.get_center()
        self.label = Label(self.center, [[[f"{self.number=}", self]]], 20, Colour.BLACK)

    def get_center(self):
        return self.position + pygame.Vector2(self.width/2, self.height/2)


    def get_collision_rect(self):
        return pygame.Rect(self.position, (self.width, self.height))

    def get_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.up_direction = pygame.Vector2(-1, 0)
            return True
        elif pressed[pygame.K_RIGHT]:
            self.up_direction = pygame.Vector2(1, 0)
            return True
        elif pressed[pygame.K_UP]:
            self.up_direction = pygame.Vector2(0, -1)
            return True
        elif pressed[pygame.K_DOWN]:
            self.up_direction = pygame.Vector2(0, 1)
            return True

    def collided(self, thing): # called when the tile collides
        self.can_move = True
        if isinstance(thing, Tile):
            if thing.number == self.number:
                thing.number *= 2
            if self in self.collide_list:
                del self.collide_list[self.collide_list.index(self)]

    def update(self, delta, can_move):
        if can_move:
            self.get_input()

        self.position, self.velocity = self.move_and_collide(delta, self.position, self.velocity, self.up_direction)
        self.center = self.get_center()
        self.label.update(delta, x=self.center.x, y=self.center.y)

    def move_and_collide(self, delta, position, velocity, up_direction=pygame.Vector2(0, 0)):
        pos = position
        vel = velocity
        vel += up_direction * delta * self.gravity_force

        pos.x += vel.x * delta
        for thing in self.collide_list:
            if thing == self:
                continue
            if self.get_collision_rect().colliderect(thing.get_collision_rect()):
                if vel.x > 0:
                    pos.x = thing.position.x - self.width
                else:
                    pos.x = thing.position.x + thing.width
                vel.x = 0
                self.collided(thing)
                break

        pos.y += vel.y * delta
        for thing in self.collide_list:
            if thing == self:
                continue
            if self.get_collision_rect().colliderect(thing.get_collision_rect()):
                if vel.y > 0:
                    pos.y = thing.position.y - self.height
                else:
                    pos.y = thing.position.y + thing.height
                vel.y = 0
                self.collided(thing)
                break

        return pos, vel

    def draw(self, surf):
        pygame.draw.rect(surf, Colour.RED, self.get_collision_rect())
        self.label.draw(surf)


class Wall:

    def __init__(self, pos, collide_list, is_vertical=True, face_right=True, visible=True):
        self.position = pygame.Vector2(pos)
        self.start_pos = pygame.Vector2(pos)
        self.collide_list = collide_list
        self.collide_list.append(self)

        self.visible = visible

        self.width = SCREEN_WIDTH / 2
        self.height = SCREEN_HEIGHT / 2

        if is_vertical:
            self.end_pos = self.position + pygame.Vector2(0, self.height)
            if not face_right:
                self.position.x -= self.width
        else:
            self.end_pos = self.position + pygame.Vector2(self.width, 0)
            if not face_right:
                self.position.y -= self.height

        self.end_point = pygame.Vector2(self.width, self.height)

    def get_collision_rect(self):
        return pygame.Rect(self.position, self.end_point)

    def update(self, delta):
        pass

    def draw(self, surf):
        # pygame.draw.rect(surf, Colour.BLACK, self.get_collision_rect())
        if self.visible:
            pygame.draw.line(surf, Colour.BLACK, self.start_pos, self.end_pos, 10)


class Game:

    def __init__(self):
        self.collision_list = []
        self.walls = [
            Wall((SCREEN_WIDTH / 4, SCREEN_HEIGHT * 3 / 4), self.collision_list, False, True),
            Wall((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), self.collision_list, False, False),
            Wall((SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4), self.collision_list, True, True),
            Wall((SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4), self.collision_list, True, False),
            Wall((SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT * 3 / 4), self.collision_list, False, True, False),
            Wall((SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4), self.collision_list, False, False, False),
            Wall((SCREEN_WIDTH/-4, SCREEN_HEIGHT / 4), self.collision_list, False, False, False),
            Wall((SCREEN_WIDTH / -4, SCREEN_HEIGHT * 5 /4), self.collision_list, False, False, False)
        ]
        self.can_move = True
        self.tiles = [
            Tile((SCREEN_WIDTH * 2 / 8, SCREEN_HEIGHT * 2 / 8), self.collision_list),
            Tile((SCREEN_WIDTH * 3 / 8, SCREEN_HEIGHT * 3 / 8), self.collision_list),
            Tile((SCREEN_WIDTH * 4 / 8, SCREEN_HEIGHT * 4 / 8), self.collision_list),
            Tile((SCREEN_WIDTH * 5 / 8, SCREEN_HEIGHT * 5 / 8), self.collision_list),
            ]
        self.title = Label((SCREEN_WIDTH/2, SCREEN_HEIGHT/8), ["2048"], 50, Colour.ORANGE)
        print(self.collision_list)


    def update(self, delta):

        if self.check_can_move():
            self.can_move = True
        else:
            self.can_move = False

        for tile in self.tiles:
            tile.update(delta, self.can_move)
        print(self.collision_list)

        for wall in self.walls:
            wall.update(delta)

        self.title.update(delta)

    def check_can_move(self):
        for tile in self.tiles:
            if not tile.can_move:
                return False
        return True
    def draw(self, surf):
        surf.fill(background_colour)

        for thing in self.collision_list:
            thing.draw(surf)

        self.title.draw(surf)

"""
