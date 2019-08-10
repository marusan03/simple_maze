from gym.envs.registration import register

register(
    id='muze-v0',
    entry_point='env:MuzeEnv'
)
