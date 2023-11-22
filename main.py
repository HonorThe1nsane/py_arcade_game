import arcade


# Add this class to represent a pushable item
class PushableItem(arcade.Sprite):
    def __init__(self, filename, scale):
        super().__init__(filename, scale=scale)


SCREEN_TITLE = "Turkey Platformer"
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
DEFAULT_DAMPING = 1.0
PLAYER_DAMPING = 0.4
PLAYER_FRICTION = 1.0
WALL_FRICTION = 0.7
DYNAMIC_ITEM_FRICTION = 0.6
PLAYER_MASS = 2.0


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera_sprites = None
        self.camera_gui = None
        self.score = 0
        self.left_key_down = False
        self.right_key_down = False
        self.pushable_item = None

    def setup(self):
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)

        map_name = "levels/platform_tiles_turkeyLevel.tmx"

        layer_options = {
            "platform": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.score = 0

        src = ":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(src, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        pushable_item_src = ":resources:images/tiles/boxCrate_double.png"
        self.pushable_item = PushableItem(pushable_item_src, TILE_SCALING)
        self.pushable_item.center_x = 350
        self.pushable_item.center_y = 350
        self.scene.add_sprite("PushableItem", self.pushable_item)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["platform"]
        )

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.scene.draw()

        self.camera_sprites.use()
        self.player_sprite.draw()

        self.camera_gui.use()

    def update_player_speed(self):
        self.player_sprite.change_x = 0

        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
            self.pushable_item.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()
            self.pushable_item.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (
            self.camera_sprites.viewport_width / 2
        )
        screen_center_y = self.player_sprite.center_y - (
            self.camera_sprites.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):
        self.physics_engine.update()
        # Check for collision between player and pushable item
        if arcade.check_for_collision(self.player_sprite, self.pushable_item):
            # If the player is pushing the item to the right, move the item to the right
            if self.right_key_down and not self.left_key_down:
                self.pushable_item.center_x += PLAYER_MOVEMENT_SPEED
            # If the player is pushing the item to the left, move the item to the left
            elif self.left_key_down and not self.right_key_down:
                self.pushable_item.center_x -= PLAYER_MOVEMENT_SPEED
        self.center_camera_to_player()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
