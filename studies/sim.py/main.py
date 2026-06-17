import arcade
import simulator


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500 
WINDOW_TITLE = "GEARSIM"


def main():
    """ Main function """

    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create the GameView
    sim = simulator.Simulator()

    # Show GameView on screen
    window.show_view(sim)

    # Start the arcade game loop
    arcade.run()



if __name__ == "__main__":

    main()