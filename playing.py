"""
Once a model is learned, use this to play it.
"""
import pygame
import Environment
import numpy as np
from nn import neural_net

NUM_SENSORS = 3


def play(model,environment):

    car_distance = 0
    # Create a new game instance.
    game_state = environment

    # Get initial state by doing nothing and getting the state.
    _, state, _ = game_state.run(2,"P")

    # Move.
    while not game_state.exit:
        car_distance += 1

        # Choose action.
        action = (np.argmax(model.predict(state, batch_size=1)))
        #print(action)

        # Take action.
        _, state, _ = game_state.run(action,"P")

        # Tell us something.
        if car_distance % 1000 == 0:
            pass#print("Current distance: %d frames." % car_distance)
    pygame.quit()
if __name__ == "__main__":
    saved_model = 'saved-models/128-128-64-50000-10000.h5'
    model = neural_net(NUM_SENSORS, [128, 128], saved_model)
    environment = Environment.Environment()
    play(model,environment)
