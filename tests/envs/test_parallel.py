import pytest

from sotopia.agents import Agents, LLMAgent
from sotopia.database.persistent_profile import (
    AgentProfile,
    EnvironmentProfile,
)
from sotopia.envs import ParallelSotopiaEnv


@pytest.mark.asyncio
async def test_parallel_sotopia_env() -> None:
    env_profile = EnvironmentProfile(
        pk="test_pk",
        code_name="test",
        scenario="test",
        agent_goals=["test 1", "test 2"],
    )
    env = ParallelSotopiaEnv(env_profile=env_profile)

    agents = Agents(
        {
            "agent1": LLMAgent(
                "agent1",
                model_name="gpt-4o-mini",
                agent_profile=AgentProfile(
                    **{
                        "first_name": "John",
                        "last_name": "Doe",
                        "pk": "test_pk_agent_1",
                    },
                ),
            ),
            "agent2": LLMAgent(
                "agent2",
                model_name="gpt-4o-mini",
                agent_profile=AgentProfile(
                    **{
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "pk": "test_pk_agent_2",
                    }
                ),
            ),
        }
    )
    env.reset(agents=agents)
    max_steps = 5
    while env.agents:
        max_steps -= 1
        actions = {
            agent: env.action_space(agent).sample() for agent in env.agents
        }  # this is where you would insert your policy
        (
            observations,
            rewards,
            terminations,
            truncations,
            infos,
        ) = await env.astep(actions)
        if not max_steps:
            break


@pytest.mark.asyncio
async def test_parallel_sotopia_env_script_writing_single_step() -> None:
    env_profile = EnvironmentProfile(
        pk="test_pk",
        code_name="test",
        scenario="test",
        agent_goals=["test 1", "test 2"],
    )
    env = ParallelSotopiaEnv(env_profile=env_profile)

    agents = Agents(
        {
            "agent1": LLMAgent(
                "agent1",
                model_name="gpt-4o-mini",
                agent_profile=AgentProfile(
                    **{
                        "first_name": "John",
                        "last_name": "Doe",
                        "pk": "test_pk_agent_1",
                    }
                ),
                script_like=True,
            ),
            "agent2": LLMAgent(
                "agent2",
                model_name="gpt-4o-mini",
                agent_profile=AgentProfile(
                    **{
                        "first_name": "Jane",
                        "last_name": "Doe",
                        "pk": "test_pk_agent_2",
                    }
                ),
                script_like=True,
            ),
        }
    )
    env.reset(agents=agents)

    max_steps = 5
    while env.agents:
        max_steps -= 1
        actions = {
            agent: env.action_space(agent).sample() for agent in env.agents
        }  # this is where you would insert your policy
        (
            observations,
            rewards,
            terminations,
            truncations,
            infos,
        ) = await env.astep(actions)
        if not max_steps:
            break
