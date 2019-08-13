from gym.envs.registration import register

register(
    id='muze-v0',
    entry_point='simple_muze.env:MuzeEnv'
)
