import argparse
import logging
from game.game import run_render
from game.renderer import Renderer

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', help='Train the model', required=False, default=False, action='store_true')
    parser.add_argument('--render', help='Run and show the renders', required=False, default=False, action='store_true')

    args = parser.parse_args()
    
    if args.train:
        from agent.trainer import train
        renderer = None
        if args.render:
            renderer = Renderer()
        train(renderer)
    elif args.render:
        run_render()
