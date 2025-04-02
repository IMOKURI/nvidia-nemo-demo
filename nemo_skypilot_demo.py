import logging

import nemo_run as run
from nemo.collections import llm

from simple.add import SomeObject, add_object, commonly_used_object

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def configure_fn():
    fn = run.Partial(
        add_object,
        obj_1=commonly_used_object(),
        obj_2=run.Config(SomeObject, value_1=10, value_2=20, value_3=30),
    )
    return fn


def configure_recipe(nodes: int = 1, gpus_per_node: int = 2):
    recipe = llm.nemotron3_4b.pretrain_recipe(
        dir="/checkpoints/nemotron",  # Path to store checkpoints
        name="nemotron_pretraining",
        tensor_parallelism=2,
        num_nodes=nodes,
        num_gpus_per_node=gpus_per_node,
        max_steps=100,  # Setting a small value for the quickstart
    )

    # Add overrides here
    recipe.trainer.val_check_interval = 100

    return recipe


def common_envs():
    return {}


def skypilot_executor(container_image: str, gpus_per_node: int = 2):
    return run.SkypilotExecutor(
        gpus="L40S",  # sky show-gpus コマンドで確認
        gpus_per_node=gpus_per_node,
        env_vars=common_envs(),
        container_image=container_image,
        cloud="kubernetes",
        cluster_name="nemo_demo",
        file_mounts={"/nemo_app": "/app"},  # なにかマウントしておかないと、/nemo_runもマウント失敗しているよう。
        setup="""
        conda deactivate
        nvidia-smi
        """,
    )


def main():
    fn = configure_fn()
    # recipe = configure_recipe()
    executor = skypilot_executor(container_image="imokuri123/nemo-executor:v0.0.5")

    run.run(fn, executor=executor, name="nemotron3_4b_pretraining")


if __name__ == "__main__":
    main()
