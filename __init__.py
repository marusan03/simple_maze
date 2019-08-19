from gym.envs.registration import register

register(
    id='Maze-v0',
    entry_point='simple_maze.env:MazeEnv'
)
