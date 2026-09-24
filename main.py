from game.game import run_render
import argparse
import logging

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', help='Test the model', required=False, default=False, action='store_true')
    parser.add_argument('--train', help='Train the model', required=False, default=False, action='store_true')
    parser.add_argument('--render', help='Run and show the renders', required=False, default=False, action='store_true')

    args = parser.parse_args()

    if args.test and args.train:
        parser.error('Cannot be both test and train at the same time.')

    if not args.test and not args.train:
        logger.warning('No mode set, using test by default.')
    
    if args.render:
        run_render()
