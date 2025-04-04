import logging

import nemo_run as run
from nemo.collections.llm.api import pretrain
from nemo.collections.llm.gpt.data import PreTrainingDataModule
from nemo.collections.llm.recipes.log.default import default_log, default_resume, tensorboard_logger
from nemo.collections.llm.recipes.nemotron import nemotron_model, nemotron_trainer
from nemo.collections.llm.recipes.optim.adam import distributed_fused_adam_with_cosine_annealing
from nemo.utils.exp_manager import TimingCallback

from simple.add import SomeObject, add_object, commonly_used_object

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def configure_fn():
    fn = run.Partial(
        add_object,
        obj_1=commonly_used_object(),
        obj_2=run.Config(SomeObject, value_1=10, value_2=20, value_3=30),
    )
    return fn


def configure_recipe(gpus_per_node, num_nodes) -> run.Partial:
    """
    https://github.com/NVIDIA/NeMo/blob/main/nemo/collections/llm/recipes/nemotron3_4b.py
    """
    dir = "/checkpoints/nemotron"
    name = "nemotron_pretraining"
    precision = "bf16-mixed"

    recipe = run.Partial(
        pretrain,
        model=nemotron_model("nemotron3_4b"),
        trainer=nemotron_trainer(
            tensor_parallelism=gpus_per_node,
            pipeline_parallelism=1,
            pipeline_parallelism_type=None,
            virtual_pipeline_parallelism=None,
            context_parallelism=1,
            sequence_parallelism=False,
            num_nodes=num_nodes,
            num_gpus_per_node=gpus_per_node,
            max_steps=2,
            precision=precision,
            accumulate_grad_batches=1,
            limit_test_batches=2,
            limit_val_batches=2,
            log_every_n_steps=1,
            val_check_interval=2,
            callbacks=[run.Config(TimingCallback)],
        ),
        data=run.Config(
            PreTrainingDataModule,
            paths=["/nemo_data/mc4-ja-tfrecord_text_document"],
            seq_length=4096,
            global_batch_size=32,
            micro_batch_size=2,
            split="80,10,10",
        ),
        log=default_log(dir=dir, name=name, tensorboard_logger=tensorboard_logger(name=name)),
        optim=distributed_fused_adam_with_cosine_annealing(
            precision=precision,
            warmup_steps=500,
            constant_steps=0,
            min_lr=3e-5,
            max_lr=3e-4,
            clip_grad=1.0,
        ),
        resume=default_resume(),
    )

    # Add overrides here
    recipe.trainer.val_check_interval = 2

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
        file_mounts={"/nemo_data": "/app/data"},  # なにかマウントしておかないと、/nemo_runのマウントも失敗しているよう。
        setup="""
        conda deactivate
        nvidia-smi
        """,
    )


def main():
    gpus_per_node = 4
    num_nodes = 1

    fn = configure_fn()
    recipe = configure_recipe(gpus_per_node, num_nodes)
    executor = skypilot_executor("nvcr.io/nvidia/nemo:25.02.01", gpus_per_node)

    with run.Experiment("nemo_demo", executor=executor) as experiment:
        experiment.add(fn, tail_logs=True)
        experiment.add(recipe, tail_logs=True)
        experiment.run()


if __name__ == "__main__":
    main()
