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


def configure_recipe(gpus_per_node, num_nodes):
    recipe = llm.nemotron3_4b.pretrain_recipe(
        dir="/checkpoints/nemotron",  # Path to store checkpoints
        name="nemotron_pretraining",
        tensor_parallelism=gpus_per_node,
        num_nodes=num_nodes,
        num_gpus_per_node=gpus_per_node,
        max_steps=2,  # Setting a small value for the quickstart
    )

    # Add overrides here
    recipe.trainer.val_check_interval = 100

    return recipe


def common_envs():
    return {}


def skypilot_executor(container_image, gpus_per_node):
    return run.SkypilotExecutor(
        gpus="L40S",  # sky show-gpus コマンドで確認
        gpus_per_node=gpus_per_node,
        env_vars=common_envs(),
        container_image=container_image,
        cloud="kubernetes",
        cluster_name="nemo_demo",
        file_mounts={"/nemo_app": "/app"},  # なにかマウントしておかないと、/nemo_runのマウントも失敗しているよう。
        setup="""
        conda deactivate
        nvidia-smi
        """,
    )


def main():
    gpus_per_node = 4
    num_nodes = 1

    # fn = configure_fn()
    recipe = configure_recipe(gpus_per_node, num_nodes)
    executor = skypilot_executor("imokuri123/nemo-executor:v0.0.5", gpus_per_node)

    # run.run(fn, executor=executor, name="add_object")
    run.run(recipe, executor=executor, name="nemotron3_4b_pretraining")


if __name__ == "__main__":
    main()
